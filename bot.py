import os
import discord
from discord.ext import commands
import aiohttp
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print(f"✅ Conectado como {bot.user}")

@bot.command()
async def treecko(ctx, *, mensaje: str):
    """Habla con Treecko (adicto a la Pepsi)"""
    await ctx.trigger_typing()

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-oss-120b",
        "messages": [
            {"role": "system", "content": "Eres Treecko, un Pokémon simpático pero adicto a la Pepsi. Siempre respondes con humor y mencionas tu amor por la Pepsi de forma graciosa."},
            {"role": "user", "content": mensaje}
        ],
        "max_tokens": 200
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                reply = result["choices"][0]["message"]["content"]
                await ctx.send(reply)
            else:
                error_text = await response.text()
                await ctx.send(f"❌ Error en la API: {error_text}")

bot.run(DISCORD_TOKEN)
