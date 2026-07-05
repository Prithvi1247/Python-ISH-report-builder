"""Dynamic filter panel rendering. Widget type is chosen from column metadata."""
import streamlit as st


def render_applicant_filters(metadata):
    """Renders filter widgets grouped by type. Returns a filter_state dict keyed by column."""
    filter_state = {}

    text_fields = [m for m in metadata if m["filter_type"] == "text"]
    date_fields = [m for m in metadata if m["filter_type"] == "date_range"]
    categorical_fields = [m for m in metadata if m["filter_type"] == "multiselect"]

    with st.expander("Search Filters", expanded=False):
        for meta in text_fields:
            value = st.text_input(meta["column"], key=f"filter_text_{meta['column']}")
            filter_state[meta["column"]] = {"value": value}

    with st.expander("Date Filters", expanded=False):
        for meta in date_fields:
            if meta["min_date"] is None:
                st.caption(f"{meta['column']}: no data available")
                continue
            min_d, max_d = meta["min_date"].date(), meta["max_date"].date()
            date_range = st.date_input(
                meta["column"], value=(min_d, max_d), min_value=min_d, max_value=max_d,
                key=f"filter_date_{meta['column']}",
            )
            include_blanks = False
            if meta["has_blanks"]:
                include_blanks = st.checkbox("Include Blank Values", key=f"filter_date_blank_{meta['column']}")
            filter_state[meta["column"]] = {"date_range": date_range, "include_blanks": include_blanks}

    with st.expander("Categorical Filters", expanded=False):
        for meta in categorical_fields:
            selected = st.multiselect(meta["column"], options=meta["options"], key=f"filter_multi_{meta['column']}")
            include_blanks = False
            if meta["has_blanks"]:
                include_blanks = st.checkbox("Include Blank Values", key=f"filter_multi_blank_{meta['column']}")
            filter_state[meta["column"]] = {"selected": selected, "include_blanks": include_blanks}

    return filter_state


def render_programme_filter(applied_programmes_df):
    """Applied_Programmes table is the source of truth for the Programme filter."""
    st.markdown("**Programme & Payment Filter**")
    programme_options = sorted(applied_programmes_df["Applied Programme"].dropna().unique().tolist())
    selected_programmes = st.multiselect("Programme", options=programme_options, key="filter_programme")
    payment_status = st.radio("Payment Status", options=["Any", "Paid", "Not Paid"], horizontal=True, key="filter_payment_status")
    return selected_programmes, payment_status