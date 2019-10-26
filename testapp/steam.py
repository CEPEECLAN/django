import requests

key = "0394BB908AFEAD7C1689A72F7FB7D2E7" # CLEAR TEXT WOOOOOO
base_uri = "http://api.steampowered.com/"
csgo_user_stats_sub_url = "ISteamUserStats/GetUserStatsForGame/v0002/?appid=730"
steam_user_summary_sub_url = "ISteamUser/GetPlayerSummaries/v2/"

def process_stats(stats):

    player_stats = {
            'total_kills': stats['total_kills'],
            'total_deaths': stats['total_deaths'],
            'total_mvps': stats['total_mvps'],
            'total_matches_won': stats['total_matches_won'],
            'total_matches_played': stats['total_matches_played'],
            'total_shots_hit': stats['total_shots_hit'],
            'total_shots_fired': stats['total_shots_fired'],
            'total_kills_headshot': stats['total_kills_headshot'],
            'total_kills_enemy_weapon': stats['total_kills_enemy_weapon'],
            'total_kills_knife_fight': stats['total_kills_knife_fight'],
            'total_kills_enemy_blinded': stats['total_kills_enemy_blinded'],
            'total_kills_against_zoomed_sniper': stats['total_kills_against_zoomed_sniper'],
            'overall_accuracy': "{}%".format(round(stats['total_shots_hit'] / stats['total_shots_fired'] * 100)),
    }

    all_wep_stats  = {}
    all_map_stats = {}
    # extract weapon stats
    for name, value in stats.items():
        if 'total_kills_' in name and name not in player_stats:
            weapon = name.split('_')[-1]
            if weapon not in all_wep_stats:
                all_wep_stats[weapon] = {}
            all_wep_stats[weapon].update({ 'total_kills': value })
        if 'total_shots_' in name and name not in player_stats:
            weapon = name.split('_')[-1]
            if weapon not in all_wep_stats:
                all_wep_stats[weapon] = {}
            all_wep_stats[weapon].update({ 'total_shots': value })
        if 'total_hits_' in name:
            weapon = name.split('_')[-1]
            if weapon not in all_wep_stats:
                all_wep_stats[weapon] = {}
            all_wep_stats[weapon].update({ 'total_hits': value })
        if 'total_wins_map_' in name:
            map_name =  name.split('_')[-2] + '_' + name.split('_')[-1]
            if map_name not in all_map_stats:
                all_map_stats[map_name] = {}
            all_map_stats[map_name].update({ 'total_wins': value })

        if 'total_rounds_map_' in name:
            map_name =  name.split('_')[-2] + '_' + name.split('_')[-1]
            if map_name not in all_map_stats:
                all_map_stats[map_name] = {}
            all_map_stats[map_name].update({ 'total_rounds': value })

    for weapon, wep_stats in all_wep_stats.items():
        if 'total_hits' in wep_stats and 'total_shots' in wep_stats:
            accuracy = "{}%".format(round(float(wep_stats['total_hits']) / wep_stats['total_shots'] * 100))
            all_wep_stats[weapon].update({ 'accuracy': accuracy })

    for map_name, map_stats in all_map_stats.items():
        if 'total_wins' in map_stats and 'total_rounds' in map_stats:
            winrate = "{}%".format(round(float(map_stats['total_wins']) / map_stats['total_rounds'] * 100))
            all_map_stats[map_name].update({ 'win_rate': winrate })

    stats = {
        'player_stats': player_stats,
        'weapon_stats': all_wep_stats,
        'map_stats': all_map_stats
    }

    return stats


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
                stats = user_stats['playerstats']['stats']
                extracted_stats = { entry['name']: entry['value'] for entry in stats }
                parsed_user_stats['stats'] = process_stats(extracted_stats)

            if 'achievements' in user_stats['playerstats']:
                stats = user_stats['playerstats']['achievements']
                parsed_user_stats['achievements'] = {
                        entry['name']: entry['achieved'] == 1 for entry in stats
                }

        return parsed_user_stats

