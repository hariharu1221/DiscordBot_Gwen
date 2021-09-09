# 필수 임포트
from discord.ext import commands
import discord
import os
from utils import logger

# 부가 임포트
from utils import util_box
from bs4 import BeautifulSoup
from info import Champion
import random
import requests
random.random()

class searchCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def 전적(self, ctx, arg1=None):
        if arg1 is None:
            return await ctx.send('닉네임이 적혀있지 않아..')
        baseurl = "https://kr.op.gg/summoner/userName="
        url = baseurl + arg1
        res = requests.get(url).text
        soup = BeautifulSoup(res, "html.parser")

        # 래더 랭킹 가져오기
        try:
            price = soup.find("span", attrs={"class":"ranking"}).get_text().strip()
        except:
            return await ctx.send('존재하지 않는 소환사야..')

        # 사용자 이미지 가져오기
        proimg = soup.find("div", attrs={"class":"ProfileIcon"}).find("img").get("src")

        # 티어 이미지 가져오기
        img = soup.find("div", attrs={"class":"SummonerRatingMedium"}).find("img").get('src')

        # 티어, 티어별명 가져오기 (text)
        tiername = soup.find("div", attrs={"class":"TierRank"}).get_text()
        tieraka = soup.find("div", attrs={"class":"LeagueName"}).get_text().strip()

        # LP 가져오기
        userlp = soup.find("span", attrs={"class":"LeaguePoints"}).get_text().strip()

        # 승, 패 , 승률 가져오기
        win = soup.find("span", attrs={"class":"wins"}).get_text().replace("W", "승")
        lose = soup.find("span", attrs={"class":"losses"}).get_text().replace("L", "패")
        odds = soup.find("span", attrs={"class":"winratio"}).get_text()

        # 모스트 챔피언 가져오기
        mostchamp = soup.find_all("div", attrs={"class":"ChampionBox Ranked"}, limit=3)
        mostchamp_list = []
        for most in mostchamp:
            mostchamp_list.append(most.find('div').get('title'))

        embed = discord.Embed(title=arg1 + " 님의 플레이어 정보", description="", color=0x62c1cc)
        embed.set_thumbnail(url="http:" + img)
        embed.set_image(url="http:" + proimg)


        embed.add_field(name="래더 랭킹", value="`" + price + " 위 " + "`",inline = False)
        embed.add_field(name="티어 정보", value="`" + userlp + " | " + tiername + " | " + tieraka + "`", inline=False)
        embed.add_field(name="모스트 챔피언", value="`" + mostchamp_list[0] + ", " + mostchamp_list[1] + ", " + mostchamp_list[2] + "`", inline=False)
        embed.add_field(name="승, 패, 승률", value="`" + win + " " + lose + " | " + odds + "`", inline=False)

        embed.set_footer(text="솔로랭크 기준 티어입니다. | 랭크 정보가 없을 시 출력되지 않습니다.")
        await ctx.send(embed=embed)

    @commands.command()
    async def 챔피언(self, ctx, arg1=None):
        if arg1 is None:    return await ctx.send('챔피언의 이름이 적혀있지 않아..')
        try:    champ = Champion.champion[arg1]
        except: return await ctx.send('존재하지 않는 챔피언 이름이야')

        url = "https://www.op.gg/champion/" + champ
        res = requests.get(url).text
        soup = BeautifulSoup(res, "html.parser")

        #챔피언 이미지
        chamPro = soup.find("div", attrs={"class":"champion-stats-header-info__image"}).find("img").get("src")
        spell = soup.find_all("li", attrs={"class":"champion-stats__list__item"}, limit=2)
        spell_list = []
        for most in spell:
            spell_list.append(most.find('img').get('src'))


        embed = discord.Embed(title=arg1 + " 의 챔피언 정보", description="", color=0x62c1cc)
        embed.set_thumbnail(url="http:" + chamPro)
        embed.set_image(url="http:" + spell_list[0])
        embed.set_image(url="http:" + spell_list[1])
        await ctx.send(embed=embed)

        '''


        embed.add_field(name="래더 랭킹", value="`" + price + " 위 " + "`",inline = False)
        embed.add_field(name="티어 정보", value="`" + userlp + " | " + tiername + " | " + tieraka + "`", inline=False)
        embed.add_field(name="모스트 챔피언", value="`" + mostchamp_list[0] + ", " + mostchamp_list[1] + ", " + mostchamp_list[2] + "`", inline=False)
        embed.add_field(name="승, 패, 승률", value="`" + win + " " + lose + " | " + odds + "`", inline=False)

        embed.set_footer(text="솔로랭크 기준 티어입니다. | 랭크 정보가 없을 시 출력되지 않습니다.")
        '''

    @commands.command()
    async def 챔피언라인(self, ctx, arg1=None, arg2=None):
        if arg1 is None:
            return await ctx.send('챔피언의 이름이 적혀있지 않아..')
        if arg2 is None:
            return await ctx.send('라인을 입력해줘!')
        url = "https://www.op.gg/champion/" + arg1 + "/statistics/" + arg2 + "/build"
        res = requests.get(url).text
        soup = BeautifulSoup(res, "html.parser")

def setup(bot):
    logger.info(f'{os.path.abspath(__file__)} 로드 완료')
    bot.add_cog(searchCommand(bot)) 