# <---BIBLIOTECA--->
import discord
from discord.ext import commands
import random
import re

# <---VARIÁVEIS--->

# setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

# <---EVENTOS--->

# inicialização
@bot.event
async def onReady():
    print(f"Conectado como {bot.user.name}")

# comando de oi
@bot.command(name="hello")
async def hello(ctx):
    user = ctx.author.mention
    await ctx.send(f"👋 Salve, {user}! Bão? nega nega nega")

# comando de rolar dados
@bot.command(name="roll")
async def roll(ctx, dado: str):
    try:
        match = re.match(r"(\d+)d(\d+)([+\-*/]\d+)?", dado.lower())
        if not match:
            raise ValueError("Formato inválido. Use o formato `XdY+Z`, `XdY-Z`, `XdY*Z` ou `XdY/Z`.")

      
        num_dado = int(match.group(1))
        tam_dado = int(match.group(2))
        modificador = match.group(3)  

 
        if num_dado <= 0 or tam_dado <= 0:
            raise ValueError("O número de dados e lados deve ser maior que 0.")

        rolls = [random.randint(1, tam_dado) for _ in range(num_dado)]
        total = sum(rolls)

        if modificador:
            operador = modificador[0]  
            valor = int(modificador[1:])  
            if operador == "+":
                total += valor
            elif operador == "-":
                total -= valor
            elif operador == "*":
                total *= valor
            elif operador == "/":
                total //= valor 

        user = ctx.author.mention

        await ctx.send(
            f"**Rolagem de dados para {user}:**\n"
            f"🎲 Dados rolados: `{rolls}`\n"
            f"✨ Modificador: `{modificador or ' '}`\n"
            f"🔥 **Total:** `{total}`"
        )
    except Exception as e:
        await ctx.send(f"⚠️ **Erro:** {e}")

# <---RODAR BOT--->
bot.run("")
