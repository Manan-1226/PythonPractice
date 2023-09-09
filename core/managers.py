from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(
        self, username, password, is_staff, is_superuser, **extra_fields
    ):
        if not username or not password:
            raise ValueError(
                "The given username, password, is_staff, is_superuser must be set"
            )

        user = self.model(
            username=username,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
