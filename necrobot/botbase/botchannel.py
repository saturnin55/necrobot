import discord

from necrobot.botbase import cmd_all
from necrobot.botbase.necrobot import Necrobot

# Represents a discord channel on which the bot can read commands. Holds a list of commands the bot will respond to on
# this necrobot.


class BotChannel(object):
    # necrobot: a necrobot.Necrobot object (the necrobot this is a necrobot for)
    def __init__(self):
        self.command_types = []     # the list of command.CommandType that can be called on this necrobot
        self._admin_commands = [
            cmd_all.ForceCommand(self),
            cmd_all.Help(self),
            cmd_all.Info(self),
        ]

    @property
    def client(self) -> discord.Client:
        return Necrobot().client

    @property
    def necrobot(self) -> Necrobot:
        return Necrobot()

    def refresh(self, channel):
        pass

    # Returns whether the user has access to admin commands for this necrobot
    def is_admin(self, discord_member) -> bool:
        return self.necrobot.is_admin(discord_member) or self._virtual_is_admin(discord_member)

    # Override to add more admins
    def _virtual_is_admin(self, discord_member) -> bool:
        return False

    # Attempts to execute the given command (if a command of its type is in command_types)
    async def execute(self, command):
        for cmd_type in self.command_types:
            await cmd_type.execute(command)
        for cmd_type in self._admin_commands:
            await cmd_type.execute(command)
