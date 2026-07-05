"""Applies user-selected filters to the Applicants dataframe."""
import pandas as pd


def apply_text_filter(df, column, value):
    mask = df[column].astype(str).str.contains(value, case=False, na=False, regex=False)
    return df[mask]


def apply_multiselect_filter(df, column, selected, include_blanks):
    mask = df[column].astype(str).isin(selected)
    if include_blanks:
        mask = mask | df[column].isna()
    return df[mask]


def apply_date_range_filter(df, column, start, end, include_blanks):
    series = pd.to_datetime(df[column], errors="coerce")
    mask = (series.dt.date >= start) & (series.dt.date <= end)
    if include_blanks:
        mask = mask | series.isna()
    return df[mask]


def apply_filters(df, filter_state, metadata):
    """filter_state: dict of column -> widget values captured from the filter form."""
    applied_summary = []
    result = df.copy()
    meta_by_column = {m["column"]: m for m in metadata}

    for column, state in filter_state.items():
        meta = meta_by_column.get(column)
        if meta is None:
            continue

        if meta["filter_type"] == "text":
            value = state.get("value", "").strip()
            if value:
                result = apply_text_filter(result, column, value)
                applied_summary.append(f"{column} contains '{value}'")

        elif meta["filter_type"] == "multiselect":
            selected = state.get("selected", [])
            include_blanks = state.get("include_blanks", False)
            if selected:
                result = apply_multiselect_filter(result, column, selected, include_blanks)
                label = ", ".join(selected) if len(selected) <= 5 else f"{len(selected)} values selected"
                if include_blanks:
                    label += " (incl. blanks)"
                applied_summary.append(f"{column}: {label}")

        elif meta["filter_type"] == "date_range":
            date_range = state.get("date_range")
            include_blanks = state.get("include_blanks", False)
            if date_range and len(date_range) == 2:
                start, end = date_range
                if start != meta["min_date"].date() or end != meta["max_date"].date():
                    result = apply_date_range_filter(result, column, start, end, include_blanks)
                    label = f"{start} to {end}"
                    if include_blanks:
                        label += " (incl. blanks)"
                    applied_summary.append(f"{column}: {label}")

    return result, applied_summary


def apply_applied_programme_filter(applicants_df, applied_programmes_df, selected_programmes):
    """Applied_Programmes is the source of truth for programme-based filtering.
    The 'Select Programs you are applying to' free-text column on Applicants,
    and the wide-format programme columns, are never inspected.
    """
    if not selected_programmes:
        return applicants_df, None

    mask = applied_programmes_df["Applied Programme"].isin(selected_programmes)
    matched_ids = applied_programmes_df.loc[mask, "StudentID"].unique()
    filtered = applicants_df[applicants_df["StudentID"].isin(matched_ids)]

    programme_label = (
        ", ".join(selected_programmes) if len(selected_programmes) <= 3
        else f"{len(selected_programmes)} programmes selected"
    )
    summary = f"Applied Programme: {programme_label}"
    return filtered, summary


def apply_payment_status_filter(applicants_df, payments_df, payment_status):
    """Programme Payments is the source of truth for payment-status filtering."""
    if payment_status == "Any":
        return applicants_df, None

    mask = payments_df["Payment Status"] == payment_status
    matched_ids = payments_df.loc[mask, "StudentID"].unique()
    filtered = applicants_df[applicants_df["StudentID"].isin(matched_ids)]

    summary = f"Payment Status: {payment_status}"
    return filtered, summary