"""Paradex API Client"""

import secrets
import pandas as pd
from datetime import datetime, timedelta
from eth_account import Account
from paradex_py import Paradex

# Import environment constants directly
try:
    from paradex_py.environment import TESTNET, PROD
except ImportError:
    # Try alternative import
    try:
        from paradex_py.environment import Environment
        TESTNET = "testnet"
        PROD = "prod"
    except:
        TESTNET = "testnet"
        PROD = "prod"


def generate_wallet():
    """Generate new Ethereum wallet"""
    private_key = "0x" + secrets.token_hex(32)
    address = Account.from_key(private_key).address
    
    print("="*70)
    print("NEW TEST WALLET GENERATED")
    print("="*70)
    print(f"\nPrivate Key: {private_key}")
    print(f"Address: {address}")
    print("\n⚠️  Copy the private key and paste it in config.py")
    print("="*70)
    
    return private_key, address


def fetch_klines(private_key, market, days, resolution, use_testnet=True):
    """Fetch klines from Paradex API"""
    # Use string-based environment
    env = TESTNET if use_testnet else PROD
    env_name = "TESTNET" if use_testnet else "MAINNET"
    
    print(f"\n🔄 Fetching {days} days of {resolution}-min data from Paradex {env_name}...")
    
    try:
        paradex = Paradex(env=env, l1_private_key=private_key)
        
        end_time = int(datetime.now().timestamp() * 1000)
        start_time = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
        
        # Use correct parameter names: symbol, resolution, start_at, end_at
        result = paradex.api_client.fetch_klines(
            symbol=market,
            resolution=str(resolution),
            start_at=start_time,
            end_at=end_time
        )
        
        # Check what columns we actually have
        if isinstance(result, list) and len(result) > 0:
            df = pd.DataFrame(result)
        elif isinstance(result, dict) and 'results' in result:
            df = pd.DataFrame(result['results'])
        else:
            df = pd.DataFrame(result)
        
        print(f"Available columns: {df.columns.tolist()}")
        print(f"First row sample: {df.iloc[0].tolist() if len(df) > 0 else 'No data'}")
        
        # If columns are numeric, it means data is array format [time, open, high, low, close, volume]
        if df.columns.tolist() == [0, 1, 2, 3, 4, 5]:
            df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            df['start_time'] = pd.to_datetime(df['timestamp'].astype(int), unit='ms')
        else:
            # Map columns - check what they're actually called
            time_col = None
            for col in ['start_time', 'time', 'timestamp', 't', 'start_at']:
                if col in df.columns:
                    time_col = col
                    break
            
            if time_col:
                df['start_time'] = pd.to_datetime(df[time_col].astype(int), unit='ms')
        
        # Convert OHLCV columns to float
        for col in ['open', 'high', 'low', 'close', 'volume']:
            if col in df.columns:
                df[col] = df[col].astype(float)
        
        print(f"✅ Fetched {len(df)} data points")
        return df
        
    except Exception as e:
        print(f"❌ Paradex API Error: {e}")
        raise