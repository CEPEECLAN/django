import requests

key = "0394BB908AFEAD7C1689A72F7FB7D2E7"
base_uri = "http://api.steampowered.com/"
csgo_user_stats = "ISteamUserStats/GetUserStatsForGame/v0002/?appid=730"

def request_csgo_user_stats(steamid):
    uri = base_uri + csgo_user_stats + "&key={}&steamid={}".format(key, steamid)
    response = requests.get(uri)
    return response
