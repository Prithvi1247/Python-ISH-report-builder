"""Report selection sidebar header."""
import streamlit as st


def render_report_selector(report_registry, default_report):
    st.sidebar.title("ISH Admissions Report Centre")
    st.sidebar.caption("Internal Reporting Module")
    st.sidebar.markdown("---")
    report_names = list(report_registry.keys())
    report_name = st.sidebar.selectbox("Select Report", report_names, index=report_names.index(default_report))
    st.sidebar.markdown("---")
    return report_name
