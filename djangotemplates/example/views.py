# Add the two views we have been talking about  all this time :)

from django.shortcuts import render
from django.views.generic import TemplateView # Import TemplateView
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import requests
import json
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# @require_http_methods(['GET'])
# def search(request):
#     q = request.GET.get('q')
#     if q:
#         books = Advent.objects.filter(title__icontains=q)
#         return render(request, 'search_results.html', {'books': books, 'query': q})
#     return HttpResponse('Please submit a search term.')

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def profile(request):
    if request.GET:
        keyword = request.GET['q']
        if cache.get(keyword):
            CacheData = cache.get(keyword)
            finalData = json.dumps(CacheData)
            print('DATA FROM CACHE')
            return render( request, 'index.html', {'js':finalData})
        else:
            response = SearchStack(keyword)
            cache.set(keyword, response)
            print('DB DATA')
            if response:
                finalData = json.dumps(response)
            
            return render( request, 'index.html', {'js':finalData})
    else:
        return render(request, 'index.html')


def SearchStack(keyword):
    url = 'https://api.stackexchange.com/search/advanced?site=stackoverflow.com&q='+keyword+'&page=2&pagesize=2&fromdate=1598918400&todate=1605916800&order=desc&sort=activity'
    headers = {'Accept': 'application/json'}
    r = requests.get(url, headers= headers)

    return r.json()




# class HomePageView(TemplateView):
#     template_name = "index.html"
       


# class AboutPageView(TemplateView):
#     template_name = "about.html"
    


# def DataPageView(self, request, **kwargs):
#     if request.method == "GET" :
#         name = request.GET['qns']
#         print(name)
#     return render(request, 'index.html', name)

# def newView(request):
#       context = {}
#       if request.method == 'GET':
#           city = request.GET.get('city')
#           api_address='http://api.openweathermap.org/data/2.5/weather? appid=KEY&q='
#           url = api_address + city
#           json_data = requests.get(url).json()
#           kelvin = json_data['main']['temp']
#           context['temperature'] = round(kelvin - 273.15,0)
#       render(request,'index.html',context)