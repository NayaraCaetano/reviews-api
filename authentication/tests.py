from reviews_api.tests import BaseTestCase

from rest_framework.reverse import reverse_lazy


class LoginIntegrationTestCase(BaseTestCase):
    URL = reverse_lazy('user_login')

    def test_user_try_log_in_without_one_of_the_required_fields(self):
        pass

    def test_user_try_log_in_with_invalid_credentials(self):
        pass

    def test_successful_auth_must_return_the_user_auth_token(self):
        pass

    def test_doesnt_need_authentication(self):
        pass


class SignInUnitTestCase(BaseTestCase):

    def test_user_cant_update_user_using_sign_in_serializer(self):
        pass

    def test_validation_if_user_send_different_password_and_confirm(self):
        pass

    def test_validate_password(self):
        pass

    def test_validate_unique_email(self):
        pass

    def test_serializer_fields(self):
        pass

    def test_required_fields(self):
        pass

    def test_non_required_fields(self):
        pass

    def test_password_isnt_showed_if_list_serializer(self):
        pass

    def test_create_user(self):
        pass

    def test_cant_create_admin_or_staff_user(self):
        pass

    def test_created_user_isnt_admin_or_staff(self):
        pass

    def test_user_password_is_setted_correctly(self):
        pass


class SignInIntegrationTestCase(BaseTestCase):
    URL = reverse_lazy('user_signin')

    def test_user_sign_in_by_api(self):
        pass

    def test_only_create_method_is_allowed(self):
        pass

    def test_validations_messages_is_returned_to_user(self):
        pass

    def test_http_status_code_400_is_returned_if_validation_fails(self):
        pass

    def test_doesnt_need_authentication(self):
        pass
