"""Result grid, summary bar and export controls."""
import streamlit as st
from engine.export_engine import to_csv_bytes, to_excel_bytes


def render_summary(rows_returned, total_records, execution_time, applied_filters, visible_columns):
    st.markdown("### Report Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows Returned", rows_returned)
    c2.metric("Total Records", total_records)
    c3.metric("Execution Time", f"{execution_time:.3f} sec")

    with st.expander(f"Applied Filters ({len(applied_filters)})", expanded=False):
        if applied_filters:
            for line in applied_filters:
                st.write(f"- {line}")
        else:
            st.write("No filters applied.")

    with st.expander(f"Visible Columns ({len(visible_columns)})", expanded=False):
        st.write(", ".join(visible_columns) if visible_columns else "None selected")


def render_table(df, visible_columns):
    st.markdown("### Report Results")
    if df.empty:
        st.warning("No records match the selected filters.")
        return
    st.dataframe(df[visible_columns], use_container_width=True, height=480)


def render_export_controls(df, visible_columns, report_name):
    if df.empty:
        return
    export_df = df[visible_columns]
    st.markdown("### Export")
    c1, c2 = st.columns(2)
    file_stub = report_name.replace(" ", "_")
    c1.download_button(
        "Download Excel", data=to_excel_bytes(export_df), file_name=f"{file_stub}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True,
    )
    c2.download_button(
        "Download CSV", data=to_csv_bytes(export_df), file_name=f"{file_stub}.csv",
        mime="text/csv", use_container_width=True,
    )
