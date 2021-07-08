from django.test import Client
from django.test import TestCase

c = Client()


class LinkBlockTest(TestCase):

    def test_first_task(self):
        res = '{"html":1,"head":1,"body":1,"p":0,"img":1}'

        response = c.get('/structure/')
        self.assertEquals(response.content.decode('utf-8'), res)

    def test_second_task(self):
        res1 = '{"html":1,"head":1,"body":1,"p":0,"img":23}'
        res2 = '"Incorrect link"'

        right = c.get('/structure/', {"link": "https://mail.ru/"})
        wrong = c.get('/structure/', {"link": "testurl"})

        self.assertEquals(right.content.decode('utf-8'), res1)
        self.assertEquals(wrong.content.decode('utf-8'), res2)

    def test_third_task(self):
        res = '{"html":1,"body":1}'

        response = c.get('/structure/', {"link": "https://mail.ru/", "tags": "html,body"})
        self.assertEquals(response.content.decode('utf-8'), res)
