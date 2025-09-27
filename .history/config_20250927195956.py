"""Configuration for Paradex Bollinger Bands Calculator"""

# API Configuration
PRIVATE_KEY = ""  # Paste your private key here after generating
USE_TESTNET = True  # True = Safe testnet, False = Real mainnet

# Trading Parameters
MARKET = 'BTC-USD-PERP'
DAYS = 30
RESOLUTION = 1  # Minutes: 1, 3, 5, 15, 30, 60

# Bollinger Bands Parameters
BB_PERIOD = 20
BB_STD_DEV = 2

# Visualization
CHART_POINTS = 1000
SAVE_CSV = True
SAVE_CHART = True