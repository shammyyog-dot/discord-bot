# discord-bot

Simple Discord gambling bot example with persistent balances.

Setup
-----

1. Copy `.env.sample` to `.env` and set `DISCORD_TOKEN`.
2. (Optional) Set `BALANCE_DB` in `.env` to change database file location.
3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run
----

```bash
python bot.py
```

Or use the helper script which bootstraps a venv and installs dependencies:

```bash
./run.sh
```

Commands
--------

- `!balance` — show your balance
- `!deposit @user <amount>` — banker-only command to add money to a user
- `!mines <bet>`, `!blackjack <bet>`, `!roulette <bet>`, `!crash <bet>` — play games
