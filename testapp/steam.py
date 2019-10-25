import requests

key = "0394BB908AFEAD7C1689A72F7FB7D2E7" # CLEAR TEXT WOOOOOO
base_uri = "http://api.steampowered.com/"
csgo_user_stats_sub_url = "ISteamUserStats/GetUserStatsForGame/v0002/?appid=730"
steam_user_summary_sub_url = "ISteamUser/GetPlayerSummaries/v2/"


class SteamRequestHelper:
    def request_steam_user_summary(steamid):
        uri = base_uri + steam_user_summary_sub_url + "?key={}&steamids={}".format(key, steamid)
        response = requests.get(uri)
        return response


    def request_csgo_user_stats(steamid):
        uri = base_uri + csgo_user_stats_sub_url + "&key={}&steamid={}".format(key, steamid)
        response = requests.get(uri)
        return response

class SteamJsonParser:

    def parse_steam_user_summary(user_summary):
        parsed_user_summary = {}

        if 'response' in user_summary:
            if 'players' in user_summary['response']:
                summary = user_summary['response']['players'][0]
                parsed_user_summary['steamid'] = int(summary['steamid'])
                parsed_user_summary['personaname'] = summary['personaname']
                parsed_user_summary['avatar'] = summary['avatarfull']

        return parsed_user_summary


    def parse_csgo_user_stats(user_stats):
        parsed_user_stats = {
                'stats': {},
                'achievements': {}
        }
        if 'playerstats' in user_stats:
            if 'stats' in user_stats['playerstats']:
                stats_dict = user_stats['playerstats']['stats']
                parsed_user_stats['stats'] = {
                        entry['name']: entry['value'] for entry in stats_dict
                }

            if 'achievements' in user_stats['playerstats']:
                stats_dict = user_stats['playerstats']['achievements']
                parsed_user_stats['achievements'] = {
                        entry['name']: entry['achieved'] == 1 for entry in stats_dict
                }

        return parsed_user_stats
