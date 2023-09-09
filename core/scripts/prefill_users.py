from core.models import User, UserProfile
from django.contrib.auth.hashers import make_password

user, _ = User.objects.update_or_create(
    username="sahil.garg@daffodilsw.com",
    password=make_password("Hrhk@4321"),
    phone_number="9467483188",
    country_code="+91",
)
UserProfile.objects.update_or_create(
    user=user,
    defaults={
        "first_name": "Sahil",
        "last_name": "Garg",
        "email": "sahil.garg@daffodilsw.com",
    },
)

print("Created Login User")
# exec(open('core/scripts/prefill_users.py').read())
