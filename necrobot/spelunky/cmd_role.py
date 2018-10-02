from necrobot.util import server
from necrobot.config import Config
from necrobot.botbase.commandtype import CommandType


class AddRacerRole(CommandType):
    def __init__(self, bot_channel):
        CommandType.__init__(self, bot_channel, 'addrole')
        self.help_text = f'Add yourself to the {Config.RACER_ROLE} role.'

    async def _do_execute(self, cmd):
        await _modify_roles(self, cmd, add=True)


class RemoveRacerRole(CommandType):
    def __init__(self, bot_channel):
        CommandType.__init__(self, bot_channel, 'removerole')
        self.help_text = f'Remove yourself from the {Config.RACER_ROLE} role.'

    async def _do_execute(self, cmd):
        await _modify_roles(self, cmd, add=False)


async def _modify_roles(cmdtype: CommandType, cmd, add: bool):
    role_to_use = None
    for role in server.server.roles:
        if role.name == Config.RACER_ROLE:
            role_to_use = role
            break
    else:
        await cmdtype.client.send_message(cmd.channel, 'Error: Could not find the role.')
        return

    if add:
        await cmdtype.client.add_roles(cmd.author, role_to_use)
        confirm_msg = 'Role added.'
    else:
        await cmdtype.client.remove_roles(cmd.author, role_to_use)
        confirm_msg = 'Role removed.'

    await cmdtype.client.send_message(cmd.channel, confirm_msg)
