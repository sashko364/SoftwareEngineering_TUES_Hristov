import requests
from django.shortcuts import render
from .models import Car

# Create your views here.
PI = 3.14

from django.http import HttpResponse, JsonResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    info = requests.get('https://api-v3.mbta.com/predictions?page%5Boffset%5D=0&page%5Blimit%5D=10&sort=departure_time&include=schedule%2Ctrip&filter%5Bdirection_id%5D=0&filter%5Bstop%5D=place-north').json()
    data = []
    for i in info["data"]:
        trainData = {}
        trainData["departureTime"] = i["attributes"]["departure_time"]
        for k in info["included"]:
            if i["relationships"]["trip"]["data"]["id"] == k["id"]:
                trainData["destination"] = k["attributes"]["headsign"]

        if i["relationships"]["vehicle"]["data"] is None:
            trainData["train"] = "null"
        else:
            for k in info["included"]:
                if i["relationships"]["trip"]["data"]["id"] == k["id"]:
                    trainData["train"] = i['relationships']['vehicle']['data']['id']

        trainData["status"] = i["attributes"]["status"]

        data.append(trainData)

    return render(request, 'home.html', {'data': data})

def about(request):
    return render(request, 'about.html')

def cars(request):
    cars = Car.objects.all()
    return render(request, 'cars.html', {'cars':cars})
