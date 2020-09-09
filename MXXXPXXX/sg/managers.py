from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, name, email, userid=None, password=None):
        if not email:
            raise ValueError('must have user email')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            userid=userid,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, userid, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            userid=userid,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user
