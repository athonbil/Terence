# <---BIBLIOTECA--->
import discord
from discord.ext import commands
import random
import re
import pandas as pd

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

# comando de rolar stand
@bot.command(name="stand")
async def stand(ctx):
    user = ctx.author.mention

    try:
        with open('stands.txt', 'r', encoding='utf-8') as arquivo_stand:
            stands = arquivo_stand.read().split(", ")
            stand_sorteado = random.choice(stands).strip()

            await ctx.send(
                f"⭐ Seu espírito evoluiu, sua mente e seu corpo se fortaleceram.\n"
                f"{user} acaba de despertar 🔥: \n"
                f"**『{stand_sorteado}』** 💋\n"
            )
    except FileNotFoundError:
        await ctx.send(f"⚠️ **Erro:** Arquivo não encontrado.")
    except Exception as e:
        await ctx.send(f"⚠️ **Erro:** {e}")

# comando de buscar descrição de stand
@bot.command(name="info")
async def stand_descricao(ctx, *, nome_stand: str):
    user = ctx.author.mention
    try:
        with open('descricao.txt', 'r', encoding='utf-8') as arquivo:
            descricao = arquivo.read()

            stand_inicio = descricao.find(nome_stand)
            if stand_inicio == -1:
                raise ValueError(f"Descrição de 『{nome_stand}』 não encontrada.")

            stand_fim = descricao.find('\n\n', stand_inicio + len(nome_stand))
            if stand_fim == -1:
                stand_fim = len(descricao)
            descricao_final = descricao[stand_inicio:stand_fim].strip()

            await ctx.send(
                f"⭐ {user}, aqui está a descrição de 『{nome_stand}』:\n"
                f"```\n{descricao_final}\n```"
            )
    except FileNotFoundError:
        await ctx.send(f"⚠️ **Erro:** Arquivo de descrição não encontrado.")
    except ValueError as e:
        await ctx.send(f"⚠️ **Erro:** {e}")
    except Exception as e:
        await ctx.send(f"⚠️ **Erro inesperado:** {e}")




# <---RODAR BOT--->
bot.run("")
