from django.conf.urls import url
from .views import AuthBlock

urlpatterns = [

    url('login/', AuthBlock.as_view()),

]
