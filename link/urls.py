from django.conf.urls import url

from link.views import LinkBlock

urlpatterns = [

    url('structure/', LinkBlock.as_view()),
    url('check_structure/', LinkBlock.as_view())

]
