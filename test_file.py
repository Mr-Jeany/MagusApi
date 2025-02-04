from dota_requesters import StratzRequester

sr = StratzRequester()

print(sr.last_matches(1548070952, 10, "id", "didRadiantWin", "durationSeconds"))