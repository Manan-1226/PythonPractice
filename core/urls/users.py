from ..views import login_view
from django.urls import path

urlpatterns = {path("v1/login", login_view(), name="login")}
# The format_suffix_pattern allows us to specify the data format (raw json or even html) when we use the URLs.
# It appends the format to be used to every URL in the pattern.
users_urlpatterns = list(urlpatterns)
