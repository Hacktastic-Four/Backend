from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save()
        return 

# Create your models here.
class CustomUser(AbstractBaseUser):
    email = models.EmailField("email", max_length=254, unique=True)
    first_name = models.CharField("first_name", max_length=50)
    last_name = models.CharField("last_name", max_length=50)
    rating = models.FloatField("rating", blank=True, null=True)
    profile = models.TextField("profile", blank=True, null=True)
    skills = models.TextField("skills", blank=True, null=True)
    profile_picture = models.ImageField(default='default.jpeg', upload_to='profile_pics',null=True, blank=True)
    verified = models.BooleanField(default=False)
    rating_count = models.IntegerField('rating_count', default=0)

    USERNAME_FIELD = 'email'


    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
class EmailsHandler(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email_verf = models.UUIDField('email_verf', blank=True,null=True)
    pass_verf = models.UUIDField('pass_verf', blank=True,null=True)

    def __str__(self) -> str:
        return self.user.email

