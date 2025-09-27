"""Paradex API Client"""

import secrets
import pandas as pd
from datetime import datetime, timedelta
from eth_account import Account
from paradex_py import Paradex
from paradex_py.environment import Environment


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
    env = Environment.TESTNET if use_testnet else Environment.PROD
    env_name = "TESTNET" if use_testnet else "MAINNET"
    
    print(f"\n🔄 Fetching {days} days of {resolution}-min data from Paradex {env_name}...")
    
    try:
        paradex = Paradex(env=env, l1_private_key=private_key)
        
        end_time = int(datetime.now().timestamp() * 1000)
        start_time = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
        
        result = paradex.api_client.fetch_klines(
            market=market,
            resolution=str(resolution),
            start_unix_ms=start_time,
            end_unix_ms=end_time
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