from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from testapp.steam import SteamRequestHelper, SteamJsonParser
import json


params = {}
steamids = {
    "goob": "?steamid=76561198000008696",
    "turbokuk2000": "?steamid=76561198001388118",
    "paj": "?steamid=76561198062737401",
    "slak": "?steamid=76561198010352447",
    "kattihatt2": "?steamid=76561198095495090",
    "bop": "?steamid=76561197996258270",
    "killer human": "?steamid=76561198004576152",
}


def index(request):
    menu = { "menu": { "main": reverse(index), "stats": reverse(stats) }}
    params.update(menu)
    return render(request, 'testapp/index.html', params)


def stats(request):
    menu = { "menu": { "main": reverse(index), "stats": reverse(stats) }}
    params.update(menu)
    ids = {
            "steamids": { name: reverse(stats) + steamid for name, steamid in steamids.items() }
    }
    params.update(ids)

    steamid = request.GET.get('steamid', '') # read steam id data from url, steamid=....

    user_summary_response = SteamRequestHelper.request_steam_user_summary(steamid)
    user_stats_response = SteamRequestHelper.request_csgo_user_stats(steamid)

    parsed_user_summary = {}
    parsed_user_stats = {}
    if user_summary_response.status_code == 200:
        parsed_user_summary = SteamJsonParser.parse_steam_user_summary(user_summary_response.json())
        if len(parsed_user_summary) == 0:
            parsed_user_summary.update({ "personaname": "Player not found.. Check privacy settings! :(" })
        params.update(parsed_user_summary)

    if user_stats_response.status_code == 200:
        parsed_user_stats = SteamJsonParser.parse_csgo_user_stats(user_stats_response.json())
        params.update(parsed_user_stats['stats'])
        params.update({ 'achievements': parsed_user_stats['achievements'] })

    return render(request, 'testapp/stats.html', params)

