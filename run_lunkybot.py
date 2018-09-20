from necrobot.botbase import server
from necrobot.spelunky.lunkymainchannel import MainBotChannel
from necrobot.util import console
from necrobot import logon


async def load_lunkybot_config(necrobot):
    MAIN_CHANNEL_NAME = 'lunkybot'

    server.main_channel = server.find_channel(channel_name=MAIN_CHANNEL_NAME)
    if server.main_channel is None:
        console.warning(f'Could not find the "{MAIN_CHANNEL_NAME}" channel.')
    necrobot.register_bot_channel(server.main_channel, MainBotChannel())


if __name__ == "__main__":
    logon.logon(
        config_filename='data/lunkybot_config',
        load_config_fn=load_lunkybot_config
    )
