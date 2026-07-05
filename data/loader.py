"""Data loading and caching layer. Reads the normalized workbook once per session."""
import os
import pandas as pd
import streamlit as st

DATA_PATH = os.path.join(os.path.dirname(__file__), "Beta_SNAP_Normalized.xlsx")

APPLICANT_SHEET = "Applicants"
PAYMENTS_SHEET = "Programme Payments"
MAPPING_SHEET = "Programme Mapping"
APPLIED_PROGRAMMES_SHEET = "Applied_Programmes"


@st.cache_data(show_spinner="Loading applicant data...")
def load_workbook(path: str = DATA_PATH):
    applicants = pd.read_excel(path, sheet_name=APPLICANT_SHEET)
    payments = pd.read_excel(path, sheet_name=PAYMENTS_SHEET)
    mapping = pd.read_excel(path, sheet_name=MAPPING_SHEET)
    applied_programmes = pd.read_excel(path, sheet_name=APPLIED_PROGRAMMES_SHEET)

    # Normalize StudentID to string across all lookup tables so joins against
    # Applicants always match reliably.
    applicants["StudentID"] = applicants["StudentID"].astype(str)
    payments["StudentID"] = payments["StudentID"].astype(str)
    applied_programmes["StudentID"] = applied_programmes["StudentID"].astype(str)

    return applicants, payments, mapping, applied_programmes