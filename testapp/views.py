from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import testapp.steam as steam
import json


gabbe="76561198000008696"


def index(request):
    return render(request, 'testapp/index.html', {})


def stats(request):
    # steamid = request.GET.get('steamid', '') # read steam id data from url, steamid=....
    steamid = gabbe

    user_data_response = steam.request_csgo_user_stats(steamid)

    if user_data_response.status_code == 200: # OK!
        json_string = json.dumps(user_data_response.json())
        return render(request, 'testapp/stats.html', {'csgo_stats': json_string})

    response = HttpResponse(
        content=user_data_response.content,
        status=user_data_response.status_code,
        content_type=user_data_response.headers['Content-Type']
    )
    return response
