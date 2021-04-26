# bot.py
import glob
import discord
import numpy as np
import argparse
import re
import random
from jax_api import jax_complete

parser = argparse.ArgumentParser(description='CLI for Isaac')

parser.add_argument('token',
                    help='discord token')
args = parser.parse_args()
TOKEN = args.token
GUILD = 'EleutherAI'
client = discord.Client()

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def split_by_n(seq, n):
    '''A generator to divide a sequence into chunks of n units.'''
    while seq:
        yield seq[:n]
        seq = seq[n:]


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
            "WHY ARE YOU BEING DISTRACTED? YOU CAN'T GET ANYTHING DONE LIKE THAT.",
            "WHAT ARE YOU DOING, YOU LAZY LAZY PERSON?.",
            "WHY ARE YOU SO DISTRACTED?!",
            "?! IT'S YOU! YOU SHOULD GO GET A REAL WORK OUT!!! GET OVER THE DISTRACTION!",
            "ALL PLAY AND NO WORK MEANS GPT-NEO NEVER GETS DONE!",
            "ALL PLAY AND NO WORK MEANS I'M GOING TO BE AWFUL IN LIFE.",
            "ALL PLAY AND NO WORK MEANS SLOB WHO ONLY VALUES BIKESHEDDING, NO RESPECT FOR HONOR OR PRAYER!",
            "I DON'T HAVE TIME FOR THAT!", "WHY WOULD I PLAY?! YOU ARE THE SOBBING ONE",
            "OH F*$K! OH HELL NO! OH HELL NO! STOP IT!",
            "IT'S A BIG MISTAKE NOT TO WORK!", "IF YOU WANNA BE A PLAYER, GET UP AND DO SOM ETHING!",
            "WELL YOU'RE NOT WORKING!",
            "YOU'RE JUST PLAYING!", "IT 'S ALL ABOUT WORK! WELL YOU 'RE NOT WORKING!",
            "I'LL MAKE EVERYONE DO THEIR PART AND WE'LL GET TOGETHER!.", "OH HELL NO! F*$K YES! WORK!",
            "JUST BE A HUMAN AND KEEP WORKING!", "OI! WHO DOESN'T WANT TO WORK", "? JUST DO IT !"]
    n = np.random.randint(len(msgs))
    return msgs[n]


def get_random_scp(type='euclid'):
    if type == 'euclid':
        scps = glob.glob("euclid/*.txt")
    elif type == 'keter':
        scps = glob.glob("keter/*.txt")
    else:
        return
    n = np.random.randint(len(scps))
    choice = scps[n]
    with open(choice, 'r') as myfile:
        data = myfile.read()
        return list(split_by_n(data, 2000))


@client.event
async def on_message(message):
    if message.author == client.user:
        # bot doesn't react to it's own messages
        return
    if str(message.author) == "Sid#2121":
        print("It's me!")
        if message.content.lower() == '!icon':
            guild_id = discord.utils.find(lambda g: g.name == GUILD, client.guilds).id
            server = client.get_guild(guild_id)
            icon = get_random_icon()
            await server.edit(icon=icon)
    if "sprich deutsch du hurensohn" in message.content.lower():
        await message.channel.send("Ich möchte diesen Teppich nicht kaufen, bitte.")
    if "don't get the joke" in message.content.lower():
        if random.random() < 0.1: await message.channel.send("woosh")
    if random.random() < 0.0001:
        await message.channel.send(random.choice(
            ["comment of the year", "are you for real",
             "i'm taking a screenshot so i can remember this moment forever"]))
    if 'bikeshedding' in message.content.lower():
        await message.channel.send(get_random_bikeshedding_msg())

    if str(message.channel) != 'the-faraday-cage':
        return
    else:
        # messages designed for faraday cage only
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
            await message.channel.send(response)
        elif message.content.startswith('!complete'):
            print(f'message content: {message.content}')
            text = remove_prefix(message.content, "!complete").strip()
            print(f'Sending to jax api: \n{text}')
            response = jax_complete(text).split("<|endoftext|>")[0]
            print(f'Received response: \n{response}')
            for s in split_by_n(response, 2000):
                await message.channel.send(s)
        elif message.content.lower() == '!help':
            response = 'Commands are "!scp euclid" for Euclid-class SCP object or "!scp keter" for Keter class.' \
                       ' Use with caution.'
            await message.channel.send(response)


client.run(TOKEN)
