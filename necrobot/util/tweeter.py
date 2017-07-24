import certifi
import pycurl

from necrobot.util import console
from necrobot.config import Config
from necrobot.match.match import Match
from necrobot.league.leaguemgr import LeagueMgr


TWEET_URL = 'https://{username}:{password}@condor.host/tweet/{racer1}/{racer2}/{cawmentary}/{event}'


async def send_match_tweet(match: Match):
    cawmentator = await match.get_cawmentator()
    if cawmentator is None or LeagueMgr().league is None:
        return

    cawmentator_name = cawmentator.twitch_name if cawmentator is not None else 'RTMP'
    league_name = LeagueMgr().league.name

    curl_url = TWEET_URL.format(
                username=Config.VODRECORD_USERNAME,
                password=Config.VODRECORD_PASSWD,
                racer1=match.racer_1.display_name,
                racer2=match.racer_2.display_name,
                cawmentary=cawmentator_name,
                event=league_name
            )

    curl = pycurl.Curl()
    try:
        curl.setopt(pycurl.CAINFO, certifi.where())
        curl.setopt(pycurl.URL, curl_url)
        curl.perform()
    except pycurl.error as e:
        console.warning(
            'Pycurl error in send_match_tweet({0}): Tried to curl <{1}>. Error: {2}.'.format(
                match.matchroom_name,
                curl_url,
                e)
        )
    finally:
        curl.close()

