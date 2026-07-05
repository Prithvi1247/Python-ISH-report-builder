"""ISH Admissions Report Centre - main application entry point."""
import time
import streamlit as st

from data.loader import load_workbook
from engine.metadata import build_metadata, get_reportable_columns
from engine.filter_engine import apply_filters, apply_applied_programme_filter, apply_payment_status_filter
from config.report_registry import REPORTS, DEFAULT_REPORT
from ui.sidebar import render_report_selector
from ui.filters import render_applicant_filters, render_programme_filter
from ui.column_selector import render_column_selector
from ui.report_table import render_summary, render_table, render_export_controls

st.set_page_config(page_title="ISH Admissions Report Centre", layout="wide")

applicants_df, payments_df, mapping_df, applied_programmes_df = load_workbook()
reportable_columns = get_reportable_columns(applicants_df)
metadata = build_metadata(applicants_df)

report_name = render_report_selector(REPORTS, DEFAULT_REPORT)

st.title("ISH Admissions Report Centre")
st.caption(REPORTS[report_name]["description"])
st.markdown("---")

if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = None
    st.session_state.applied_filters = []
    st.session_state.execution_time = 0.0

st.sidebar.markdown("### Filters")
with st.sidebar.form("filter_form"):
    filter_state = render_applicant_filters(metadata)
    st.markdown("---")
    selected_programmes, payment_status = render_programme_filter(applied_programmes_df)
    st.markdown("---")
    submitted = st.form_submit_button("Generate Report", use_container_width=True)

if submitted:
    start = time.perf_counter()
    result_df, applied_filters = apply_filters(applicants_df, filter_state, metadata)

    result_df, programme_summary = apply_applied_programme_filter(result_df, applied_programmes_df, selected_programmes)
    if programme_summary:
        applied_filters.append(programme_summary)

    result_df, payment_summary = apply_payment_status_filter(result_df, payments_df, payment_status)
    if payment_summary:
        applied_filters.append(payment_summary)

    elapsed = time.perf_counter() - start

    st.session_state.filtered_df = result_df
    st.session_state.applied_filters = applied_filters
    st.session_state.execution_time = elapsed

if st.session_state.filtered_df is None:
    st.info("Configure filters in the sidebar and click **Generate Report** to run the report.")
else:
    result_df = st.session_state.filtered_df
    default_columns = reportable_columns[:10]
    visible_columns = render_column_selector(reportable_columns, default_columns)

    render_summary(
        rows_returned=len(result_df),
        total_records=len(applicants_df),
        execution_time=st.session_state.execution_time,
        applied_filters=st.session_state.applied_filters,
        visible_columns=visible_columns,
    )

    if visible_columns:
        render_table(result_df, visible_columns)
        render_export_controls(result_df, visible_columns, report_name)
    else:
        st.warning("Select at least one column to display the report.")