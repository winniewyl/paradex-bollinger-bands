"""Visualization and Output"""

import matplotlib.pyplot as plt
from datetime import datetime
import os


def print_stats(stats, market, period, std_dev):
    """Print BB statistics"""
    print("\n" + "="*70)
    print(f"BOLLINGER BANDS ANALYSIS - {market}")
    print("="*70)
    print(f"Period: {period} | Std Dev: {std_dev} | Points: {stats['total_points']}")
    print(f"Time: {stats['timestamp']}")
    print("-"*70)
    print(f"Close:      ${stats['close']:,.2f}")
    print(f"SMA ({period}):    ${stats['sma']:,.2f}")
    print(f"Upper Band: ${stats['upper_band']:,.2f}")
    print(f"Lower Band: ${stats['lower_band']:,.2f}")
    print(f"Bandwidth:  {stats['bandwidth']:.2f}%")
    print(f"%B:         {stats['percent_b']:.2f}%")
    print("-"*70)
    print(f"Signal: {stats['signal']}")
    print("="*70)


def plot_chart(df, market, period, std_dev, last_n=1000):
    """Generate BB chart"""
    df_plot = df.tail(last_n)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), gridspec_kw={'height_ratios': [3, 1]})
    
    ax1.plot(df_plot['start_time'], df_plot['close'], label='Close', color='purple', linewidth=2)
    ax1.plot(df_plot['start_time'], df_plot['sma'], label=f'SMA({period})', color='blue', linewidth=2)
    ax1.plot(df_plot['start_time'], df_plot['upper_band'], label='Upper', color='red', linestyle='--')
    ax1.plot(df_plot['start_time'], df_plot['lower_band'], label='Lower', color='green', linestyle='--')
    ax1.fill_between(df_plot['start_time'], df_plot['upper_band'], df_plot['lower_band'], alpha=0.15, color='gray')
    ax1.set_title(f'Paradex Bollinger Bands - {market}', fontsize=18, fontweight='bold')
    ax1.set_ylabel('Price', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    ax2.bar(df_plot['start_time'], df_plot['volume'], color='steelblue', alpha=0.6)
    ax2.set_xlabel('Time', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Volume', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Create data folder if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    filename = f'data/paradex_bb_{market}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\n📊 Chart saved: {filename}")
    
    # Don't block - just save and continue
    # plt.show()  # Commented out to prevent blocking
    plt.close()  # Close figure to free memory
    
    return filename


def export_csv(df, market):
    """Export to CSV"""
    # Create data folder if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    filename = f'data/paradex_{market}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    df.to_csv(filename, index=False)
    print(f"💾 CSV saved: {filename}")
    return filename