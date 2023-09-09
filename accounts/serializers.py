from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.models import User

from posts.serializers import PostSerializer

from .models import UserPasswordHistoryMananger, UserProfile


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        # an email will be sent to verify user account on given email to activate this flag True.
        user.is_active = False
        user.save()

        UserPasswordHistoryMananger.objects.create(
            user=user,
            password=validated_data['password']
        )
        return user

    def validate_email(self, value):
        email_part = value.split('@')[0]
        domain_part = value.split('@')[1]

        normalized_email = email_part.lower()+'@'+domain_part.lower()

        # Check if a user is already registered with this email
        valid_email = User.objects.filter(email=normalized_email).first()
        if valid_email:
            raise serializers.ValidationError('A user is already registered with this email id.')

        return normalized_email

    def validate_password(self, value):
        if not len(value) >= 6:
            raise serializers.ValidationError('Password should be greater or equals to 6 characters.')

        has_letter = any(char.isalpha() for char in value)
        has_number = any(char.isdigit() for char in value)
        has_symbol = any(char in '@#$&' for char in value)

        if not (has_letter and has_number and has_symbol):
            raise serializers.ValidationError(
                'Password should contain atleast a letter, a digit and a special charater [@/#/$/&].'
            )
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'user',
            'username',
            'email',
            'image',
            'post',
            'follower',
            'following',
        )

    def get_username(self, obj):
        return obj.user.username


    def get_email(self, obj):
        return obj.user.email
