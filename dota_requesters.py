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

    def last_matches(self, player_id: int, number_of_matches: int, *params, skip_matches=0):
        '''
        Returns list of last matches of player
        :param player_id: ID of a player to return matches
        :param number_of_matches: Number of last_matches to return
        :param params: What values of match to return
        :param skip_matches: Number of matches to skip
        :return: List with all matches
        '''
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

        result = requests.post("https://api.stratz.com/graphql", headers=self.headers, json={"query": req}).json()
        data = result["data"]

        return data["player"]["matches"]
