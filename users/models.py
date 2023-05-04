from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):

        if not email:
            raise ValueError('이메일은 필수 항목입니다.')

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None):
        superuser = self.create_user(
            email=email,
            password=password,
        )
        superuser.is_superuser = True
        superuser.is_admin = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    GENDERS = (
        ('M', 'Men'),
        ('W', 'Women'),
    )
    age = models.PositiveIntegerField(null=True)
    name = models.CharField(null=False, blank=False, max_length=50)
    gender = models.CharField(choices=GENDERS, max_length=10)
    introduction = models.TextField(null=True, blank=True)
    address = models.CharField("주소 수정")
    height = models.TextField("키 수정")
    weight = models.TextField("몸무게 수정")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
