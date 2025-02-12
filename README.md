# Blackjack Bot by Brendan Malaugh

## Overview
This project is a Blackjack bot that interacts with an online game using `mitmproxy` to intercept traffic and `listener.py` to process the game data.

## Installation & Setup

### 1. Install `mitmproxy`
Follow the official installation guide: [mitmproxy.org](https://mitmproxy.org/)

You may need to run your IDE **"As Administrator"** for `mitmproxy` to work correctly.

### 2. Adjust Target URL (as needed)
Modify TARGET_URL in line 6 of listener.py to end in =6223 if playing with SC, and =6227 if playing with GC.

### 3. Run the Bot

```bash
mitmproxy --mode transparent --script listener.py
python main.py
