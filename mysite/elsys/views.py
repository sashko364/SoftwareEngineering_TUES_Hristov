import requests
from django.shortcuts import render
from .models import Car

# Create your views here.
PI = 3.14

from django.http import HttpResponse, JsonResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def data(request):
    response = requests.get("https://api-v3.mbta.com/predictions?page%5Boffset%5D=0&page%5Blimit%5D=10&sort=departure_time&include=schedule%2Cvehicle%2Ctrip&filter%5Bdirection_id%5D=0&filter%5Bstop%5D=place-north")
    response = response.json()
    # new_table = InfoTable(schedule_data[''])
    # return render(request, 'grafik.html', {'data': schedule_data})

    trains = []
    for entry in response['data']:
        status = entry['attributes']['status']
        trip_id = entry['relationships']['trip']['data']['id']
        schedule_id = entry['relationships']['schedule']['data']['id']
        new_line = InfoTableLine(trip_id, schedule_id, "", "", status)
        trains.append(new_line)

    for entry in response['included']:
        if entry['type'] == "trip":
            for train in trains:
                if entry['id'] == train.trip_id:
                    train.destination = entry['attributes']['headsign']
                    break

        elif entry['type'] == "schedule":
            for train in trains:
                if entry['id'] == train.schedule_id:
                    train.departure_time = entry['attributes']['departure_time']
                    break

    # return JsonResponse({'trains': trains}, safe=False)
    return render(request, 'grafik.html', {'trains': trains})

def about(request):
    return render(request, 'about.html')

def cars(request):
    cars = Car.objects.all()
    return render(request, 'cars.html', {'cars':cars})
