import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_heart_rate_data(n_points=100):
    """
    Generate mock heart rate data for testing
    """
    # Create time series
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=n_points)
    timestamps = pd.date_range(start_time, end_time, periods=n_points)
    
    # Generate heart rate data with realistic patterns
    base_hr = 70
    trend = np.sin(np.linspace(0, 4*np.pi, n_points)) * 10
    noise = np.random.normal(0, 2, n_points)
    heart_rates = base_hr + trend + noise
    
    # Ensure heart rates are within realistic bounds
    heart_rates = np.clip(heart_rates, 40, 200)
    
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'heart_rate': heart_rates.round(1)
    })
    
    return df
