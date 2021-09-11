# 필수 임포트
from typing import AsyncIterable
from discord.ext import commands
import discord
import os

from requests.models import to_native_string
from utils import logger

# 부가 임포트
from utils import util_box
from bs4 import BeautifulSoup
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from io import BytesIO
from info import Champion
import random
import requests
import asyncio
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
        except: return await ctx.send('존재하지 않는 챔피언 이름이야!')

        url = "https://www.op.gg/champion/" + champ
        res = requests.get(url).text
        soup = BeautifulSoup(res, "html.parser")

        #챔피언 승률, 픽률, 티어
        try:
            tier = soup.find("div", attrs={"class":"champion-stats-header-info__tier"}).get_text().strip()
        except:
            url = "https://www.op.gg/champion/" + champ + "/statistics/jungle/build"
            res = requests.get(url).text
            soup = BeautifulSoup(res, "html.parser")
            tier = ""
            await ctx.send('`표본이 부족한 챔피언이야..`')
        if tier == "":
            an = "R.I.P"
            profile = Image.open('imgs/0.png')
        elif tier[len(tier) - 1] == '5':
            an = "5티어"
            profile = Image.open('imgs/5.png')
        elif tier[len(tier) - 1] == '4':
            an = "4티어"
            profile = Image.open('imgs/4.png')
        elif tier[len(tier) - 1] == '3':
            an = "3티어"
            profile = Image.open('imgs/3.png')
        elif tier[len(tier) - 1] == '2':
            an = "2티어"
            profile = Image.open('imgs/2.png')
        elif tier[len(tier) - 1] == '1':
            an = "1티어"
            profile = Image.open('imgs/1.png')

        
        rate = soup.find_all("div", attrs={"class":"champion-stats-trend-rate"}, limit=2)
        rate_list = []
        for most in rate:
            rate_list.append(most.get_text())

        
        #챔피언 이미지
        chamPro = soup.find("div", attrs={"class":"champion-stats-header-info__image"}).find("img").get("src")
        #스펠 이미지
        spell = soup.find_all("li", attrs={"class":"champion-stats__list__item"}, limit=4)
        spell_list = []
        for most in spell:
            spell_list.append(most.find('img').get('src'))
        #스킬 이미지
        skill = soup.find_all("a", attrs={"class":"Image"}, limit=5)
        skill_list = []
        for most in skill:
            skill_list.append(most.find('img').get('src'))

        #이미지 생성
        Background = Image.new(mode="RGB", size=(900, 1500), color=(255, 255, 255))
        Background.paste(getImg(chamPro, 1000,1000).convert('RGB').filter(ImageFilter.GaussianBlur(30)), (-50, -200))

        Background.paste(Image.open('imgs/Background.png'),(0,520))
        Background.paste(profile,(300,300))
        Background.paste(getImg(chamPro, 250,250),(324,324))
        Background = getText(Background, arg1, 900, 600, fontsize = 100)

        Background = getText(Background, "승률", 380, 820, fontsize = 40)
        Background = getText(Background, rate_list[0], 310, 680, fontsize = 50)
        Background = getText(Background, "티어", 900, 820, fontsize = 40)
        Background = getText(Background, an, 900, 730, fontsize = 50)
        Background = getText(Background, "픽률", 1420, 820, fontsize = 40)
        Background = getText(Background, rate_list[1], 1350, 680, fontsize = 50)

        Background.paste(getImg(skill_list[0], 200,200), (-110, 914))
        Background.paste(getImg(skill_list[1], 200,200), (121, 914))
        Background.paste(getImg(skill_list[2], 200,200), (351, 914))
        Background.paste(getImg(skill_list[3], 200,200), (581, 914))
        Background.paste(getImg(skill_list[4], 200,200), (810, 914))

        Background.paste(getImg(spell_list[0], 100,100), (80, 1200))
        Background.paste(getImg(spell_list[1], 100,100), (280, 1200))
        Background.paste(getImg(spell_list[2], 100,100), (520, 1200))
        Background.paste(getImg(spell_list[3], 100,100), (720, 1200))

        with BytesIO() as image_binary:
        # 이미지를 BytesIO 스트림에 저장
            Background.save(image_binary, "png")
        # BytesIO 스트림의 0바이트(처음)로 이동
            image_binary.seek(0)
        # discord.File 인스턴스 생성
            out = discord.File(fp=image_binary, filename="info.png")
            Img = await ctx.send(file=out, reference=ctx.message)

        #룬
        window = await ctx.send('`이 챔피언의 룬을 보여줄까?`')
        result = await util_box.ox(self.bot, window, ctx)

        if result == 1:
            await window.edit(content='`룬 이미지 로드중...`')
        else:
            await window.edit(content='`룬은 보여주지 않을게!`')
            await asyncio.sleep(2.0)
            await window.delete()
            return
        
        #룬 이미지
        luneType = soup.find_all("div", attrs="perk-page__item perk-page__item--mark", limit=2)
        luneType_list = []
        for most in luneType:
            luneType_list.append(most.find('img').get('src'))

        lune = soup.find("div", attrs={"class":"perk-page__item perk-page__item--keystone perk-page__item--active"}).find("img").get("src")

        Background = Image.new(mode="RGB", size=(900, 1500), color=(255, 255, 255))
        Background.paste(getImg(luneType_list[0], 200,200), (200,100))
        Background.paste(getImg(luneType_list[1], 200,200), (650,100))
        Background.paste(getImg(lune, 200,200), (200,400))

        with BytesIO() as image_binary:
            Background.save(image_binary, "png")
            image_binary.seek(0)
            out = discord.File(fp=image_binary, filename="lune.png")
            await window.delete()
            await ctx.send(file=out)









def setup(bot):
    logger.info(f'{os.path.abspath(__file__)} 로드 완료')
    bot.add_cog(searchCommand(bot)) 

def getImg(url, x, y):
    res = requests.get("http:" + url).content
    im = Image.open(BytesIO(res))
    return im.resize((x, y))

def getText(Img, text, x, y, fontsize = 50, fonttype = 'font/Cafe24SsurroundAir.ttf'):
    selectedFont = ImageFont.truetype(fonttype, fontsize, encoding="UTF-8")
    draw = ImageDraw.Draw(Img)
    w, h = draw.textsize(text, selectedFont)
    draw.text(((x-w)/2,y),text,fill="white",font=selectedFont,align='center')
    return Img