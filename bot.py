"""
OmniBot: The Pluggable Discord Bot
"""
import configparser
import logging
import os
import sys
import traceback
from logging.handlers import RotatingFileHandler

import discord
from discord.ext import commands

# if these don't load, you didn't install correctly.
DEFAULT_EXTENSIONS = [
    'jishaku',
    'ext.admin',
    'ext.fun',
    'ext.rng',
]

# quick basic logging setup
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(f'{logger.name}.log', maxBytes=1024**2, backupCount=5, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class OmniBot(commands.Bot):
    def __init__(self):
        # Get config file read
        self.config_file = 'config.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

        # General config info for before the bot loads
        self.token = self.config['General']['token']
        self.owner_id = self.config['General']['owner_id']
        self.crypto_token = self.config['General']['crypto_token']

        # Initialize the bot further to give access to extension/cog/command stuffs
        super().__init__(command_prefix=self.config['General']['command_prefix'],
                         description='OmniBot: The Pluggable Discord Bot')

        # Borrow from Default extensions and build out any missing files
        self.ext_list = DEFAULT_EXTENSIONS
        for root, dir, files in os.walk('ext'):
            for file in files:
                if file in DEFAULT_EXTENSIONS:
                    break
                file = 'ext.{0}'.format(file.strip('.py'))
                if file not in self.ext_list:
                    self.ext_list.append(file)
        for ext in self.ext_list:
            try:
                self.load_extension(ext)
            except Exception as e:
                logger.error(e)

    async def on_ready(self):
        # Just a bunch of prints for shits
        logger.info('--------------------')
        logger.info('Logged in as')
        logger.info(self.user.name)
        logger.info(self.user.id)
        logger.info('--------------------')
        print('--------------------')
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('--------------------')

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
                traceback.print_tb(original.__traceback__)
                print(f'{original.__class__.__name__}: {original}', file=sys.stderr)
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(error)

    def run(self):
        super().run(self.token)

if __name__ == '__main__':
    OmniBot = OmniBot()
    try:
        OmniBot.run()
    except KeyboardInterrupt:
        OmniBot.logout()