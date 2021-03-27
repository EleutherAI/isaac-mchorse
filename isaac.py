# bot.py
import glob
import discord
import numpy as np
import argparse
import re
import random

parser = argparse.ArgumentParser(description='CLI for Isaac')

parser.add_argument('token',
                    help='discord token')
args = parser.parse_args()
TOKEN = args.token
GUILD = 'EleutherAI'
client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

def get_random_icon():
    icons = glob.glob("variable_logos/*.png")
    n = np.random.randint(len(icons))
    print(icons[n])
    with open(icons[n], 'rb') as f:
        icon = f.read()
    return icon

def get_random_bikeshedding_msg():
    msgs = ["GET BACK TO WORK YOU LAZY SLOB", "WHAT ARE YOU DOING BIKESHEDDING? BACK TO WORK!",
            "FOCUS ON THE REAL WORK! STOP GETTING DISTRACTED!",
            "IT'S ALL ABOUT WORK!  WELL YOU'RE NOT REALLY DOING ANYTHING!",
            "OI! ARE YOU WORKING?", "I'M NOT WORK ING! I'M JUST PLAYING!",
            "HEY! DON'T BE LIKE THAT!", "I have a feeling that you will be getting a lot of work done this week.",
            "I'm going to have to go ahead and say that you are going to be working hard, when you stop this bikeshedding.",
            "WHY ARE YOU BEING DISTRACTED? YOU CAN'T GET ANYTHING DONE LIKE THAT.", "WHAT ARE YOU DOING, YOU LAZY LAZY PERSON?.",
            "WHY ARE YOU SO DISTRACTED?!", "?! IT'S YOU! YOU SHOULD GO GET A REAL WORK OUT!!! GET OVER THE DISTRACTION!",
            "ALL PLAY AND NO WORK MEANS GPT-NEO NEVER GETS DONE!", "ALL PLAY AND NO WORK MEANS I'M GOING TO BE AWFUL IN LIFE.",
            "ALL PLAY AND NO WORK MEANS SLOB WHO ONLY VALUES BIKESHEDDING, NO RESPECT FOR HONOR OR PRAYER!",
            "I DON'T HAVE TIME FOR THAT!", "WHY WOULD I PLAY?! YOU ARE THE SOBBING ONE", "OH F*$K! OH HELL NO! OH HELL NO! STOP IT!",
            "IT'S A BIG MISTAKE NOT TO WORK!", "IF YOU WANNA BE A PLAYER, GET UP AND DO SOM ETHING!", "WELL YOU'RE NOT WORKING!",
            "YOU'RE JUST PLAYING!", "IT 'S ALL ABOUT WORK! WELL YOU 'RE NOT WORKING!",
            "I'LL MAKE EVERYONE DO THEIR PART AND WE'LL GET TOGETHER!.", "OH HELL NO! F*$K YES! WORK!",
            "JUST BE A HUMAN AND KEEP WORKING!", "OI! WHO DOESN'T WANT TO WORK", "? JUST DO IT !"]
    n = np.random.randint(len(msgs))
    return msgs[n]


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if str(message.author) == "Sid#2121":
        print("It's me!")
        if message.content.lower() == '!icon':
            guild_id = discord.utils.find(lambda g: g.name == GUILD, client.guilds).id
            server = client.get_guild(guild_id)
            icon = get_random_icon()
            await server.edit(icon=icon)
    #if 'start' in message.content.lower() and 'run' in message.content.lower():
    #    await message.channel.send("***pls use sacred***")
    if "sprich deutsch du hurensohn" in message.content.lower():
        await message.channel.send("Ich möchte diesen Teppich nicht kaufen, bitte.")
    if "don't get the joke" in message.content.lower():
        if random.random() < 0.1: await message.channel.send("woosh")
    if random.random() < 0.0001: await message.channel.send(random.choice(["comment of the year", "are you for real", "i'm taking a screenshot so i can remember this moment forever"]))
    if 'bikeshedding' in message.content.lower():
        await message.channel.send(get_random_bikeshedding_msg())
    if message.content.lower()[:12] == '!addresource':
        # adds resource to the selected resources channel
        try:
            print(message.content)
            result = re.match(r"^.*\<#(\d*)\>.*$", message.content)
            print(result)
            channelid = result.group(1)
            channelid = channelid.strip('#')
            print(channelid)
            valid_channels = [730093770414227531, 730091696083435541, 730095183038906412, 730097574010290318,
                              730393049863028778, 732204291078619216, 733347369847881838]
            if int(channelid) not in valid_channels:
                print(f'{channelid} invalid')
                raise Exception()
            msg = message.content.split(channelid)[1][1:].strip()
            print(channelid)
            print(msg)
            channel = client.get_channel(int(channelid))
            if message.attachments:
                # append attachment url to your image
                msg += " " + message.attachments[0].url
                # message.attachments[0].url
            else:
                print('no attachments')
            await channel.send(msg)
        except Exception as e:
            print(e)
            await message.channel.send("I'm sorry Dave, I'm afraid I can't do that")

    if str(message.channel) != 'the-faraday-cage':
        print(message.channel)
        return

    def get_random_scp(type='euclid'):
        if type == 'euclid':
            scps = glob.glob("euclid/*.txt")
        elif type == 'keter':
            scps = glob.glob("keter/*.txt")
        print(scps)
        print(len(scps))
        n = np.random.randint(len(scps))
        print(n)
        choice = scps[n]
        with open(choice, 'r') as myfile:
            data = myfile.read()
            print(len(data))
            if len(data) > 2000:
                return [data[:2000], data[2000:]]
            else:
                return [data]

    if message.content.lower() == '!scp euclid':
        response = get_random_scp('euclid')
        for r in response:
            await message.channel.send(r)
    elif message.content.lower() == '!scp keter':
        response = get_random_scp('keter')
        for r in response:
            await message.channel.send(r)
    elif message.content.lower() == '!ping':
        response = 'pong'
        print(message.channel)
        print(message.author)
        await message.channel.send(response)
    elif message.content.lower() == '!help':
        response = 'Commands are "!scp euclid" for Euclid-class SCP object or "!scp keter" for Keter class.' \
                   ' Use with caution.'
        await message.channel.send(response)

client.run(TOKEN)
