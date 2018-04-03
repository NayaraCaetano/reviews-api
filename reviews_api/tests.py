from django.test import TestCase

from faker import Faker

from model_mommy.recipe import Recipe, seq

from rest_framework.test import APIClient

from authentication.models import User


class BaseTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.faker = Faker('pt_BR')

    def _user_recipe(self):
        return Recipe(
            User,
            first_name=self.faker.first_name(),
            email='email{num}@teste.com'.format(num=seq(15)),
            password=self.faker.password(),
        )
