# <---BIBLIOTECA--->
import discord
from discord.ext import commands
import random
import re
import pandas as pd
# dicionário portugues para pegar 3 palavras e soltar a boa
# pesquisador de nome de música aleatoria para dar ideia de nome de stand

# <---VARIÁVEIS--->
pericias = {
    "fisico": ["Atletismo ", "Fôlego ", "Resistência Física"],
    "agilidade": ["Prestidigitação ", "Acrobacia ", "Pickpocket ", "Quick Draw"],
    "precisao": ["Furtividade ", "Desenhar ", "Dançar ", "Mirar ", "Desviar "],
    "inteligencia": ["Concentração ", "Religião ", "História ", "Lidar com Máquinas ", "Intuição ", "Aprender"],
    "sabedoria": ["Medicina", "Lidar com Animais", "Percepção", "Natureza", "Ensinar"],
    "carisma": ["Atuação ", "Mentir ", "Intimidação ", "Sedução ", "Diplomacia ", "JISM(i) "],
    "sorte": ["Jogar"]
}

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

# comando mostar modificador
@bot.command(name="mod")
async def mod(ctx):
    await ctx.send(
        f"# Modificadores\n"
        f"**ATRIBUTOS\n**"
        f"• A: +25\n"
        f"• B: +20\n"
        f"• C: +15\n"
        f"• D: +10\n"
        f"• E: +5\n"
        f"• ∅: 0\n\n"
        f"**PERÍCIAS**\n"
        f"• Todas as perícias adicionam um bônus de +3 ao atributo correspondente quando rolado.\n\n"
        f"**SUPER ATRIBUTOS**\n"
        f"• Concedem um bônus de **+3** ao atributo\n"
        f"• Em caso de empate, quem possui um **Super Atributo** é considerado o vencedor.\n\n"
        f"**HÍPER ATRIBUTOS**\n"
        f"• Concedem um bônus adicional de +5 ao atributo.\n"
        f"• Em caso de empate com um Super Atributo, o Híper Atributo é o vencedor.\n"
        f"• Caso a disputa seja entre um **Híper Atributo** e um atributo comum (sem modificadores especiais), o **Híper Atributo** vence automaticamente."   
    )

# comando para mostrar pericias
@bot.command(name="pericias")
async def pericias_command(ctx, atributo: str = None):
    if not atributo:
        await ctx.send(
            "Por favor, digite `$pericias <atributo>` para listar as perícias.\n"
            "Atributos disponíveis:\n"
            "- 🐒 geral\n"
            "- 🦾 fisico\n"
            "- 💨 agilidade\n"
            "- 🎯 precisao\n"
            "- 🤓 inteligencia\n"
            "- 🧙‍♂️ sabedoria\n"
            "- 👳‍♂️ carisma\n"
            "- 😎 sorte"
        )
        return

    user = ctx.author.mention

    if atributo.lower() == "geral":
        todas_pericias = "\n".join(
            [f"**{chave.capitalize()}**: {', '.join(valores)}" for chave, valores in pericias.items()]
        )
        await ctx.send(f"{user} Aqui estão todas as perícias:\n\n{todas_pericias}")

    elif atributo.lower() in pericias:
        lista_pericias = ", ".join(pericias[atributo.lower()])
        await ctx.send(f"{user} As perícias de **{atributo.capitalize()}** são:\n{lista_pericias}")
    else:

        await ctx.send(
            f"{user} Atributo não existe. Escolha um dos seguintes:\n"
            "- geral\n"
            "- fisico\n"
            "- agilidade\n"
            "- precisao\n"
            "- inteligencia\n"
            "- sabedoria\n"
            "- carisma\n"
            "- sorte"
        )


# comando de rolar stand
@bot.command(name="stand")
async def stand(ctx):
    user = ctx.author.mention

    try:
        # Lendo os nomes dos stands
        with open('stands.txt', 'r', encoding='utf-8') as arquivo_stand:
            stands = arquivo_stand.read().split(", ")
            stand_sorteado = random.choice(stands).strip()

        # Tentando encontrar a descrição do stand sorteado
        try:
            with open('descricao.txt', 'r', encoding='utf-8') as arquivo_descricao:
                descricao = arquivo_descricao.read()

                stand_inicio = descricao.find(stand_sorteado)
                if stand_inicio == -1:
                    descricao_final = "Descrição não encontrada."
                else:
                    stand_fim = descricao.find('\n\n', stand_inicio + len(stand_sorteado))
                    if stand_fim == -1:
                        stand_fim = len(descricao)
                    descricao_final = descricao[stand_inicio:stand_fim].strip()
        except FileNotFoundError:
            descricao_final = "Arquivo de descrição não encontrado."
        except Exception as e:
            descricao_final = f"Erro ao buscar descrição: {e}"

        # Enviando a mensagem com o stand sorteado e a descrição
        await ctx.send(
            f"⭐ Seu espírito evoluiu, sua mente e seu corpo se fortaleceram.\n"
            f"{user} acaba de despertar 🔥: \n"
            f"**『{stand_sorteado}』** 💋\n"
            f"📝 Descrição: \n```\n{descricao_final}\n```"
        )
    except FileNotFoundError:
        await ctx.send(f"⚠️ **Erro:** Arquivo de stands não encontrado.")
    except Exception as e:
        await ctx.send(f"⚠️ **Erro inesperado:** {e}")

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