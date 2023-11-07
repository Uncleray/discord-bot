# custom help menu from chatgpt -> I need to check this code and understand what it does and why its written as it is. Aim: be able to write this myself.
class CustomHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            'help': 'Shows help about the bot, a command, or a category',
            'aliases': ['h']
        })

    async def send_bot_help(self, mapping):
        # Customize how bot-level help is displayed
        embed = discord.Embed(title=settings.BOT_NAME, description='Customized help for this bot.', color=discord.Color.blue())
        for cog, commands in mapping.items():
            command_list = []
            for command in commands:
                if not command.hidden:
                    command_list.append(f'`{command.name}` - {command.short_doc or "No description provided."}')
            if command_list:
                embed.add_field(name=cog.qualified_name if cog else "No Category", value='\n'.join(command_list), inline=False)
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        # Customize how individual command help is displayed
        embed = discord.Embed(title=f'Command Help: {command.name}', description=command.help or "No description provided.", color=discord.Color.green())
        embed.add_field(name='Usage', value=f'`{self.get_command_signature(command)}`', inline=False)
        await self.context.send(embed=embed)

bot.help_command = CustomHelpCommand()