from necrobot.spelunky.mainchannel import MainBotChannel
from necrobot.spelunky.pmbotchannel import PMBotChannel
from necrobot.util import server, console
from necrobot import logon


async def load_lunkybot_config(necrobot):
    MAIN_CHANNEL_NAME = 'lunkybot'
    necrobot.register_pm_channel(PMBotChannel())

    server.main_channel = server.find_channel(channel_name=MAIN_CHANNEL_NAME)
    if server.main_channel is None:
        console.warning(f'Could not find the "{MAIN_CHANNEL_NAME}" channel.')
    necrobot.register_bot_channel(server.main_channel, MainBotChannel())


if __name__ == "__main__":
    logon.logon(
        config_filename='data/lunkybot_config',
        logging_prefix='lunkybot',
        load_config_fn=load_lunkybot_config
    )
