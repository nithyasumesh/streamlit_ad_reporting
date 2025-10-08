import pandas as pd
import streamlit as st

# Define all available reports and their configurations
REPORT_CONFIGS = {
    "URL Report": {
        "file": "data/sample_ad_reporting__url_report.csv",
        "primary_dimension": "url_segment",
        "dimension_label": "URL Path"
    },
    "Ad Report": {
        "file": "data/sample_ad_reporting__ad_report.csv",
        "primary_dimension": "ad_name",
        "dimension_label": "Ad Name"
    },
    "Ad Group Report": {
        "file": "data/sample_ad_reporting__ad_group_report.csv",
        "primary_dimension": "ad_group_name",
        "dimension_label": "Ad Group"
    },
    "Campaign Report": {
        "file": "data/sample_ad_reporting__campaign_report.csv",
        "primary_dimension": "campaign_name",
        "dimension_label": "Campaign"
    },
    "Campaign Region Report": {
        "file": "data/sample_ad_reporting__campaign_region_report.csv",
        "primary_dimension": "region",
        "dimension_label": "Region"
    },
    "Campaign Country Report": {
        "file": "data/sample_ad_reporting__campaign_country_report.csv",
        "primary_dimension": "country",
        "dimension_label": "Country"
    },
    "Search Report": {
        "file": "data/sample_ad_reporting__search_report.csv",
        "primary_dimension": "keyword_text",
        "dimension_label": "Keyword"
    },
    "Keyword Report": {
        "file": "data/sample_ad_reporting__keyword_report.csv",
        "primary_dimension": "keyword_text",
        "dimension_label": "Keyword"
    },
    "Account Report": {
        "file": "data/sample_ad_reporting__account_report.csv",
        "primary_dimension": "account_name",
        "dimension_label": "Account"
    }
}

@st.cache_data
def load_report_data(report_type):
    """Load data based on selected report type"""
    if report_type not in REPORT_CONFIGS:
        report_type = "URL Report"  # Default fallback

    config = REPORT_CONFIGS[report_type]
    file_path = config["file"]

    df = pd.read_csv(file_path)

    # Handle different date column names
    if 'date_day' in df.columns:
        df['date_day'] = pd.to_datetime(df['date_day'])
    elif 'date_month' in df.columns:
        df['date_day'] = pd.to_datetime(df['date_month'])  # Rename to standardize

    # Add computed fields based on report type
    if report_type == "URL Report":
        df['url_segment'] = df['base_url'].apply(lambda x: '/' + x.split('/')[-1] if '/' in x else x)

    return df

def get_available_reports():
    """Get list of available report types"""
    return list(REPORT_CONFIGS.keys())

def get_report_config(report_type):
    """Get configuration for a specific report"""
    return REPORT_CONFIGS[report_type]