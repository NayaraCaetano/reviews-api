import random, string

from django.test import TestCase

from faker import Faker

from model_mommy.recipe import Recipe, seq, foreign_key

from rest_framework.test import APIClient

from authentication.models import User
from review.models import Company, Review


class BaseTestCase(TestCase):
    auth_user = None

    def setUp(self):
        self.client = APIClient()
        self.faker = Faker('pt_BR')
        self.init_recipes()

    def get_auth_user(self):
        return self.auth_user

    def authenticate(self, user=None):
        self.client.force_authenticate(user=self.auth_user)

    def init_recipes(self):
        self._user_recipe = Recipe(
            User,
            first_name=self.faker.first_name,
            email=self.faker.email,
            password=self.faker.password,
        )

        self.auth_user = self._user_recipe.make()

        self._company_recipe = Recipe(
            Company,
            name=self.faker.company,
            company_id=seq(1),
            website=self.faker.uri
        )

        self._review_recipe = Recipe(
            Review,
            rating=5,
            title=self.faker.sentence,
            summary=self.faker.paragraph,
            ip_address=self.faker.ipv4,
            company=foreign_key(self._company_recipe),
            reviewer=self.get_auth_user
        )


def generate_string_with_size(size):
    return ''.join(random.choice(string.ascii_lowercase) for x in range(size))
