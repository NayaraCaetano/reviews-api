from datetime import date

from django.utils.translation import ugettext_lazy as _

from parameterized import parameterized


from rest_framework.reverse import reverse_lazy

from reviews_api.tests import BaseTestCase, generate_string_with_size

from review.serializers import ReviewSerializer
from review.models import Company, Review


class ReviewTestCase(BaseTestCase):
    URL = reverse_lazy('reviews')

    def _default_review_data(self, *args, **kwargs):
        return {
            "rating": kwargs.pop('rating', 5),
            "title": kwargs.pop('title', self.faker.sentence()[:64]),
            "summary": kwargs.pop('summary', self.faker.paragraph()),
            "company": {
                "name": kwargs.pop('company__name', self.faker.company()),
                "company_id": kwargs.pop('company__company_id', self.faker.numerify()),
                "website": kwargs.pop('company__website', '')
            }
        }

    @parameterized.expand([
        (0, _('Ensure this value is greater than or equal to 1.')),
        (6, _('Ensure this value is less than or equal to 5.')),
    ])
    def test_validate_rating(self, value, message):
        data = self._default_review_data(rating=value)
        serializer = ReviewSerializer(data=data)
        serializer.is_valid()
        self.assertTrue(
            message in serializer.errors.get('rating')
        )

    @parameterized.expand([
        (generate_string_with_size(65), _('Ensure this field has no more than 64 characters.')),
    ])
    def test_validate_title(self, value, message):
        data = self._default_review_data(title=value)
        serializer = ReviewSerializer(data=data)
        serializer.is_valid()
        self.assertTrue(
            message in serializer.errors.get('title')
        )

    @parameterized.expand([
        (generate_string_with_size(10001), _('Ensure this field has no more than 10000 characters.')),
    ])
    def test_validate_summary(self, value, message):
        data = self._default_review_data(summary=value)
        serializer = ReviewSerializer(data=data)
        serializer.is_valid()
        self.assertTrue(
            message in serializer.errors.get('summary')
        )

    @parameterized.expand([
        ('a', _('A valid integer is required.')),
    ])
    def test_validate_company_id(self, value, message):
        data = self._default_review_data(company__company_id=value)
        serializer = ReviewSerializer(data=data)
        serializer.is_valid()
        self.assertTrue(
            message in serializer.errors.get('company').get('company_id')
        )

    @parameterized.expand([
        ('invalidowebsite', _('Enter a valid URL.')),
    ])
    def test_validate_company_website(self, value, message):
        data = self._default_review_data(company__website=value)
        serializer = ReviewSerializer(data=data)
        serializer.is_valid()
        self.assertTrue(
            message in serializer.errors.get('company').get('website')
        )

    def test_submission_date_is_automatically_setted_on_create(self):
        data = self._default_review_data()
        serializer = ReviewSerializer(data=data)
        serializer.is_valid()
        instance = serializer.save(ip_address=self.faker.ipv4(), reviewer=self._user_recipe.make())
        self.assertEquals(instance.submission_date, date.today())

    def test_serializer_fields(self):
        data = self._default_review_data()
        serializer = ReviewSerializer(data=data)
        serializer.is_valid()
        self.assertEquals(data.keys(), serializer.data.keys())

    @parameterized.expand([
        ('rating',),
        ('title',),
        ('summary',),
    ])
    def test_required_fields(self, field):
        data = self._default_review_data()
        del data[field]
        serializer = ReviewSerializer(data=data)
        serializer.is_valid()
        self.assertTrue(_('This field is required.') in serializer.errors.get(field))

    @parameterized.expand([
        ('name',),
        ('company_id',),
    ])
    def test_company_required_fields(self, field):
        data = self._default_review_data()
        del data['company'][field]
        serializer = ReviewSerializer(data=data)
        serializer.is_valid()
        self.assertTrue(_('This field is required.') in serializer.errors['company'].get(field))

    @parameterized.expand([
        ('website',),
    ])
    def test_company_non_required_fields(self, field):
        data = self._default_review_data()
        del data['company'][field]
        serializer = ReviewSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    @parameterized.expand([
        ('ip_address',),
        ('reviewer',),
        ('submission_date')
    ])
    def test_read_only_fields(self, field):
        review = self._review_recipe.make()
        serializer = ReviewSerializer(review)
        self.assertTrue(serializer.to_representation(review).get(field))

    def test_review_create_new_company_if_the_id_company_doesnt_exist(self):
        data = self._default_review_data()
        serializer = ReviewSerializer(data=data)
        serializer.is_valid()
        serializer.save(ip_address=self.faker.ipv4(), reviewer=self._user_recipe.make())
        self.assertEquals(Company.objects.count(), 1)

    def test_review_dont_create_new_company_if_the_id_company_exists(self):
        company = self._company_recipe.make()
        data = self._default_review_data(company__company_id=company.company_id)
        serializer = ReviewSerializer(data=data)
        serializer.is_valid()
        serializer.save(ip_address=self.faker.ipv4(), reviewer=self._user_recipe.make())
        self.assertEquals(Company.objects.count(), 1)

    def test_review_update_data_company_if_the_id_company_exists(self):
        company = self._company_recipe.make()
        data = self._default_review_data(
            company__company_id=company.company_id,
            company__name='new name'
        )
        serializer = ReviewSerializer(data=data)
        serializer.is_valid()
        review = serializer.save(ip_address=self.faker.ipv4(), reviewer=self._user_recipe.make())
        self.assertEquals(review.company.name, 'new name')

    def test_show_reviewer_str_name(self):
        review = self._review_recipe.make()
        serializer = ReviewSerializer(review)
        self.assertEquals(
            serializer.to_representation(review).get('reviewer'),
            str(review.reviewer)
        )

    def test_show_company_informations(self):
        review = self._review_recipe.make()
        serializer = ReviewSerializer(review)
        self.assertTrue(
            serializer.to_representation(review)['company'].get('name'),
        )

    def test_ip_request_getting(self):
        data = self._default_review_data()
        self.authenticate()
        self.client.post(self.URL, data, format='json')
        review = Review.objects.get(id=1)
        self.assertEquals(review.ip_address, '127.0.0.1')

    def test_reviewer_must_be_que_request_user(self):
        data = self._default_review_data()
        self.authenticate()
        self.client.post(self.URL, data, format='json')
        review = Review.objects.get(id=1)
        self.assertEquals(review.reviewer, self.auth_user)

    def test_reviewer_list_his_reviews(self):
        self.authenticate()
        review = self._review_recipe.make()
        response = self.client.get(self.URL)
        self.assertEquals(
            ReviewSerializer(review).to_representation(review),
            response.json()[0]
        )

    def test_user_only_can_see_his_reviews(self):
        self.authenticate()
        self._review_recipe.make()
        self._review_recipe.make()
        another_user = self._user_recipe.make()
        self._review_recipe.make(reviewer=another_user)
        response = self.client.get(self.URL)
        self.assertEquals(
            len(response.json()),
            2
        )

    def test_http_status_code_400_is_returned_if_validation_fails(self):
        data = self._default_review_data()
        del data['title']
        self.authenticate()
        response = self.client.post(self.URL, data, format='json')
        self.assertEquals(
            400,
            response.status_code
        )

    def test_validations_messages_is_returned_to_user(self):
        data = self._default_review_data()
        del data['title']
        self.authenticate()
        response = self.client.post(self.URL, data, format='json')
        self.assertTrue(
            _('This field is required.') in response.json()['title']
        )

    @parameterized.expand([
        ('put',),
        ('delete')
    ])
    def test_only_post_and_get_method_is_allowed(self, method):
        data = self._default_review_data()
        self.authenticate()
        response = self.client.__getattribute__(method)(self.URL, data, format='json')
        self.assertEquals(405, response.status_code)

    def test_user_must_be_autenticated(self):
        data = self._default_review_data()
        response = self.client.post(self.URL, data, format='json')
        self.assertEquals(401, response.status_code)
