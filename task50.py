import os
import random
from time import time

import discord
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

CODEFORCES_API_STATUS = 'https://codeforces.com/api/user.status'
CODEFORCES_API_PROBLEMSET = 'https://codeforces.com/api/problemset.problems'
CODEFORCES_PROBLEM_URL = 'https://codeforces.com/problemset/problem/{contest_id}/{index}'


client = discord.Client()

problemset = requests.get(CODEFORCES_API_PROBLEMSET).json()[
    'result']['problems']
problemset = [(problem['contestId'], problem['index'])
              for problem in problemset]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


def get_problems(handle):
    res = requests.get(CODEFORCES_API_STATUS, params={
        "handle": handle
    }, timeout=5)
    if res.status_code != requests.codes.ok:
        return set()
    submissions = res.json()['result']
    problems = [submission['problem'] for submission in submissions]
    problems = set((problem['contestId'], problem['index'])
                   for problem in problems)
    return problems


async def command_task(message):
    handles = message.content.strip().split()
    problems = set()
    try:
        for handle in handles:
            problems.update(get_problems(handle))
    except requests.exceptions.ReadTimeout:
        await message.channel.send('Мы не смогли обработать ваш запрос! Похоже у вас слишком много посылок!')
        return
    problem = None
    for _ in range(1000):
        problem = random.choice(problemset)
        if problem in problems:
            problem = None
        else:
            break
    if problem is None:
        await message.channel.send(
            'Мы не смогли подобрать для вас задачу. Попробуйте ещё раз!')
    else:
        contest_id, index = problem
        problem_url = CODEFORCES_PROBLEM_URL.format(
            contest_id=contest_id, index=index)
        await message.channel.send(f'Вот ваша задача: {problem_url}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$task'):
        await command_task(message)


client.run(DISCORD_TOKEN)
