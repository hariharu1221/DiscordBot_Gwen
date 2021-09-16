# 임포트 = include, using
import os
import discord
from discord.ext import commands
from utils import logger

class Bot(commands.AutoShardedBot): # 봇 클래스 선언 매개 변수로 디스코드 라이브러리에서 제공하는 변수 사용
    def __init__(self):          # init 함수
        super().__init__(
            command_prefix='#',  # 봇을 불러올 접두사 설정
            help_command=None
        )   
        cog_list = [i[:-3] for i in os.listdir('cogs') if i.endswith('.py') and i != '__init__.py'] # Cogs 로드
        for i in cog_list:
            self.load_extension(f"cogs.{i}")

    async def on_ready(self):    # 봇이 구동되면 실행
        logger.info('실행 완료')
        await self.change_presence(              # 봇의 정보를 설정해주는 디스코드 라이브러리 함수
            status=discord.Status.online,        # 상태 설정
            activity=discord.Game(name="코딩"))  # 하고 있는 게임으로 표시되는 것 설정 -> 코딩 하는중

    def run(self):
        super().run("복사한 토큰 값 붙여넣기", reconnect=True)

bot = Bot() #봇 클래스 받아옴
bot.run() #봇 실행
