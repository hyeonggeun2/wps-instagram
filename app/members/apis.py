from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import User
from members.serializers import UserSerializer


class AuthTokenAPIView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        users = [user.username for user in User.objects.all()]

        if username in users:
            print('true')
        else:
            print('false')

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
        else:
            raise AuthenticationFailed()

        serializer = UserSerializer(user)
        data = {
            'token': token.key,
            'user': serializer.data,
        }

        return Response(data)

    def get(self, request):
        data = {
            'token': request.auth
        }

        return Response(data)
