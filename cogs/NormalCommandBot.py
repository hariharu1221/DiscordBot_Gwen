# 필수 임포트
from discord.ext import commands
import discord
import os
from utils import logger

# 부가 임포트
from utils import util_box
import random
random.random()


class normalCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def 안녕(self, ctx):
        await ctx.send(f'안녕 {ctx.author.name}!')

    @commands.command()
    async def 잡담(self, ctx):
        act = random.randrange(1,5)
        if act == 1:      await ctx.send(f'어, 절벽 너머에 있는 저건... 산인가? 꼭 한번 가까이 가서 보고 싶었어.')
        elif act == 2:    await ctx.send(f'그분이 이 가위로 내 드레스를 만드시던 기억이 생생해. 지금은 이걸로 다른 걸 자르지만.')
        elif act == 3:    await ctx.send(f'신성한 안개는 그 이름보다 느낌이 훨씬 더 중요해. 무엇도 날 해칠 수 없을 것처럼 따스한 보호를 받는 기분이거든.')
        elif act == 4:    await ctx.send(f'이곳에선 다들 투지가 넘친다니까. 그러니까 나도 최선을 다해야겠지.')
        else:             await ctx.send(f'천 조각은 아름다운 모습으로 변할 수 있어. 그게 바로 내가 하는 일이지.')

    @commands.cooldown(1, 10)
    @commands.command()
    async def 그웬식(self, ctx, arg1):
            if arg1 == "가위바위보":
                window = await ctx.send('가위바위보??')
            else:
                return
            result = await util_box.wait_for_reaction(self.bot, ctx.message, ['✋', '✌️', '✊'], 10, ctx)
            if not result:
                await ctx.message.clear_reactions()
                return
            elif result.emoji == '✋':
                await ctx.message.clear_reactions()
                result = 1
            elif result.emoji == '✌️':
                await ctx.message.clear_reactions()
                result = 2
            else:
                await ctx.message.clear_reactions()
                result = 3
            rand = random.randrange(1,6)
            if rand == 2 or rand > 3:
                st = f'{ctx.author.name}, 넌 졌어!'
                rt = '🦴 vs ✌️'
            elif result == 1:
                st = f'{ctx.author.name}, 넌 비겼어!' if rand == 1 else f'{ctx.author.name}, 넌 이겼어' if rand == 3 else f'{ctx.author.name}, 넌 졌어'
                rt = '✋ vs ✋' if rand == 1 else '✋ vs ✊' if rand == 3 else '✋ vs ✌️'
            elif result == 2:
                st = f'{ctx.author.name}, 넌 비겼어!' if rand == 2 else f'{ctx.author.name}, 넌 이겼어' if rand == 1 else f'{ctx.author.name}, 넌 졌어'
                rt = '✌️ vs ✌️' if rand == 2 else '✌️ vs ✋' if rand == 1 else '✌️ vs ✊'
            elif result == 3:
                st = f'{ctx.author.name}, 넌 비겼어!' if rand == 3 else f'{ctx.author.name}, 넌 이겼어' if rand == 2 else f'{ctx.author.name}, 넌 졌어'
                rt = '✊ vs ✊' if rand == 3 else '✊ vs ✌️' if rand == 2 else '✊ vs ✋'
            embed = discord.Embed(title='가위바위보', description='음....', colour=0x1DDB16)
            embed.add_field(name='결과', value=st, inline=True)
            embed.add_field(name='상태', value=rt, inline=True)
            if rand == 2 or rand > 3:   
                r = random.randrange(1,5)
                if r== 1:   embed.set_footer(text="`너무 재밌어!`")
                if r== 2:   embed.set_footer(text="`재단사 필요해?`")
                if r== 3:   embed.set_footer(text="`하, 이 상쾌하고도 신선한 공기!`")
                if r== 4:   embed.set_footer(text="`어, 이런. 어쩌지?`")
                if r== 5:   embed.set_footer(text="`하! 바위가 가위를 이긴다고?`")
            else: embed.set_footer(text="가위바위보")
            await window.delete()
            await ctx.send(embed=embed)

    @commands.cooldown(1, 10)
    @commands.command()
    async def 가위바위보(self, ctx):
        window = await ctx.send('가위바위보??')
        result = await util_box.wait_for_reaction(self.bot, ctx.message, ['✋', '✌️', '✊'], 10, ctx)
        if not result:
            await ctx.message.clear_reactions()
            return
        elif result.emoji == '✋':
            await ctx.message.clear_reactions()
            result = 1
        elif result.emoji == '✌️':
            await ctx.message.clear_reactions()
            result = 2
        else:
            await ctx.message.clear_reactions()
            result = 3
        rand = random.randrange(1,3)
        
        if result == 1:
            st = f'{ctx.author.name}, 넌 비겼어!' if rand == 1 else f'{ctx.author.name}, 넌 이겼어' if rand == 3 else f'{ctx.author.name}, 넌 졌어'
            rt = '✋ vs ✋' if rand == 1 else '✋ vs ✊' if rand == 3 else '✋ vs ✌️'
        if result == 2:
            st = f'{ctx.author.name}, 넌 비겼어!' if rand == 2 else f'{ctx.author.name}, 넌 이겼어' if rand == 1 else f'{ctx.author.name}, 넌 졌어'
            rt = '✌️ vs ✌️' if rand == 2 else '✌️ vs ✋' if rand == 1 else '✌️ vs ✊'
        if result == 3:
            st = f'{ctx.author.name}, 넌 비겼어!' if rand == 3 else f'{ctx.author.name}, 넌 이겼어' if rand == 2 else f'{ctx.author.name}, 넌 졌어'
            rt = '✊ vs ✊' if rand == 3 else '✊ vs ✌️' if rand == 2 else '✊ vs ✋'
            
        embed = discord.Embed(title='가위바위보', description='음....', colour=0x1DDB16)
        embed.add_field(name='결과', value=st, inline=True)
        embed.add_field(name='상태', value=rt, inline=True)
        embed.set_footer(text="가위바위보")
        await window.delete()
        await ctx.send(embed=embed)

    @commands.command()
    async def 발사(self, ctx, arg1=None, arg2=None):
        if arg1 is None or arg2 is None:
            return await ctx.send('뭘 누구한테 발사해야 해?')

        await ctx.send(f'`{arg1}`에 `{arg2}`를 발사! 퍼퍼벙')

    # 따라말하는
    @commands.command()
    async def 말해(self, ctx, *, content=None):
        if content is None:
            return await ctx.send('뭘 말해?')

        await ctx.message.delete()  # 유저가 쓴 메시지는 지웁니다.
        await ctx.send(f'{ctx.author.name}님이 전해달래! : ' + content)

    # 핑
    @commands.command()
    async def 핑(self, ctx):
        await ctx.send(f'`지연 시간 : {int(self.bot.latency * 1000)}ms`')

    #embed
    @commands.command()
    async def 프로필(self, ctx):
        embed = discord.Embed(title='네 정보야', description='음....', colour=0x1DDB16)
        embed.add_field(name='네 이름', value=ctx.author.name, inline=True)
        embed.add_field(name='네 디스코드 ID', value=ctx.author.id, inline=True)
        embed.add_field(name='여기 채널 이름', value=ctx.channel.name, inline=True)
        embed.add_field(name='여기 채널 ID', value=ctx.channel.id, inline=True)
        embed.set_footer(text="히히네이스")
        await ctx.send(embed=embed)

    @commands.command()
    async def DM(self, ctx):
        if ctx.author.dm_channel:
            await ctx.author.dm_channel.send("DM")
        elif ctx.author.dm_channel is None:
            channel = await ctx.author.create_dm()
            await channel.send("DM 생성")



def setup(bot):
    logger.info(f'{os.path.abspath(__file__)} 로드 완료')
    bot.add_cog(normalCommand(bot)) 
