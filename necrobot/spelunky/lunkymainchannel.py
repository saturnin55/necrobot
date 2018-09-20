from necrobot.botbase import cmd_admin
from necrobot.spelunky import cmd_role
from necrobot.stdconfig import cmd_color
from necrobot.race import cmd_racemake
from necrobot.stats import cmd_stats
from necrobot.user import cmd_user

from necrobot.botbase.botchannel import BotChannel


class MainBotChannel(BotChannel):
    def __init__(self):
        BotChannel.__init__(self)
        self.channel_commands = [
            cmd_admin.Die(self),
            cmd_admin.Reboot(self),

            cmd_color.ColorMe(self),

            cmd_racemake.Make(self),
            cmd_racemake.MakeCondor(self),
            cmd_racemake.MakePrivate(self),

            cmd_role.AddRacerRole(self),
            cmd_role.RemoveRacerRole(self),

            cmd_stats.Fastest(self),
            cmd_stats.MostRaces(self),
            cmd_stats.Stats(self),

            cmd_user.DailyAlert(self),
            cmd_user.RaceAlert(self),
            cmd_user.RTMP(self),
            cmd_user.SetInfo(self),
            cmd_user.Timezone(self),
            cmd_user.Twitch(self),
            cmd_user.ViewPrefs(self),
            cmd_user.UserInfo(self),
        ]
