from rest_framework import generics, status
from rest_framework.response import Response
from core.components import ErrorCode, ErrorHandling, UsersComponent
from core.serializers import UserLoginRequestSerializer
from core.models import User


class LoginView_API_2023_03_01(generics.GenericAPIView):
    serializer_class = UserLoginRequestSerializer

    def post(self, request):
        serializer = UserLoginRequestSerializer(data=request.data)
        if not serializer.is_valid():
            error_response = ErrorHandling.get_response(
                "USER_LOGIN_SERIALIZER_ERROR",
                ErrorCode.ERROR_HTTP_400_BAD_REQUEST,
                ErrorCode.ERROR_INVALID_OR_MISSING_ARGS_8001,
                serializer.errors,
            )
            return error_response

        data = dict(serializer.validated_data)

        username = data.get("username")
        password = data.get("password")

        users_component = UsersComponent()
        response: UsersComponent.Result = users_component.login(
            username=username, password=password
        )
        if not response.is_success:
            return response.errors
        jwt_token = User.generate_jwt_token()
        response["Authorization"] = jwt_token
        return Response(response.result, status=status.HTTP_200_OK)
