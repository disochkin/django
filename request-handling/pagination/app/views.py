import urllib

from django.core.paginator import Paginator
from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.conf import settings
import csv


def custom_csv2list(filename, column_name):
    with open(filename, 'r', encoding='cp1251') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        result = []
        for row in reader:
            item = {}
            for column in column_name:
                item.update({column: row[column]})
            result.append(item)
        return result


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    data = custom_csv2list(settings.BUS_STATION_CSV, ['Name', 'Street', 'District'])
    paginator = Paginator(data, 20)
    page = request.GET.get('page', 1)
    page_content = paginator.page(page)
    prev_page, next_page = None, None
    if page_content.has_previous():
        prev_page = reverse('bus_stations') + '?' + urllib.parse.urlencode({'page': page_content.previous_page_number()})
    if page_content.has_next():
        next_page = reverse('bus_stations') + '?' + urllib.parse.urlencode({'page': page_content.next_page_number()})
    return render_to_response('index.html', context={
         'bus_stations': page_content,
         'current_page': page_content.number,
         'prev_page_url': prev_page,
         'next_page_url': next_page,
    })
