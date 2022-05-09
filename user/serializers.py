from tabnanny import verbose
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from user.models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Profile
        fields  = [
            'nickname'
        ]

class UserListSerializer(serializers.ModelSerializer):
    profile     = ProfileSerializer('profile')

    class Meta:
        model   = User
        fields  = [
            'id', 'username', 'email', 'profile'
        ]

class UserDetailSerializer(serializers.ModelSerializer):
    #profile     = ProfileSerializer('profile')
    username    = serializers.ReadOnlyField()
    email       = serializers.ReadOnlyField()
    nickname    = serializers.CharField(
        source      = 'profile.nickname'
    )

    class Meta:
        model   = User
        fields = [
            'id', 'username', 'email', 'nickname',
        ]

class UserRegisterSerializer(serializers.ModelSerializer):
    email   = serializers.EmailField(
        required    = True,
        validators  = [UniqueValidator(queryset=User.objects.all())]
    )
    nickname    = serializers.CharField(
        write_only  = True,
        required    = True
    )
    password    = serializers.CharField(
        write_only  = True, 
        required    = True, 
        validators  = [validate_password]
    )
    password2   = serializers.CharField(
        write_only  = True,
        required    = True
    )

    class Meta:
        model = User
        fields = [
            'username', 'nickname', 'password', 'password2', 'email',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username    = validated_data['username'],
            email       = validated_data['email'],
        )
        user.profile.nickname = validated_data['nickname']

        user.set_password(validated_data['password'])
        user.save()
        return user
