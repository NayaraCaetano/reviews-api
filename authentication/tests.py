import pytest

from django.utils.translation import ugettext_lazy as _

from parameterized import parameterized

from rest_framework.reverse import reverse_lazy

from authentication.models import User
from authentication.serializers import UserSignInSerializer
from reviews_api.tests import BaseTestCase


class LoginIntegrationTestCase(BaseTestCase):
    URL = reverse_lazy('user_login')

    def _create_user(self, email, password):
        user = self._user_recipe.make(email=email)
        user.set_password(password)
        user.save()
        return user

    @parameterized.expand([
        ({'email': 'test@test.com', 'password': ''},),
        ({'email': '', 'password': '1234qwert'},)
    ])
    def test_user_try_log_in_without_one_of_the_required_fields(self, data):
        self._create_user('test@test.com', '1234qwert')
        response = self.client.post(self.URL, data)
        self.assertEquals(400, response.status_code)

    @parameterized.expand([
        ({'email': 'incorrect@test.com', 'password': '1234qwert'},),
        ({'email': 'test@test.com', 'password': 'incorrect'},)
    ])
    def test_user_try_log_in_with_invalid_credentials(self, data):
        self._create_user('test@test.com', '1234qwert')
        response = self.client.post(self.URL, data)
        self.assertEquals(400, response.status_code)

    def test_successful_auth_must_return_the_user_auth_token(self):
        data = {'email': 'test@test.com', 'password': '1234qwert'}
        self._create_user(**data)
        response = self.client.post(self.URL, data)
        self.assertTrue(response.json().get('token') is not None)

    def test_doesnt_need_authentication(self):
        data = {'email': 'test@test.com', 'password': '1234qwert'}
        self._create_user(**data)
        response = self.client.post(self.URL, data)
        self.assertFalse(response.status_code is 401)


