# ISH Admissions Report Centre

Internal enterprise reporting application for admissions staff, built with Streamlit.

## Run

```
pip install -r requirements.txt
streamlit run app.py
```

## Structure

```
app.py                     Application entry point / orchestration
data/
  Beta_SNAP_Cleaned.xlsx   Source workbook (Applicants, Programme Payments, Programme Mapping)
  loader.py                Cached workbook loading
engine/
  metadata.py              Infers column types and builds filter metadata automatically
  filter_engine.py         Applies filters to the Applicants dataframe
  export_engine.py         Excel / CSV export
ui/
  sidebar.py                Report selector
  filters.py                Dynamic filter widgets (text / date range / multiselect)
  column_selector.py        Visible column picker
  report_table.py           Summary bar, results grid, export buttons
config/
  report_registry.py        Registry of available reports (extend here for new reports)
```

## Notes

- The wide-format programme/test-payment columns embedded in the Applicants sheet
  (named `"... | <code>"`) are automatically excluded from filters and the report
  grid. The **Programme Payments** sheet is the sole source of truth for the
  Programme & Payment Status filter: selecting programmes filters that table,
  the matching StudentIDs are extracted, and the Applicants dataframe is then
  filtered by those IDs.
- Filters are grouped into Search Filters (text), Date Filters, and Categorical
  Filters, generated automatically from the dataset - no column names are
  hardcoded. Add new reports via `config/report_registry.py`.
