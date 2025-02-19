import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

def plot_heart_rate(data):
    """
    Create an interactive heart rate plot
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['timestamp'],
        y=data['heart_rate'],
        mode='lines+markers',
        name='Heart Rate',
        line=dict(color='#ff4b4b', width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title='Heart Rate Over Time',
        xaxis_title='Time',
        yaxis_title='Heart Rate (BPM)',
        hovermode='x unified',
        showlegend=False,
        yaxis=dict(range=[30, 210]),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    # Add reference zones
    fig.add_hrect(
        y0=40, y1=60,
        fillcolor="yellow", opacity=0.1,
        layer="below", line_width=0,
    )
    fig.add_hrect(
        y0=60, y1=100,
        fillcolor="green", opacity=0.1,
        layer="below", line_width=0,
    )
    fig.add_hrect(
        y0=100, y1=200,
        fillcolor="red", opacity=0.1,
        layer="below", line_width=0,
    )
    
    return fig

def plot_health_metrics(data):
    """
    Create a plot showing health metrics over time
    """
    # Calculate rolling metrics
    window = 10
    rolling_data = data.copy()
    rolling_data['avg_hr'] = data['heart_rate'].rolling(window=window).mean()
    rolling_data['hr_var'] = data['heart_rate'].rolling(window=window).std()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=rolling_data['timestamp'],
        y=rolling_data['avg_hr'],
        mode='lines',
        name='Average HR',
        line=dict(color='#2196f3', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=rolling_data['timestamp'],
        y=rolling_data['hr_var'],
        mode='lines',
        name='HR Variability',
        line=dict(color='#4caf50', width=2)
    ))
    
    fig.update_layout(
        title='Heart Rate Metrics Over Time',
        xaxis_title='Time',
        yaxis_title='Value',
        hovermode='x unified',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig
