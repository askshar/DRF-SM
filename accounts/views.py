import uuid

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.models import User
from .serializers import CustomTokenObtainPairSerializer, UserSerializer, UserProfileSerializer
from .models import UserConfig, UserPasswordHistoryMananger, UserProfile
from posts.models import Post
from posts.serializers import PostSerializer
from config.email import send_email
from config.validators import password_validator, password_history_validator


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]


class UserProfileAPI(APIView):
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"Error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        profile = UserProfile.objects.filter(user=user).first()
        profile_serializer = UserProfileSerializer(profile).data

        posts = Post.objects.filter(user=user)
        post_serializer = PostSerializer(posts, many=True).data

        data = {
            'profile': profile_serializer,
            'posts': post_serializer
        }
        return Response(data, status=status.HTTP_200_OK)


class UserAccountVerificationAPI(APIView):
    """
    API to activate user account.
    """
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        unique_token = request.query_params.get('token')
        if unique_token:
            user_conf = UserConfig.objects.filter(
                token=unique_token).first()
            if user_conf:
                user_conf.user.is_active = True
                user_conf.user.save()

                user_conf.token = None
                user_conf.save()
                return Response({"Success": "Your account has been activated."}, status=status.HTTP_200_OK)
            return Response({"Info": "Invalid Token."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"TokenError": "Token not found."}, status=status.HTTP_404_NOT_FOUND)


class UserReVerificationAPI(APIView):
    """
    API to generate new token to verify user account if user fails to activate on registration.
    """
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        email_id = request.POST.get('email')
        if not email_id:
            return Response({'Error': 'Please provide email id.'}, status=status.HTTP_400_BAD_REQUEST)

        instance = User.objects.filter(email=email_id).first()
        if not instance:
            return Response({"Error": "Account not found with provided email id."})

        if not instance.is_active:
            unique_token = uuid.uuid4()

            verification_link = f'http://localhost:8000/api/verify/?token={unique_token}'

            subject = "Account Verification"
            message = f"""
                                Click on the link below to verify your account.
    
                                {verification_link}
                                """
            send_email(instance, unique_token, verification_link, subject, message)
            return Response(
                    {"Success": "Verification email has been sent."},
                    status=status.HTTP_200_OK
                )
        return Response(
                {"Info": "Your account is already activated."},
                status=status.HTTP_400_BAD_REQUEST
            )


class ForgetPasswordAPI(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        if not email:
            return Response(
                    {"Error": "Please enter your email id."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        instance = User.objects.filter(email=email).first()
        if not instance:
            return Response({"Error": "Account not found with provided email id."})

        try:
            unique_token = uuid.uuid4()

            verification_link = f'http://localhost:8000/api/password-reset/?token={unique_token}'

            subject = "Account Verification"
            message = f"""
                            Click on the link below to reset your password.
    
                            {verification_link}
                    """
            send_email(instance, unique_token, verification_link, subject, message)
            return Response(
                    {"Success": "Password reset link sent to your email."},
                    status=status.HTTP_200_OK
                )
        except:
            return Response(
                {"Error": "Error sending reset email currently, Please try after some time."},
                status=status.HTTP_400_BAD_REQUEST
            )


class PasswordResetAPI(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        new_password = request.POST.get('new_password')

        if not token:
            return Response(
                    {'Error': 'Token not found.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        if not new_password:
            return Response(
                    {'Error': 'Please enter your new password.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if not password_validator(new_password):
            return Response(
                {'Error': '''Password should be greater than or equals to 6 characters 
                and should contain atleast a letter a digit and a special character.'''},
                status=status.HTTP_400_BAD_REQUEST)

        user_conf = UserConfig.objects.filter(token=token).first()
        if user_conf:
            user = user_conf.user
            if password_history_validator(user=user, password=new_password):
                return Response({"Error": "This password has been used recently."},
                                status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()

            user_conf.token = None
            user_conf.save()

            UserPasswordHistoryMananger.objects.create(
                user=user,
                password=new_password
            )
            return Response({"Success": "Password has been changed."}, status=status.HTTP_200_OK)
        return Response({"Error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
