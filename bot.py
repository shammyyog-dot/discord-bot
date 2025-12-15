import os
import random
import logging
import sqlite3
from contextlib import closing

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DB_PATH = os.getenv("BALANCE_DB", "balances.db")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord_bot")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def init_db(path: str = DB_PATH):
    with closing(sqlite3.connect(path)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS balances (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER NOT NULL
            )
            """
        )
        conn.commit()


def get_balance(user_id: int) -> int:
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.execute("SELECT balance FROM balances WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        return row[0] if row else 0


def set_balance(user_id: int, amount: int) -> None:
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            "INSERT INTO balances(user_id, balance) VALUES(?, ?) ON CONFLICT(user_id) DO UPDATE SET balance=excluded.balance",
            (user_id, amount),
        )
        conn.commit()


def add_balance(user_id: int, delta: int) -> int:
    current = get_balance(user_id)
    new = max(0, current + delta)
    set_balance(user_id, new)
    return new


@bot.event
async def on_ready():
    logger.info("Bot online as %s", bot.user)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send("❌ Missing arguments for command")
    if isinstance(error, commands.BadArgument):
        return await ctx.send("❌ Invalid argument type")
    if isinstance(error, commands.MissingRole):
        return await ctx.send("❌ Banker only")
    logger.exception(error)
    await ctx.send("❌ An unexpected error occurred")


@bot.command()
async def balance(ctx):
    bal = get_balance(ctx.author.id)
    await ctx.send(f"💰 Balance: ${bal:,}")


@bot.command()
@commands.has_role("Banker")
async def deposit(ctx, member: discord.Member, amount: int):
    if amount <= 0:
        return await ctx.send("❌ Amount must be positive")
    new = add_balance(member.id, amount)
    await ctx.send(f"✅ Deposited ${amount:,} to {member.display_name}. New balance: ${new:,}")


def win(probability: float = 0.40) -> bool:
    return random.random() <= probability


async def play_game(ctx, bet: int, name: str, win_chance: float = 0.40, payout: float = 2.0):
    if bet <= 0:
        return await ctx.send("❌ Bet must be a positive integer")
    bal = get_balance(ctx.author.id)
    if bet > bal:
        return await ctx.send("❌ Not enough money")
    # Deduct bet
    add_balance(ctx.author.id, -bet)
    if win(win_chance):
        winnings = int(bet * payout)
        add_balance(ctx.author.id, winnings)
        await ctx.send(f"🎉 {name} — {ctx.author.display_name} WIN! +${winnings:,}")
    else:
        await ctx.send(f"💥 {name} — {ctx.author.display_name} LOSS — -${bet:,}")


@bot.command()
async def mines(ctx, bet: int):
    await play_game(ctx, bet, "Mines")


@bot.command()
async def blackjack(ctx, bet: int):
    await play_game(ctx, bet, "Blackjack")


@bot.command()
async def roulette(ctx, bet: int):
    await play_game(ctx, bet, "Roulette")


@bot.command()
async def crash(ctx, bet: int):
    await play_game(ctx, bet, "Crash")


if __name__ == "__main__":
    if not TOKEN:
        logger.error("DISCORD_TOKEN is not set. Copy .env.sample to .env and add your token.")
        raise SystemExit(1)
    init_db()
    bot.run(TOKEN)
