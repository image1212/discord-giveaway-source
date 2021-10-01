import discord
from discord.ext import commands
import asyncio
import random
import datetime
import os

# prefix = 접두사 ex. g!
client = commands.Bot(command_prefix = '^')

@client.event
async def on_ready():
    print('OK!')

@client.command()
async def helpme(ctx):
    ghelp = discord.Embed(color = 0x7289da)
    ghelp.set_author(name = 'Commands/Help', icon_url = '')
    ghelp.add_field(name= 'helpme', value = '지금 니가 보고있는거', inline = False)
    ghelp.add_field(name= 'giveaway', value = '이벤트설정', inline = False)
    ghelp.add_field(name= 'reroll `#channel_name` `message id`', value = '리롤', inline = False)
    await ctx.send(embed = ghelp)



@client.command()
@commands.has_role("Giveaway Host")     # 역할 Giveaway Host 만드세요 저부분에 다른 역할 이름 넣어도 됩니다 
async def giveaway(ctx):
    giveaway_questions = ['이벤트채널어디야', '경품뭐야', '얼마뒤에 뽑히게할거냐',]
    giveaway_answers = []
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    for question in giveaway_questions:
        await ctx.send(question)
        try:
            message = await client.wait_for('message', timeout= 30.0, check= check)
        except asyncio.TimeoutError:
            await ctx.send('당신은 제 시간에 대답하지 않았습니다. 다시 시도하고 질문 후 30초 이내에 답을 보내주십시오.')
            return
        else:
            giveaway_answers.append(message.content)
    try:
        c_id = int(giveaway_answers[0][2:-1])
    except:
        await ctx.send(f'채널을 올바르게 언급하지 안았습니다. 다음과 같이 하십시오.: {ctx.channel.mention}')
        return
    
    channel = client.get_channel(c_id)
    prize = str(giveaway_answers[1])
    time = int(giveaway_answers[2])

    await ctx.send(f' {prize} 이벤트 시작\n 빨리참여 기억기억 {channel.mention}, 끝나는 시간 : {time} 초')
    give = discord.Embed(color = 0x2ecc71)
    give.set_author(name = f'이벤트 시작!', icon_url = 'https://i.imgur.com/VaX0pfM.png')
    give.add_field(name= f'호스트 : {ctx.author.name} \n 경품: {prize}!', value = f'아래에 🎉 이모지를 클릭해주세요!\n 끝나는시간 : {round(time/60, 2)} 분', inline = False)
    end = datetime.datetime.utcnow() + datetime.timedelta(seconds = time)
    give.set_footer(text = f'얘! 이거보지말고 배먹어배!')
    my_message = await channel.send(embed = give)
    
    # 다른 이모지로 대체하고 싶으면 디코에서 역슬래쉬 (\)랑 원하는 이모지쓰면 좀 다른 이모지나옴 그거 복사해서 아래에 넣어
    await my_message.add_reaction("🎉")
    await asyncio.sleep(time)

    new_message = await channel.fetch_message(my_message.id)

    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)

    winning_announcement = discord.Embed(color = 0xff2424)
    winning_announcement.set_author(name = f'이벤트 끝!!', icon_url= 'https://i.imgur.com/DDric14.png')
    winning_announcement.add_field(name = f'🎉 경품: {prize}', value = f'🥳 **당첨자**: {winner.mention}\n 🎫 **응모자**: {len(users)}', inline = False)
    winning_announcement.set_footer(text = '안죄송해!')
    await channel.send(embed = winning_announcement)



@client.command()
@commands.has_role("Giveaway Host")
async def reroll(ctx, channel: discord.TextChannel, id_ : int):
    try:
        new_message = await channel.fetch_message(id_)
    except:
        await ctx.send("Incorrect id.")
        return
    
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)


    reroll_announcement = discord.Embed(color = 0xff2424)
    reroll_announcement.set_author(name = f'리롤돌렷읍니다', icon_url = 'https://i.imgur.com/DDric14.png')
    reroll_announcement.add_field(name = f'🥳 세로운 당첨자:', value = f'{winner.mention}', inline = False)
    await channel.send(embed = reroll_announcement)

# 토큰
client.run("ㅌㅋ")
