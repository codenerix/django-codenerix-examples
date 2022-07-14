from django.test import TestCase
from django.contrib.auth.models import User

from .models import Person
from .views import PersonList


class PersonTestCase(TestCase):

    def setUp(self):
        u = User.objects.create_user(username="a1234", email='a@a.com', password='12345678')
        u.save()
        Person.objects.create(user=u, name='ahola', surname='aadios')
        p = Person(name='bhola', surname='badios')
        p.presave('b1234', '12345678', 'b@b.com', '12345678')
        p.save()
        '''Verifica que se obtienen los objetos y comprueba si son correctos'''

    def test_uno(self):

        a = Person.objects.get(name="ahola")
        b = Person.objects.get(name="bhola")
        self.assertEqual(a.user.username, 'a1234')
        self.assertEqual(b.user.username, 'b1234')
        return 'The %s says "%s"' % (a, b)

    def test_PersonListModel(self):
        u = PersonList.model.objects.get(name="ahola")
        self.assertEqual(u.user.username, 'a1234')
