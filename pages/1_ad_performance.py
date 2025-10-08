import streamlit as st
from functions.data_loader import load_report_data, get_available_reports, get_report_config
from functions.filters import render_date_filter, render_platform_filter, apply_filters
from functions.metrics import calculate_kpi_metrics, prepare_performance_table
from functions.charts import create_performance_over_time_chart, create_platform_comparison_chart, create_platform_performance_heatmap

# Page configuration
st.set_page_config(
    page_title="Ad Performance Report",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Title
st.title("Ad Performance Report")

# Report Type filter
st.subheader("Report Type")
available_reports = get_available_reports()
selected_report = st.selectbox(
    "Select report type",
    available_reports,
    index=0,
    key="report_type"
)

# Load data based on selected report
df = load_report_data(selected_report)
report_config = get_report_config(selected_report)

st.markdown("---")

# Date range and platform filters
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Date Range")
    date_range = render_date_filter(df)

with col2:
    st.subheader("Platforms")
    selected_platforms = render_platform_filter(df)

# Apply filters
filtered_df = apply_filters(df, date_range, selected_platforms)

# KPI metrics
st.markdown("---")
col1, col2, col3, col4, col5, col6 = st.columns(6)

metrics = calculate_kpi_metrics(filtered_df)

with col1:
    st.metric(
        label="Spend",
        value=f"${metrics['total_spend']/1000:.1f}k",
        help="Total amount spent on advertising campaigns across all selected platforms and time period"
    )

with col2:
    st.metric(
        label="Impressions",
        value=f"{metrics['total_impressions']/1000:.1f}k",
        help="Total number of times ads were displayed to users across all campaigns"
    )

with col3:
    st.metric(
        label="CTR",
        value=f"{metrics['ctr']:.1f}%",
        help="Click-Through Rate: Percentage of impressions that resulted in clicks (Clicks ÷ Impressions × 100)"
    )

with col4:
    st.metric(
        label="CVR",
        value=f"{metrics['cvr']:.1f}%",
        help="Conversion Rate: Percentage of clicks that resulted in conversions (Conversions ÷ Clicks × 100)"
    )

with col5:
    st.metric(
        label="Conversions",
        value=f"{int(metrics['total_conversions'])}",
        help="Total number of desired actions completed by users (purchases, sign-ups, downloads, etc.)"
    )

with col6:
    st.metric(
        label="ROAS",
        value=f"{metrics['roas']:.1f}x",
        help="Return on Ad Spend: Revenue generated per dollar spent (Conversion Value ÷ Spend). Higher is better."
    )

st.markdown("---")

# Charts section
col1, col2 = st.columns(2)

with col1:
    st.subheader("Spend Over Time")
    fig_line = create_performance_over_time_chart(filtered_df)
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.subheader("Platform Comparison")
    fig_bar = create_platform_comparison_chart(filtered_df)
    st.plotly_chart(fig_bar, use_container_width=True)

# Platform Performance Heatmap
heatmap_title = f"Platform-{report_config['dimension_label']} Performance Heatmap"
st.subheader(heatmap_title)
heatmap_subtitle = f"*ROAS (Return on Ad Spend) by platform and {report_config['dimension_label'].lower()} - darker green indicates better performance*"
st.markdown(heatmap_subtitle)

# Create scrollable container for heatmap (like the table below)
with st.container(height=500):
    heatmap_fig = create_platform_performance_heatmap(filtered_df, selected_report, report_config)
    st.plotly_chart(heatmap_fig, use_container_width=True)

st.markdown("---")

# Performance table (dynamic based on report type)
table_title = f"{report_config['dimension_label']} Performance"
st.subheader(table_title)
performance_table = prepare_performance_table(filtered_df, selected_report, report_config)
st.dataframe(performance_table, use_container_width=True, hide_index=True)