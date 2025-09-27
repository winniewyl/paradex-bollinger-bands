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
        
        # Debug: check what parameters fetch_klines accepts
        import inspect
        sig = inspect.signature(paradex.api_client.fetch_klines)
        print(f"fetch_klines parameters: {sig}")
        
        end_time = int(datetime.now().timestamp() * 1000)
        start_time = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
        
        # Try calling with positional arguments
        result = paradex.api_client.fetch_klines(
            market,  # First positional argument
            str(resolution),
            start_time,
            end_time
        )
        
        df = pd.DataFrame(result['results'])
        df['start_time'] = pd.to_datetime(df['start_time'].astype(int), unit='ms')
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)
        
        print(f"✅ Fetched {len(df)} data points")
        return df
        
    except Exception as e:
        print(f"❌ Paradex API Error: {e}")
        raise