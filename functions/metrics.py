import pandas as pd
import numpy as np

def calculate_kpi_metrics(df):
    """Calculate KPI metrics from filtered dataframe"""
    total_spend = df['spend'].sum()
    total_impressions = df['impressions'].sum()
    total_clicks = df['clicks'].sum()
    total_conversions = df['conversions'].sum()
    total_conversions_value = df['conversions_value'].sum()

    # Calculate CTR, CVR, and ROAS
    ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    cvr = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
    roas = (total_conversions_value / total_spend) if total_spend > 0 else 0

    return {
        'total_spend': total_spend,
        'total_impressions': total_impressions,
        'total_clicks': total_clicks,
        'total_conversions': total_conversions,
        'total_conversions_value': total_conversions_value,
        'ctr': ctr,
        'cvr': cvr,
        'roas': roas
    }

def prepare_performance_table(df, report_type, report_config):
    """Prepare performance table with calculated metrics (flexible for different report types)"""

    df_copy = df.copy()

    # Handle different report types
    if report_type == "URL Report":
        # Extract just the final path segment from base_url
        df_copy['url_segment'] = df_copy['base_url'].apply(lambda x: '/' + x.split('/')[-1] if '/' in x else x)
        group_by_field = 'url_segment'
    elif report_type in ["Search Report", "Keyword Report"]:
        group_by_field = 'keyword_text'
    elif report_type == "Campaign Country Report":
        group_by_field = 'country'
    elif report_type == "Campaign Region Report":
        group_by_field = 'region'
    elif report_type == "Ad Report":
        group_by_field = 'ad_name'
    elif report_type == "Ad Group Report":
        group_by_field = 'ad_group_name'
    elif report_type == "Campaign Report":
        group_by_field = 'campaign_name'
    elif report_type == "Account Report":
        group_by_field = 'account_name'
    else:
        # Use the configured primary dimension
        group_by_field = report_config['primary_dimension']

    # Aggregate data by the appropriate dimension
    performance_data = df_copy.groupby(group_by_field).agg({
        'spend': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'impressions': 'sum',
        'conversions_value': 'sum'
    }).reset_index()

    # Calculate CTR, CPA, and ROAS
    performance_data['CTR'] = (performance_data['clicks'] / performance_data['impressions'] * 100).round(1)
    performance_data['CPA'] = (performance_data['spend'] / performance_data['conversions']).round(2)
    performance_data['CPA'] = performance_data['CPA'].replace([np.inf, -np.inf], np.nan)
    performance_data['ROAS'] = (performance_data['conversions_value'] / performance_data['spend']).round(1)
    performance_data['ROAS'] = performance_data['ROAS'].replace([np.inf, -np.inf], np.nan)

    # Format columns
    performance_data['Spend'] = performance_data['spend'].apply(lambda x: f"${x:,.0f}")
    performance_data['Clicks'] = performance_data['clicks'].apply(lambda x: f"{x:,}")
    performance_data['Conversions'] = performance_data['conversions'].apply(lambda x: f"{x:,}")
    performance_data['CTR_formatted'] = performance_data['CTR'].apply(lambda x: f"{x:.1f}%")
    performance_data['CPA_formatted'] = performance_data['CPA'].apply(lambda x: f"${x:.2f}" if pd.notna(x) else "N/A")
    performance_data['ROAS_formatted'] = performance_data['ROAS'].apply(lambda x: f"{x:.1f}x" if pd.notna(x) else "N/A")

    # Sort by spend (descending) and include all items
    performance_data = performance_data.sort_values('spend', ascending=False)
    display_df = performance_data[[group_by_field, 'Spend', 'Clicks', 'Conversions', 'CTR_formatted', 'CPA_formatted', 'ROAS_formatted']].copy()
    display_df.columns = [report_config['dimension_label'], 'Spend', 'Clicks', 'Conversions', 'CTR', 'CPA', 'ROAS']

    return display_df