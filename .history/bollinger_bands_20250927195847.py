"""Bollinger Bands Calculator"""

import pandas as pd


def calculate_bollinger_bands(df, period=20, std_dev=2):
    """Calculate Bollinger Bands"""
    df = df.copy()
    
    df['sma'] = df['close'].rolling(window=period).mean()
    df['std'] = df['close'].rolling(window=period).std()
    df['upper_band'] = df['sma'] + (std_dev * df['std'])
    df['lower_band'] = df['sma'] - (std_dev * df['std'])
    df['bandwidth'] = (df['upper_band'] - df['lower_band']) / df['sma'] * 100
    df['percent_b'] = (df['close'] - df['lower_band']) / (df['upper_band'] - df['lower_band']) * 100
    
    return df


def get_signal(percent_b):
    """Get market signal from %B"""
    if pd.isna(percent_b):
        return "Insufficient data"
    elif percent_b > 100:
        return "Price ABOVE upper band (overbought)"
    elif percent_b < 0:
        return "Price BELOW lower band (oversold)"
    elif percent_b > 80:
        return "Strong uptrend"
    elif percent_b < 20:
        return "Strong downtrend"
    else:
        return "Normal range"


def get_stats(df):
    """Get latest BB statistics"""
    latest = df.iloc[-1]
    return {
        'timestamp': latest['start_time'],
        'close': latest['close'],
        'sma': latest['sma'],
        'upper_band': latest['upper_band'],
        'lower_band': latest['lower_band'],
        'bandwidth': latest['bandwidth'],
        'percent_b': latest['percent_b'],
        'signal': get_signal(latest['percent_b']),
        'total_points': len(df)
    }