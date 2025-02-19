def calculate_health_metrics(data):
    """
    Calculate various health metrics from heart rate data
    """
    metrics = {
        'average_hr': data['heart_rate'].mean(),
        'min_hr': data['heart_rate'].min(),
        'max_hr': data['heart_rate'].max(),
        'hr_variability': data['heart_rate'].std()
    }
    
    return metrics

def check_alerts(heart_rate):
    """
    Check for abnormal heart rate values and return appropriate alerts
    """
    alerts = []
    
    if heart_rate < 50:
        alerts.append("Warning: Heart rate is below normal range (bradycardia)")
    elif heart_rate > 100:
        alerts.append("Warning: Heart rate is above normal range (tachycardia)")
    
    return "\n".join(alerts) if alerts else None
