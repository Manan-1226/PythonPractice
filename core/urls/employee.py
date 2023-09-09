from ..views.employee.employee import employee_view
from django.urls import path

urlpatterns = {
    path("v1/emp", employee_view(), name="employee"),
    path("v1/emp/<uuid:pk>", employee_view(), name="employee_update"),
}

# The format_suffix_pattern allows us to specify the data format (raw json or even html) when we use the URLs.
# It appends the format to be used to every URL in the pattern.
employee_urlpatterns = list(urlpatterns)
