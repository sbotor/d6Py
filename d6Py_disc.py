import discord as dc
import re

from expr import Calculator

START_SYMBOL = '='
repeat_regex = re.compile(r'^\s*[xr](\d+)(.+)$', re.IGNORECASE)

client = dc.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}. Ready.')

def calculate(expression: str) -> str:
    calc = Calculator(expression)
    calc.calculate()
    return f'Result: {calc.result}\nDetails: {calc.details}'

def repeat(times: int, expression: str) -> str:
    REPEAT_LIMIT = 15
    
    if times < 1:
        raise ValueError('Incorrect repeat number')
    elif times > REPEAT_LIMIT:
        raise ValueError(f'Sorry, the current repeat limit is {REPEAT_LIMIT}')
    else:
        calc = Calculator(expression)
        res_list = []
        for i in range(1, times + 1):
            calc.calculate()
            res = f'[{i}]. Result: {calc.result}\nDetails: {calc.details}'
            res_list.append(res)

        return '\n---\n'.join(res_list)

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if msg.content.startswith(START_SYMBOL):
        content = msg.content[1:]
        
        if content:
            # Repeat an expression
            if repeat_regex.match(content):
                match = repeat_regex.match(content)
                times = int(match[1]) # Fetch how many times to repeat
                expr = match[2] # Fetch the expression
                if expr:
                    try:
                        await msg.channel.send(repeat(times, expr))
                    except Exception as e:
                        await msg.channel.send(f'Error: {e}')
                else:
                    await msg.channel.send('The expression to evaluate is empty')
            
            # Just evaluate the expression
            else:
                try:
                    await msg.channel.send(calculate(content))
                except Exception as e:
                    await msg.channel.send(f'Error: {e}')
        else:
            await msg.channel.send('The message is empty')

# This runs the bot
if __name__ == '__main__':
    # Find the token saved in a file
    with open('token.txt') as f:
        client.run(f.read())