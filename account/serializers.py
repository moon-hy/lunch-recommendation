import re

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from account.models import Profile


class LikeDislikeSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id'    : instance.id,
            'name'  : instance.name
        }

class ProfileSerializer(serializers.ModelSerializer):
    likes       = LikeDislikeSerializer('likes', many=True)
    dislikes    = LikeDislikeSerializer('dislikes', many=True)

    class Meta:
        model   = Profile
        fields  = [
            'nickname', 'likes', 'dislikes'
        ]

class UserListSerializer(serializers.ModelSerializer):
    profile     = ProfileSerializer('profile')

    class Meta:
        model   = User
        fields  = [
            'id', 'username', 'email', 'profile'
        ]

class UserDetailSerializer(serializers.ModelSerializer):
    profile     = ProfileSerializer('profile')
    username    = serializers.ReadOnlyField()
    email       = serializers.ReadOnlyField()

    class Meta:
        model   = User
        fields = [
            'id', 'username', 'email', 'profile'
        ]

class UserRegisterSerializer(serializers.ModelSerializer):
    user_id     = serializers.CharField(
        source      = 'username',
        write_only  = True,
        required    = True,
        validators  = [
            UniqueValidator(queryset=User.objects.all()),
            RegexValidator(regex=r"^[\w.]+\Z")
        ]
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
        model   = User
        fields  = [
            'user_id', 'nickname', 'password', 'password2'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username    = validated_data['username'],
        )
        user.profile.nickname = validated_data['nickname']

        user.set_password(validated_data['password'])
        user.save()
        return user
