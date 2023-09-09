from .users import users_urlpatterns
from .employee import employee_urlpatterns

urlpatterns = users_urlpatterns + employee_urlpatterns
