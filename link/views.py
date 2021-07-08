import json
import requests

from bs4 import BeautifulSoup

from rest_framework.response import Response
from rest_framework.views import APIView

response = {}  # Словарь с результатом
default_tags = ['html', 'head', 'body', 'p', 'img']  # Стандартные тэги для запроса без тэгов в параметрах


def get_content(link):
    page = requests.get(link)
    b_soup = BeautifulSoup(page.content, features="html.parser")
    return b_soup


class LinkBlock(APIView):

    def get(self, request):
        response.clear()
        link = request.GET.get("link", "https://freestylo.ru/")

        tags = request.GET.getlist('tags')
        tag_list = ','.join(tags).split(',')

        content = get_content(link)

        if not tags:
            for item in default_tags:
                response.update({item: len(content.findAll(item))})

        else:
            for item in tag_list:
                response.update({item: len(content.findAll(item))})

        return Response(response)

    def post(self, request):
        response.clear()
        link = request.POST.get('link')  # Ссылка из тела запроса
        structure = request.POST.get('structure')  # Структура из тела запроса

        content = get_content(link)

        for item in default_tags:
            response.update({item: len(content.findAll(item))})

        struct_json = json.loads(structure)

        if struct_json == response:
            return Response({"is_correct": True})

        else:
            result = {}

            for key in struct_json.keys():
                value1 = {k: struct_json[k] for k in set(struct_json) - set(response)}
                value2 = {k: response[k] for k in set(response) - set(struct_json)}
                result.update(value1)
                result.update(value2)

                if key in response:
                    diff = response[key] - struct_json[key]

                    if diff != 0:
                        result.update({key: abs(diff)})

            return Response(result)
