import streamlit as st
import pandas as pd

def render_date_filter(df):
    """Render date range filter and return selected dates"""
    min_date = df['date_day'].min().date()
    max_date = df['date_day'].max().date()

    date_range = st.date_input(
        "Select date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="date_range"
    )

    return date_range

def render_platform_filter(df):
    """Render platform multiselect filter and return selected platforms"""
    platforms = df['platform'].unique()
    selected_platforms = st.multiselect(
        "Select platforms",
        platforms,
        default=platforms,
        key="platforms"
    )

    return selected_platforms

def apply_filters(df, date_range, selected_platforms):
    """Apply date and platform filters to the dataframe"""
    filtered_df = df.copy()

    # Apply date filter
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['date_day'].dt.date >= start_date) &
            (filtered_df['date_day'].dt.date <= end_date)
        ]

    # Apply platform filter
    filtered_df = filtered_df[filtered_df['platform'].isin(selected_platforms)]

    return filtered_df