from django.shortcuts import render
from django.http import JsonResponse
from . import seacher
import json
import os
from emwiki.settings import BASE_DIR
# Create your views here.


def index(request):
    search_query = request.GET.get('search_query', default='')
    categorys_json_path = os.path.join(BASE_DIR, 'emsearch','search_settings', "categorys.json")
    with open(categorys_json_path, 'r', encoding="utf-8") as f:
        categorys = json.load(f)
    context = {
        'search_query': search_query,
        'categorys': categorys
    }
    return render(request, 'emsearch/index.html', context)


def search(request):
    search_query = request.GET.get('search_query', default='')
    if(search_query):
        search_results = seacher.search(search_query)
    else:
        search_results = []
    context = {
        'search_results': search_results,
        'search_query': search_query,
    }
    return JsonResponse(context)


def get_keywords(request):
    keywords_json_path = os.path.join(BASE_DIR, 'emsearch','search_settings', "keywords.json")
    with open(keywords_json_path, 'r', encoding="utf-8") as f:
        keywords = json.load(f)
    return JsonResponse(keywords)