class SignInTestCase(BaseTestCase):
    URL = reverse_lazy('user_sign_in')

    def _default_signin_data(self, *args, **kwargs):
        password = self.faker.password()
        return {
            'email': kwargs.pop('email', 'test@test.com'),
            'first_name': kwargs.pop('first_name', self.faker.first_name()),
            'last_name': kwargs.pop('last_name', ''),
            'password': kwargs.pop('password', password),
            'confirm_password':  kwargs.pop('confirm_password', password)
        }

    def test_cant_update_user_using_sign_in_serializer(self):
        user = self._user_recipe.make()
        serializer = UserSignInSerializer(user, self._default_signin_data())
        with pytest.raises(Exception) as excinfo:
            serializer.save()
            self.assertEquals(excinfo.msg, _('You can\'t edit a user here!'))

    def test_validation_if_user_send_different_password_and_confirm(self):
        data = self._default_signin_data(confirm_password='invalid')
        serializer = UserSignInSerializer(data=data)
        serializer.is_valid()
        self.assertTrue(
            _('The passwords must be the same.') in serializer.errors.get('non_field_errors')
        )

    @parameterized.expand([
        ('12a', _('This password is too short. It must contain at least 8 characters.')),
        ('123456789', _('This password is entirely numeric.')),
    ])
    def test_validate_password(self, password, message):
        data = self._default_signin_data(
            password=password,
            confirm_password=password
        )
        serializer = UserSignInSerializer(data=data)
        serializer.is_valid()
        self.assertTrue(message in serializer.errors.get('password'))

    @parameterized.expand([
        ('test@test.com', _('user with this Email address already exists.')),
        ('invalid', _('Enter a valid email address.')),
    ])
    def test_validate_email(self, email, message):
        self._user_recipe.make(email=email)
        data = self._default_signin_data(email=email)
        serializer = UserSignInSerializer(data=data)
        serializer.is_valid()
        self.assertTrue(message in serializer.errors.get('email'))

    def test_serializer_fields(self):
        data = self._default_signin_data()
        serializer = UserSignInSerializer(data=data)
        serializer.is_valid()
        del data['password']
        del data['confirm_password']
        self.assertEquals(data.keys(), serializer.data.keys())

    @parameterized.expand([
        ('email',),
        ('first_name',),
        ('password',),
        ('confirm_password',)
    ])
    def test_required_fields(self, field):
        data = self._default_signin_data()
        del data[field]
        serializer = UserSignInSerializer(data=data)
        serializer.is_valid()
        self.assertTrue(_('This field is required.') in serializer.errors.get(field))

    @parameterized.expand([
        ('last_name',)
    ])
    def test_non_required_fields(self, field):
        data = self._default_signin_data()
        del data[field]
        serializer = UserSignInSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    @parameterized.expand([
        ('password',),
        ('confirm_password',)
    ])
    def test_write_only_fields(self, field):
        user = self._user_recipe.make()
        serializer = UserSignInSerializer(user)
        self.assertFalse(serializer.to_representation(user).get(field))

    def test_create_user(self):
        data = self._default_signin_data()
        serializer = UserSignInSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        self.assertTrue(User.objects.get(email=data['email']))

    @parameterized.expand([
        ('is_staff',),
        ('is_superuser',)
    ])
    def test_cant_create_admin_or_staff_user(self, field):
        data = self._default_signin_data()
        data[field] = True
        serializer = UserSignInSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        user = User.objects.get(email=data['email'])
        self.assertFalse(user.__getattribute__(field))

    def test_user_password_is_setted_correctly(self):
        data = self._default_signin_data()
        serializer = UserSignInSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        user = User.objects.get(email=data['email'])
        self.assertTrue(user.check_password, data['password'])

    def test_user_sign_in_by_api(self):
        data = self._default_signin_data()
        response = self.client.post(self.URL, data)
        self.assertEquals(201, response.status_code)

    @parameterized.expand([
        ('get',),
        ('put',),
        ('delete')
    ])
    def test_only_post_method_is_allowed(self, method):
        data = self._default_signin_data()
        response = self.client.__getattribute__(method)(self.URL, data)
        self.assertEquals(405, response.status_code)

    def test_validations_messages_is_returned_to_user(self):
        data = self._default_signin_data()
        del data['email']
        response = self.client.post(self.URL, data)
        self.assertTrue(
            _('This field is required.') in response.json()['email']
        )

    def test_http_status_code_400_is_returned_if_validation_fails(self):
        data = self._default_signin_data()
        del data['email']
        response = self.client.post(self.URL, data)
        self.assertEquals(
            400,
            response.status_code
        )

    def test_doesnt_need_authentication(self):
        data = self._default_signin_data()
        response = self.client.post(self.URL, data)
        self.assertFalse(401 is response.status_code)


class UserObjectManagerTestCase(BaseTestCase):

    def test_create_user(self):
        User.objects.create_user('test@test.com', '1234qwert')
        self.assertTrue(User.objects.filter(email='test@test.com', is_superuser=False))

    def test_create_super_user(self):
        User.objects.create_superuser('test@test.com', '1234qwert')
        self.assertTrue(User.objects.filter(email='test@test.com', is_superuser=True))

    def test_create_staff_user(self):
        User.objects.create_user('test@test.com', '1234qwert', is_staff=True)
        self.assertTrue(User.objects.filter(email='test@test.com', is_staff=True))

    def test_password_is_set_corretly(self):
        User.objects.create_user('test@test.com', '1234qwert')
        user = User.objects.get(email='test@test.com')
        self.assertTrue(user.check_password('1234qwert'))

    def test_tries_to_create_user_without_email(self):
        with pytest.raises(Exception) as excinfo:
            User.objects.create_user(password='1234qwert')
            self.assertEquals(excinfo.msg, _('The given email must be set'))

    def test_tries_to_create_superuser_without_staff_status(self):
        with pytest.raises(Exception) as excinfo:
            User.objects.create_superuser('test@test.com', '1234qwert', is_staff=False)
            self.assertEquals(excinfo.msg, _('Superuser must have is_staff=True.'))

    def test_tries_to_create_superuser_without_superuser_status(self):
        with pytest.raises(Exception) as excinfo:
            User.objects.create_superuser('test@test.com', '1234qwert', is_superuser=False)
            self.assertEquals(excinfo.msg, _('Superuser must have is_superuser=True.'))
