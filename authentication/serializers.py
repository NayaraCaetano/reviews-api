from django.utils.translation import ugettext_lazy as _
import django.contrib.auth.password_validation as validators

from rest_framework import serializers

from authentication.models import User


class UserSignInSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'confirm_password')

    def validate_password(self, value):
        validators.validate_password(password=value)
        return value

    def validate(self, data):
        if data.get('password') != data.pop('confirm_password'):
            raise serializers.ValidationError(_('The passwords must be the same.'))
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        raise Exception(_('You can\'t edit a user here!'))
