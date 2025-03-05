import requests

from config import BEARER
from utils import replace_placeholders, multiplaceholder


class StratzRequester:
    def __init__(self):
        self.headers = {
            "Authorization": BEARER,
            "User-Agent": "STRATZ_API",
            "Content-Type": "application/json"
        }

    def get_data_from_request(self, r):
        result = requests.post("https://api.stratz.com/graphql", headers=self.headers, json={"query": r}).json()
        data = result["data"]

        return data

    def last_matches(self, player_id: int, *params, number_of_matches: int=10, skip_matches: int=0):
        """
        Returns list of last matches of player
        :param player_id: ID of a player to return matches
        :param number_of_matches: Number of last_matches to return
        :param params: What values of match to return
        :param skip_matches: Number of matches to skip
        :return: List with all matches
        """
        req = '''
        {
            player (steamAccountId: %player_id)
            {
                matches (request: {take: %number_of_matches, skip: %skip_matches})
                {
                    %%params
                }
            }
        }
        '''

        req = replace_placeholders(req, ["player_id", "number_of_matches", "skip_matches"], [player_id, number_of_matches, skip_matches])
        req = multiplaceholder(req, "params", params)

        data = self.get_data_from_request(req)

        return data["player"]["matches"]

    def last_matches_heroes_filter(self, player_id: int, heroes_ids: list[int], *params, number_of_matches: int = 10, skip_matches: int = 0):
        """
        Returns list of last matches of player
        :param heroes_ids: ID of heroes to filter by
        :param player_id: ID of a player to return matches
        :param number_of_matches: Number of last_matches to return
        :param params: What values of match to return
        :param skip_matches: Number of matches to skip
        :return: List with all matches
        """
        req = '''
        {
            player (steamAccountId: %player_id)
            {
                matches (request: {take: %number_of_matches, skip: %skip_matches, heroIds: %hero_ids})
                {
                    %%params
                }
            }
        }
        '''

        joined_heroes = ",".join(map(str, heroes_ids))
        req = replace_placeholders(req, ["player_id", "number_of_matches", "skip_matches", "hero_ids"],
                                   [player_id, number_of_matches, skip_matches, f"[{joined_heroes}]"])
        req = multiplaceholder(req, "params", params)

        data = self.get_data_from_request(req)

        return data["player"]["matches"]

    def constants(self, *params):
        req = '''
        {
            constants
            {
                %%params
            }
        }
        '''

        req = multiplaceholder(req, "params", params)

        data = self.get_data_from_request(req)

        return data["constants"]

class OpenDotaRequester:
    def __init__(self):
        self.heroes_constant = requests.get("https://api.opendota.com/api/constants/heroes").json()
        self.hero_abilities_constant = requests.get("https://api.opendota.com/api/constants/hero_abilities").json()

    def heroes(self, player_id: int, exclude: list=None, sort_by="games", reverse=True):
        """
        Returns a list of dictionary of heroes with their stats
        :param player_id: ID of a player to return heroes of
        :param exclude: Parameters that will be excluded from return
        :param sort_by: Name of the parametr to sort by
        :param reverse: Whether the list should be sorted in reverse way
        :return:
        """
        result = requests.get(f"https://api.opendota.com/api/players/{player_id}/heroes").json()

        values = ["last_played", "games", "win", "with_games", "with_win", "against_games", "against_win"]

        if not exclude is None:
            values = list(set(values) - set(exclude))

        filtered_heroes = {}

        for hero in result:
            filtered_heroes[hero["hero_id"]] = {
                "hero_id": hero["hero_id"],
                "display_name": self.heroes_constant[str(hero["hero_id"])]["localized_name"]
            }
            for value in values:
                filtered_heroes[hero["hero_id"]][value] = hero[value]

        return dict(sorted(filtered_heroes.items(), key=lambda item: item[1][sort_by], reverse=reverse))


    def id_to_npc(self, id):
        return self.heroes_constant[str(id)]["name"]
