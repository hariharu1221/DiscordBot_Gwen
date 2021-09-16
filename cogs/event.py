# 필수 임포트
from discord.ext import commands
import discord
import os
from utils import logger

# 부가 임포트
from utils import util_box
import openpyxl
import random
random.random()


class EventCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # 접두사에 관계없이 누군가가 메시지를 올렸을 때 여기가 실행될 거야
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:  # 봇이 말한 건 무시
            return

        logger.msg(message)  # 메시지를 기록

        if message.content.endswith("바보"):
            await message.channel.send('바보')  # 바보 아니라고 답변

        #배운거 답변
        if message.content.startswith("그웬아") or message.content.startswith("!"):
            word = message.content.split(" ")
            wb = openpyxl.load_workbook("memory.xlsx")
            ws = wb.active

            for i in range(1, 10):
                if ws["A" + str(i)].value == word[1]:
                    await message.channel.send(ws["B" + str(i)].value)
                    break

    # 누가 서버에 들어오면 여기가 실행될 거야
    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

    # 누가 서버에서 나가면 여기가 실행될 거야
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        pass

    # 이 봇이 어떤 서버에 초대되면 여기가 실행될 거야
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logger.info(f"{guild.name} 서버에 들어갔어!")

    # 이 봇이 어떤 서버에 쫓겨나면 여기가 실행될 거야
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        logger.info(f"{guild.name} 서버에서 쫓겨났어...")

    # 누군가가 메시지를 삭제하면 여기가 실행될 거야
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        logger.info(f"{message.author.name}이(가) '{message.content}' 메시지를 삭제")

    # 누군가가 메시지를 수정하면 여기가 실행될 거야 before와 after 모두 message야.
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        logger.info(f"{before.author.name}이(가) '{before.content}' 메시지를 '{after.content}' 로 수정")

    # 오류 발생 시 여기가 실행될 거야
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.errors.Forbidden):  # 권한 부족 오류
            try:
                return await ctx.send('내 권한이 부족해.. ㅠㅠ')
            except discord.errors.Forbidden:  # 여기는 봇이 볼 수는 있지만 메시지를 쓸 수 조차 없는 경우야
                return logger.warn('채팅 권한 없음')

        elif isinstance(error, commands.errors.CommandNotFound):  # 해당하는 명령어가 없는 경우
            return await ctx.send('몰루, 히힛!')

        elif isinstance(error, commands.CommandOnCooldown):  # 명령어 쿨타임이 다 차지 않은 경우
            return await ctx.send(
                f'이 명령어는 {error.cooldown.rate}번 쓰면 {error.cooldown.per}초의 쿨타임이 생기는 명령어야!'
                f'``cs\n{int(error.retry_after)}초 남았어!``')

        await ctx.send(f'오류가 발생했어...\n`{str(error)}`')
        logger.err(error)


def setup(bot):
    logger.info(f'{os.path.abspath(__file__)} 로드 완료')
    bot.add_cog(EventCog(bot))
