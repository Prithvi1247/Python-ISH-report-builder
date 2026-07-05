"""Registry of available reports. New reports are added here."""

REPORTS = {
    "Applicant Master Report": {
        "id": "applicant_master",
        "description": "Master listing of all applicants with configurable filters and column selection.",
        "primary_sheet": "Applicants",
    },
}

DEFAULT_REPORT = "Applicant Master Report"
