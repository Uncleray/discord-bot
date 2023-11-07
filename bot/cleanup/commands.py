# example Command for Ping -> Pong
@bot.command(help='sends a pong as answer.',brief='sends a pong as answer.')
async def ping(ctx):
    await ctx.reply('Pong!')

# command with fixed response from response.py file
@bot.command(help='sends a greeting message back.',brief='sends a greeting message back.')
async def hello(ctx):
    await ctx.reply(responses.hello_response)

# command to receive random answers (magic 8ball)
@bot.command(aliases=['8ball'])
async def eightbal(ctx, *, question):
    responses = [
        'not so sure about that.',
        'yes, clearly.',
        'very doubtful.'
    ]
    await ctx.reply(random.choice(responses))

# command to clear channel for user provides {amount} of messages
@bot.command(help='clears messages in the channel.',brief='clears messages in the channel.')
async def clear(ctx, amount):
    await ctx.message.delete() # delete the command send by user before further deletions.
    if amount == 'all':
        messages = []
        async for message in ctx.channel.history(limit=None):
            messages.append(message)
        await ctx.channel.delete_messages(messages)
        await ctx.send('All messages have been cleared.')
    else:
        amount = int(amount)
        amount = min(amount, 100) # limit the number of messages that can be cleared at once.
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'{amount} messages have been cleared')