import datetime
import discord
import os
from discord.ext import commands
from utils import logger
from config import Config
from classes.user import User



class adminCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='')
    async def restart(self, ctx):
        if ctx.author.id not in Config.admin:
            return await ctx.send(
                '관리자 명령어'
                '\n`사용불가`')

        w = await ctx.send("``나갔다 올게~``")
        cog_list = [i[:-3] for i in os.listdir('cogs') if i.endswith('.py') and i != '__init__.py']
        for i in cog_list:
            self.bot.reload_extension(f"cogs.{i}")
            logger.info(f"'{i}' reload complete")

        await w.edit(content="``다시 왔어!``")

    @commands.command()
    async def exec(self, ctx, *args):
        if ctx.author.id not in Config.admin:
            return await ctx.send(
                '관리자 명령어'
                '\n`사용불가`')

        text = ' '.join(args)
        me = User(ctx.author)
        logger.info(f'{me.name}이(가) exec 명령어 사용 : {text}')
        try:
            exec(text)
        except Exception as e:
            embed = discord.Embed(
                color=0x980000,
                timestamp=datetime.datetime.today())
            embed.add_field(
                name="🐣  **Cracked!**",
                value=f"```css\n[입구] {text}\n[오류] {e}```",
                inline=False)
            logger.err(e)
        else:
            embed = discord.Embed(
                color=0x00a495,
                timestamp=datetime.datetime.today())
            embed.add_field(
                name="🥚  **Exec**",
                value=f"```css\n[입구] {text}```",
                inline=False)
        embed.set_footer(
            text=f"{ctx.author.name} • exec",
            icon_url=str(ctx.author.avatar_url_as(static_format='png', size=128)))
        await ctx.send(embed=embed, reference=ctx.message)

    @commands.command()
    async def eval(self, ctx, *args):
        if ctx.author.id not in Config.admin:
            return await ctx.send(
                '관리자 명령어'
                '\n`사용 불가`')

        text = ' '.join(args)
        me = User(ctx.author)
        logger.info(f'{me.name}이(가) eval 명령어 사용 : {text}')
        try:
            result = eval(text)
        except Exception as e:
            embed = discord.Embed(
                color=0x980000,
                timestamp=datetime.datetime.today())
            embed.add_field(
                name="🐣  **Cracked!**",
                value=f"```css\n[입구] {text}\n[오류] {e}```",
                inline=False)
            logger.err(e)
        else:
            embed = discord.Embed(
                color=0x00a495,
                timestamp=datetime.datetime.today())
            embed.add_field(
                name="🥚  **Eval**",
                value=f"```css\n[입구] {text}\n[출구] {result}```",
                inline=False)
        embed.set_footer(
            text=f"{ctx.author.name} • eval",
            icon_url=str(ctx.author.avatar_url_as(static_format='png', size=128)))
        await ctx.send(embed=embed, reference=ctx.message)

def setup(bot):
    logger.info(f'{os.path.abspath(__file__)} 로드 완료')
    bot.add_cog(adminCommand(bot)) 