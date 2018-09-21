import necrobot.exception
from necrobot.util import server
from necrobot.race import raceinfo, raceutil
from necrobot.race.privaterace import privateraceinfo, privateraceroom
from necrobot.util.category import Category

from necrobot.botbase.commandtype import CommandType


class Make(CommandType):
    def __init__(self, bot_channel):
        CommandType.__init__(self, bot_channel, 'make')
        self.help_text = \
            'Makes a new race room. ASO by default, or specify a category.\n' \
            f'Example: `{self.mention} low`'

    async def _do_execute(self, cmd):
        try:
            if not cmd.args:
                race_info = raceinfo.RaceInfo()
            elif args[0].lower() == 'custom':
                try:
                    race_info = raceinfo.RaceInfo(Category.CUSTOM, args[1])
                except IndexError:
                    await self.client.send_message(cmd.channel, f'Provide a description. Ex: `{self.mention} custom "Max Low"')
                    return
            else:
                race_info = raceinfo.RaceInfo(category.fromstr(args[0]))
        except necrobot.exception.ParseException as e:
            await self.client.send_message(cmd.channel, 'Invalid category. Choose one of `aso low hell any lowng custom`.')
            return

        await raceutil.make_room(race_info)


class MakePrivate(CommandType):
    def __init__(self, bot_channel):
        CommandType.__init__(self, bot_channel, 'makeprivate')
        self.help_text = "Create a new private race room. This takes the same command-line options as `.make`. You " \
                         "can create multiple rooms at once by adding `-repeat N`, where `N` is the number of rooms " \
                         "to create (limit 20)."

    async def _do_execute(self, command):
        try:
            cmd_idx = command.args.index('-repeat')
            repeat_index = int(command.args[cmd_idx + 1])
            del command.args[cmd_idx + 1]
            del command.args[cmd_idx]
        except (ValueError, IndexError):
            repeat_index = 1

        author_as_member = server.get_as_member(command.author)     # TODO convert to NecroUser

        repeat_index = min(20, max(repeat_index, 1))

        private_race_info = privateraceinfo.parse_args(command.args)
        if private_race_info is not None:
            for _ in range(repeat_index):
                await privateraceroom.make_private_room(private_race_info, author_as_member)
        else:
            await self.client.send_message(
                command.channel, 'Error parsing arguments to `.makeprivate`.')


class MakeCondor(CommandType):
    def __init__(self, bot_channel):
        CommandType.__init__(self, bot_channel, 'makecondor')
        self.help_text = "Create a new CoNDOR race room. This takes the same command-line options as `.make`. You " \
                         "can create multiple rooms at once by adding `-repeat N`, where `N` is the number of rooms " \
                         "to create (limit 20)."
        self.admin_only = True

    async def _do_execute(self, command):
        try:
            cmd_idx = command.args.index('-repeat')
            repeat_index = int(command.args[cmd_idx + 1])
            del command.args[cmd_idx + 1]
            del command.args[cmd_idx]
        except (ValueError, IndexError):
            repeat_index = 1

        repeat_index = min(20, max(repeat_index, 1))

        private_race_info = privateraceinfo.parse_args(command.args)
        private_race_info.race_info.can_be_solo = False
        private_race_info.race_info.post_results = True
        private_race_info.race_info.condor_race = True
        if private_race_info is not None:
            for _ in range(repeat_index):
                await privateraceroom.make_private_room(private_race_info, command.author)
        else:
            await self.client.send_message(
                command.channel, 'Error parsing arguments to `.makecondor`.')
