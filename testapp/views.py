from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from testapp.steam import SteamRequestHelper, SteamJsonParser
import json


gabbe="76561198000008696"


def index(request):
    return render(request, 'testapp/index.html', {})


def stats(request):
    steamid = request.GET.get('steamid', '') # read steam id data from url, steamid=....
    if steamid == "":
        steamid = gabbe

    user_summary_response = SteamRequestHelper.request_steam_user_summary(steamid)
    user_stats = SteamRequestHelper.request_csgo_user_stats(steamid)

    if user_stats.status_code != 200:
        response = HttpResponse(
            content=user_stats.content,
            status=user_stats.status_code,
            content_type=user_stats.headers['Content-Type']
        )
        return response

    if user_summary_response.status_code != 200:
        response = HttpResponse(
            content=user_summary_response.content,
            status=user_summary_response.status_code,
            content_type=user_summary_response.headers['Content-Type']
        )
        return response

    parsed_user_summary = SteamJsonParser.parse_steam_user_summary(user_summary_response.json())
    parsed_user_stats = SteamJsonParser.parse_csgo_user_stats(user_stats.json())

    parsed_user_summary['player_stats'] = parsed_user_stats['stats']['player_stats']
    parsed_user_summary['weapon_stats'] = parsed_user_stats['stats']['weapon_stats']
    parsed_user_summary['map_stats'] = parsed_user_stats['stats']['map_stats']
    parsed_user_summary['achievements'] = parsed_user_stats['achievements']

    return render(request, 'testapp/stats.html', parsed_user_summary)


