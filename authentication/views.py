from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from authentication.serializers import AuthTokenSerializer


class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    @swagger_auto_schema(   
        operation_id            = '토큰 발급(로그인)',
        operation_description   = '토큰을 가져오거나 발급 받습니다.',
        request_body            = serializer_class,
        responses               = {200: openapi.Response('', serializer_class)}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })