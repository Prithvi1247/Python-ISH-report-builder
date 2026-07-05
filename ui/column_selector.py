"""Visible column selection widget for the report grid."""
import streamlit as st


def render_column_selector(all_columns, default_columns, key="visible_columns"):
    st.markdown("**Visible Columns**")
    selected = st.multiselect(
        "Choose columns to display in the report", options=all_columns, default=default_columns, key=key,
    )
    return selected
