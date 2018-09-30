import math

from necrobot.race import racedb
from necrobot.util import console, racetime
from necrobot.util.category import Category
from necrobot.util.singleton import Singleton


class CategoryStats(object):
    def __init__(self, category):
        self.category = category
        self.number_of_races = 0
        self.mean = 0
        self.var = 0
        self.winrate = 0
        self.has_wins = False

    @property
    def catname(self) -> str:
        return str(self.category)

    @property
    def stdev(self) -> float:
        return math.sqrt(self.var)

    @property
    def mean_str(self) -> str:
        if self.has_wins:
            return racetime.to_str(int(self.mean))
        else:
            return '--'

    @property
    def stdev_str(self) -> str:
        if self.has_wins:
            return racetime.to_str(int(self.stdev))
        else:
            return '--'

    def barf(self) -> None:
        console.info('{0:>25}   {1:>5}   {2:>9}  {3:>9}  {4:>6}\n'.format(
            self.catname,
            self.number_of_races,
            self.mean_str,
            self.stdev_str,
            int(self.winrate * 100)))


class GeneralStats(object):
    def __init__(self):
        self._catstats = []

    @property
    def infotext(self) -> str:
        info_text = '{0:>25}   {1:<5}   {2:<9}  {3:<9}  {4}\n'.format('', 'Races', 'Avg', 'Stdev', 'Clear%')
        for cat in sorted(self._catstats, key=lambda c: c.number_of_races, reverse=True):
            info_text += '{0:>25}   {1:>5}   {2:>9}  {3:>9}  {4:>6}\n'.format(
                cat.catname,
                cat.number_of_races,
                cat.mean_str,
                cat.stdev_str,
                int(cat.winrate*100))
        return info_text[:-1]

    def insert_catstats(self, cat: CategoryStats) -> None:
        self._catstats.append(cat)

    def get_catstats(self, cat: Category) -> CategoryStats:
        for c in self._catstats:
            if c.category == cat:
                return c
        return CategoryStats(cat)


class StatCache(object, metaclass=Singleton):
    class CachedStats(object):
        def __init__(self):
            self.last_race_number = 0      # The number of the last race cached
            self.stats = GeneralStats()

    def __init__(self):
        self._cache = {}  # Map from discord ID's to UserStats

    async def get_general_stats(self, user_id) -> GeneralStats:
        last_race_number = await racedb.get_largest_race_number(user_id=user_id)

        # Check whether we have an up-to-date cached version, and if so, return it
        cached_data = self.CachedStats()
        if user_id in self._cache:
            cached_data = self._cache[user_id]
            if cached_data.last_race_number == last_race_number:
                return cached_data.stats

        # If here, the cache is out-of-date
        general_stats = GeneralStats()
        for row in await racedb.get_public_race_numbers(user_id=user_id):
            cat = Category.fromstr(row[0])
            catstats = CategoryStats(cat)
            catstats.number_of_races = int(row[1])
            total_time = 0
            total_squared_time = 0
            number_of_wins = 0
            number_of_forfeits = 0
            for stat_row in await racedb.get_all_racedata(user_id=user_id, cat_name=cat.name.lower()):
                if int(stat_row[1]) == -2:  # finish
                    time = int(stat_row[0])
                    total_time += time
                    total_squared_time += time * time
                    number_of_wins += 1
                else:
                    number_of_forfeits += 1

            if number_of_wins > 0:
                catstats.mean = total_time / number_of_wins

            if number_of_wins > 1:
                catstats.has_wins = True
                catstats.var = \
                    (total_squared_time / (number_of_wins-1)) - catstats.mean * total_time/(number_of_wins-1)

            if number_of_wins + number_of_forfeits > 0:
                catstats.winrate = number_of_wins / (number_of_wins + number_of_forfeits)

            general_stats.insert_catstats(catstats)

        # Update the cache
        cached_data.last_race_number = last_race_number
        cached_data.stats = general_stats
        self._cache[user_id] = cached_data

        # Return
        return general_stats


async def get_general_stats(user_id: int) -> GeneralStats:
    return await StatCache().get_general_stats(user_id)


async def get_category_stats(user_id: int, category: Category) -> CategoryStats:
    general_stats = await StatCache().get_general_stats(user_id)
    return general_stats.get_catstats(category)


async def get_winrates(user_id_1: int, user_id_2: int, category: Category) -> tuple or None:
    stats_1 = await get_category_stats(user_id_1, category)
    stats_2 = await get_category_stats(user_id_2, category)
    if not stats_1.has_wins or not stats_2.has_wins:
        return None

    m2_minus_m1 = stats_2.mean - stats_1.mean
    sum_var = stats_1.var + stats_2.var
    erf_arg = m2_minus_m1 / math.sqrt(2*sum_var)
    if m2_minus_m1 > 0:
        winrate_of_1_if_both_finish = (1.0 + math.erf(erf_arg))/2.0
    else:
        winrate_of_1_if_both_finish = (1.0 - math.erf(-erf_arg))/2.0

    both_finish_prob = stats_1.winrate * stats_2.winrate
    neither_finish_prob = (1-stats_1.winrate)*(1-stats_2.winrate)
    winrate_of_1 = winrate_of_1_if_both_finish*both_finish_prob + (stats_1.winrate - both_finish_prob)
    winrate_of_2 = (1.0-winrate_of_1_if_both_finish)*both_finish_prob + (stats_2.winrate - both_finish_prob)
    return winrate_of_1, winrate_of_2, neither_finish_prob


async def get_most_races_infotext(category: Category, limit: int) -> str:
    most_races = await racedb.get_most_races_leaderboard(category.name.lower(), limit)
    infotext = '{0:>20} {1:>6}\n'.format('', 'Races')
    for row in most_races:
        infotext += '{0:>20.20} {1:>6}\n'.format(row[0], row[1])
    return infotext


async def get_fastest_times_infotext(category: Category, limit: int) -> str:
    fastest_times = await racedb.get_fastest_times_leaderboard(category.name.lower(), limit)
    infotext = '{0:>20} {1:<9} {2:<9} {3:<13}\n'.format('', 'Time (rta)', 'Seed', 'Date')
    for row in fastest_times:
        infotext += '{0:>20.20} {1:>9} {2:>9} {3:>13}\n'.format(
            row[0],
            racetime.to_str(int(row[1])),
            row[2],
            row[3].strftime("%b %d, %Y"))
    return infotext
