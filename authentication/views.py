import random
import re
import string

from rest_framework.response import Response
from rest_framework.views import APIView

auth_pass = {}


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class AuthBlock(APIView):
    def get(self, request):
        phone = request.GET.get('phone')
        phone_regex = re.compile(r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$")

        if not phone_regex.match(phone):
            return Response("Invalid phone number")

        code = id_generator()

        auth_pass.update({phone: code})

        return Response(code)

    def post(self, request):
        if request.POST.get("phone") in auth_pass.keys() and request.POST.get("code") in auth_pass.values():
            return Response({"status": "OK"})
        else:
            return Response({"status": "Fail"})
