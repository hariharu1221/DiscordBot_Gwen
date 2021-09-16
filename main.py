import datetime
import os

import discord
from discord.ext import commands

from classes.user import User
from config import Config
from utils import logger


class GwenBot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=Config.prefixes,  # 봇을 불러올 접두사 설정
            help_command=None
        )

        # Cogs 로드
        cog_list = [i[:-3] for i in os.listdir('cogs') if i.endswith('.py') and i != '__init__.py']
        for i in cog_list:
            self.load_extension(f"cogs.{i}")

    async def on_ready(self):  # 봇이 구동되면 실행
        logger.info('======================')
        logger.info('< 구동 완료 >')
        logger.info('======================')

        await self.change_presence(
            status=discord.Status.online,  # 상태 설정
            activity=discord.Game(name=Config.activity))  # 하고 있는 게임으로 표시되는 것 설정

    def run(self):
        super().run(Config().using_token(), reconnect=True)

gwenbot = GwenBot()
gwenbot.run()
