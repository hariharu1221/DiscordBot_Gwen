import asyncio
import random


async def ox(bot, message, ctx):
    result = await wait_for_reaction(bot, message, ['๐พ๏ธ', 'โ'], 10, ctx)
    if not result:
        await message.clear_reactions()
        return 2
    elif result.emoji == 'โ':
        await message.clear_reactions()
        return False
    else:
        await message.clear_reactions()
        return True


async def wait_for_reaction(bot, window, canpress, timeout, ctx, event='reaction_add', add_react=True):
    '''์ง์ ํ ์ด๋ชจ์ง๊ฐ ๋๋ฆด ๋๊น์ง ๊ธฐ๋ค๋ฆฐ ํ ๋๋ฆผ ์ฌ๋ถ์ ๋ฐ๋ผ Bool ๋ฐฉ์ ๋ฐํ
    - ์๊ฐ ์ด๊ณผ๋ False ๋ฐํ'''
    if add_react:
        for i in list(canpress):
            await window.add_reaction(i)

    def check(reaction, user):
        if user == ctx.author and str(reaction.emoji) in canpress and reaction.message.id == window.id:
            return True
        else:
            return False

    try:
        reaction = await bot.wait_for(event, timeout=timeout, check=check)

    except asyncio.TimeoutError:
        return False

    else:
        return reaction[0]


async def wait_for_saying(bot, timeout, ctx, keyword='', user=None):
    if user is None:
        for_user = ctx.author
    else:
        for_user = user

    def check(m):
        if m.author == for_user and keyword in m.content:
            return True
        else:
            return False

    try:
        msg = await bot.wait_for('message', timeout=timeout, check=check)

    except asyncio.TimeoutError:
        return False

    else:
        return msg


def rdpc(percentage):
    '''RanDom PerCents
    ํผ์ผํธ๋ฅผ ๋ฃ์ผ๋ฉด ๊ทธ ํ๋ฅ ๋ก Bool ๋ฑ์'''
    F = random.randrange(1, 101)
    if F <= percentage:
        return True
    else:
        return False
