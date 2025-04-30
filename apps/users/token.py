from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.utils.timezone import now

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    """
    Autentica usando email ou username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username_or_email = request.data.get('username', '').lower()
        password = request.data.get('password', '')

        user = EmailOrUsernameBackend().authenticate(request, username=username_or_email, password=password)

        if not user:
            return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)

        name = f'{user.first_name} {user.last_name}'

        return Response({
            'token': token.key,
            'name': name,   
            'image': user.image.url
        }, status=status.HTTP_200_OK)