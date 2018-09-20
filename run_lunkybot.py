from necrobot.botbase import server
from necrobot.spelunky.lunkymainchannel import MainBotChannel
from necrobot import logon

async def load_lunkybot_config(necrobot):
    server.main_channel = server.find_channel(channel_name='lunkybot')
    necrobot.register_bot_channel(server.main_channel, MainBotChannel())


if __name__ == "__main__":
    logon.logon(
        config_filename='data/lunkybot_config',
        load_config_fn=load_lunkybot_config
    )
