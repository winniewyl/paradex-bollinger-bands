"""Paradex Bollinger Bands Calculator - Main Entry Point"""

import config
from paradex_client import generate_wallet, fetch_klines
from bollinger_bands import calculate_bollinger_bands, get_stats
from visualization import print_stats, plot_chart, export_csv


def main():
    print("="*70)
    print("PARADEX BOLLINGER BANDS CALCULATOR")
    print("="*70)
    
    # Check private key
    if not config.PRIVATE_KEY:
        print("\n⚠️  No private key found!")
        generate_wallet()
        print("\n👉 Paste the key in config.py and run again\n")
        return
    
    print(f"\nMarket: {config.MARKET} | Days: {config.DAYS} | Resolution: {config.RESOLUTION}min")
    env_text = 'TESTNET' if config.USE_TESTNET else 'PROD'
    print(f"Environment: {env_text}")
    
    try:
        # Fetch data
        df = fetch_klines(
            config.PRIVATE_KEY,
            config.MARKET,
            config.DAYS,
            config.RESOLUTION,
            config.USE_TESTNET
        )
        
        # Calculate BB
        print("\n🔢 Calculating Bollinger Bands...")
        df = calculate_bollinger_bands(df, config.BB_PERIOD, config.BB_STD_DEV)
        
        # Get stats
        stats = get_stats(df)
        
        # Display results
        print_stats(stats, config.MARKET, config.BB_PERIOD, config.BB_STD_DEV)
        
        # Plot chart
        if config.SAVE_CHART:
            plot_chart(df, config.MARKET, config.BB_PERIOD, config.BB_STD_DEV, config.CHART_POINTS)
        
        # Export CSV
        if config.SAVE_CSV:
            export_csv(df, config.MARKET)
        
        print("\n✅ Task completed successfully!\n")
        
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        print()


if __name__ == "__main__":
    main()