import necrobot.exception
from necrobot.util import server
from necrobot.race import raceinfo, raceutil
from necrobot.race.privaterace import privateraceroom
from necrobot.race.privaterace.privateraceinfo import PrivateRaceInfo
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
            race_info = raceinfo.parse_args(cmd.args)
        except necrobot.exception.ParseException as e:
            await self.client.send_message(cmd.channel, e)
            return

        await raceutil.make_room(race_info)


class MakePrivate(CommandType):
    def __init__(self, bot_channel):
        CommandType.__init__(self, bot_channel, 'makeprivate')
        self.help_text = "Create a new private race room. This takes the same command-line options as `.make`. You " \
                         "can create multiple rooms at once by adding `-repeat N`, where `N` is the number of rooms " \
                         "to create (limit 20)."

    async def _do_execute(self, cmd):
        try:
            cmd_idx = cmd.args.index('-repeat')
            repeat_index = int(cmd.args[cmd_idx + 1])
            del cmd.args[cmd_idx + 1]
            del cmd.args[cmd_idx]
        except (ValueError, IndexError):
            repeat_index = 1

        repeat_index = min(20, max(repeat_index, 1))
        author_as_member = server.get_as_member(cmd.author)  # TODO convert to NecroUser

        try:
            race_info = raceinfo.parse_args(cmd.args)
        except necrobot.exception.ParseException as e:
            await self.client.send_message(cmd.channel, e)
            return

        race_info.private_race = True
        race_info.post_results = False
        race_info.can_be_solo = True
        private_race_info = PrivateRaceInfo(race_info)

        for _ in range(repeat_index):
            await privateraceroom.make_private_room(private_race_info, author_as_member)


class MakeCondor(CommandType):
    def __init__(self, bot_channel):
        CommandType.__init__(self, bot_channel, 'makecondor')
        self.help_text = "Create a new CoNDOR race room. This takes the same command-line options as `.make`. You " \
                         "can create multiple rooms at once by adding `-repeat N`, where `N` is the number of rooms " \
                         "to create (limit 20)."
        self.admin_only = True

    async def _do_execute(self, cmd):
        try:
            cmd_idx = cmd.args.index('-repeat')
            repeat_index = int(cmd.args[cmd_idx + 1])
            del cmd.args[cmd_idx + 1]
            del cmd.args[cmd_idx]
        except (ValueError, IndexError):
            repeat_index = 1

        repeat_index = min(20, max(repeat_index, 1))

        try:
            race_info = raceinfo.parse_args(cmd.args)
        except necrobot.exception.ParseException as e:
            await self.client.send_message(cmd.channel, e)
            return

        private_race_info.race_info.condor_race = True
        private_race_info = PrivateRaceInfo(race_info)

        for _ in range(repeat_index):
            await privateraceroom.make_private_room(private_race_info, cmd.author)
