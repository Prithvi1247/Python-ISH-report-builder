"""Column metadata inference used to auto-generate filter widgets."""
import pandas as pd

TEXT_KEYWORDS = ("name", "email", "id", "phone", "mobile")
MULTISELECT_MAX_UNIQUE = 60

# Applied_Programmes is the source of truth for programme filtering, so this
# free-text column is never used to generate a filter widget. It remains a
# normal, exportable column on the Applicants dataframe.
EXCLUDED_FILTER_COLUMNS = {"Select Programs you are applying to"}


def is_reportable_column(column: str) -> bool:
    """Excludes the raw programme/test-payment matrix columns (format 'Label | Code').
    Programme Payments is the source of truth for payment-status filtering, so
    these duplicate wide-format columns are never surfaced in filters or the
    report grid.
    """
    return " | " not in column


def get_reportable_columns(df: pd.DataFrame) -> list:
    return [c for c in df.columns if is_reportable_column(c)]


def get_filterable_columns(df: pd.DataFrame) -> list:
    return [c for c in get_reportable_columns(df) if c not in EXCLUDED_FILTER_COLUMNS]


def _sort_key(value):
    try:
        return (0, float(value))
    except (TypeError, ValueError):
        return (1, str(value))


def infer_filter_type(series: pd.Series, column_name: str) -> str:
    if pd.api.types.is_datetime64_any_dtype(series):
        return "date_range"

    name_lower = column_name.lower()
    if any(keyword in name_lower for keyword in TEXT_KEYWORDS):
        return "text"

    if series.nunique(dropna=True) <= MULTISELECT_MAX_UNIQUE:
        return "multiselect"

    return "text"


def build_metadata(df: pd.DataFrame) -> list:
    """Builds filter metadata for every reportable column in df."""
    metadata = []
    for column in get_filterable_columns(df):
        series = df[column]
        filter_type = infer_filter_type(series, column)
        entry = {"column": column, "dtype": str(series.dtype), "filter_type": filter_type}

        if filter_type == "multiselect":
            entry["options"] = sorted(series.dropna().astype(str).unique().tolist(), key=_sort_key)
            entry["has_blanks"] = bool(series.isna().any())
        elif filter_type == "date_range":
            valid = series.dropna()
            entry["min_date"] = valid.min() if not valid.empty else None
            entry["max_date"] = valid.max() if not valid.empty else None
            entry["has_blanks"] = bool(series.isna().any())
        else:
            entry["has_blanks"] = bool(series.isna().any())

        metadata.append(entry)
    return metadata