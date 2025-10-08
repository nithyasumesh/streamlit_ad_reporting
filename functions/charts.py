import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_performance_over_time_chart(df):
    """Create performance over time line chart"""
    # Aggregate data by date
    daily_performance = df.groupby('date_day').agg({
        'spend': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum'
    }).reset_index()

    fig = px.line(
        daily_performance,
        x='date_day',
        y='spend',
        title="",
        labels={'spend': 'Spend ($)', 'date_day': 'Date'}
    )
    fig.update_layout(
        showlegend=False,
        height=300,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig

def create_platform_comparison_chart(df):
    """Create platform comparison bar chart with data labels"""
    # Aggregate data by platform
    platform_performance = df.groupby('platform').agg({
        'spend': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum'
    }).reset_index()

    # Sort by conversions (highest to lowest)
    platform_performance = platform_performance.sort_values('conversions', ascending=False)

    fig = px.bar(
        platform_performance,
        x='platform',
        y='conversions',
        title="",
        labels={'conversions': 'Conversions', 'platform': 'Platform'},
        color='conversions',
        color_continuous_scale=[[0, '#4A90E2'], [1, '#1A5490']]  # Light blue to dark blue
    )

    # Add data labels on top of bars
    fig.update_traces(
        texttemplate='%{y:,}',
        textposition='outside',
        textfont_size=12
    )

    fig.update_layout(
        showlegend=False,
        height=350,  # Increased overall height
        margin=dict(l=0, r=0, t=20, b=0),
        yaxis=dict(range=[0, platform_performance['conversions'].max() * 1.15])  # Add 15% padding above highest bar
    )

    return fig

def create_platform_performance_heatmap(df, report_type, report_config):
    """Create platform performance heatmap (flexible for different report types)"""

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
        group_by_field = report_config['primary_dimension']

    # Aggregate data by platform and the appropriate dimension
    heatmap_data = df_copy.groupby(['platform', group_by_field]).agg({
        'conversions': 'sum',
        'spend': 'sum',
        'conversions_value': 'sum'
    }).reset_index()

    # Calculate ROAS for heatmap values
    heatmap_data['roas'] = (heatmap_data['conversions_value'] / heatmap_data['spend']).round(1)
    heatmap_data['roas'] = heatmap_data['roas'].replace([float('inf'), -float('inf')], 0)

    # Pivot the data for heatmap
    pivot_data = heatmap_data.pivot(index=group_by_field, columns='platform', values='roas').fillna(0)

    # Set fixed height with good row spacing - let Plotly handle scrolling
    num_rows = len(pivot_data.index)
    row_height = 20  # Reduced row height for better performance

    # Use actual height needed for proper spacing, but let container handle overflow
    chart_height = max(400, num_rows * row_height)

    # Create text matrix for data labels
    text_matrix = pivot_data.applymap(lambda x: f"{x:.1f}x")

    # Create heatmap with text labels
    fig = px.imshow(
        pivot_data,
        labels=dict(x="Platform", y=report_config['dimension_label'], color="ROAS"),
        aspect="auto",
        color_continuous_scale="RdYlGn",
        title="",
        text_auto=False
    )

    # Add text using update_traces (more efficient than individual annotations)
    fig.update_traces(
        text=text_matrix.values,
        texttemplate="%{text}",
        textfont={"size": 9, "color": "black"}
    )

    # Update layout with scrollable configuration
    fig.update_layout(
        height=chart_height,
        margin=dict(l=0, r=0, t=50, b=50),  # More margin for top/bottom labels
        xaxis=dict(title='Platform'),
        yaxis=dict(side='left', autorange=True, title=report_config['dimension_label']),  # Normal order (bottom to top)
        font=dict(size=10)  # Ensure text is readable
    )

    # Configure x-axis to show labels on both top and bottom
    fig.update_xaxes(
        mirror='all',  # Shows tick labels on both top and bottom
        showticklabels=True
    )

    return fig