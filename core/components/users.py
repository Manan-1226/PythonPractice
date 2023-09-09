from core.models import User
from core.components import ErrorCode, ErrorHandling
from django.contrib.auth.hashers import check_password
from core.serializers import UserInformationSerializer, UserProfileInformationSerializer


class UsersComponent:
    def __init__(self):
        pass

    # object to return with results
    class Result:
        def __init__(self, is_success, errors, result=None):
            self.is_success = is_success
            self.errors = errors
            self.result = result

    def login(self, username: str, password: str):
        users_qs = User.objects.filter(username=username)
        if not users_qs.exists():
            error_response = ErrorHandling.get_response(
                "LOGIN_ERROR",
                ErrorCode.ERROR_HTTP_400_BAD_REQUEST,
                ErrorCode.ERROR_INVALID_OR_MISSING_ARGS_8001,
                "INVALID_USER_EMAIL",
            )
            return UsersComponent.Result(False, error_response)

        user: User = users_qs.first()
        if not check_password(password, user.password):
            error_response = ErrorHandling.get_response(
                "LOGIN_ERROR",
                ErrorCode.ERROR_HTTP_400_BAD_REQUEST,
                ErrorCode.ERROR_INVALID_OR_MISSING_ARGS_8001,
                "Password is incorrect",
            )
            return UsersComponent.Result(False, error_response)

        user_info = {
            "token": user.user_token(),
            "user": UserInformationSerializer(user).data,
            "profile": UserProfileInformationSerializer(user.user_profile).data,
        }

        return UsersComponent.Result(True, None, user_info)
