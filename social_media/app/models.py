from django.contrib.auth.models import AbstractBaseUser, Group, Permission, UserManager, AbstractUser
from django.db import models


class AppUserManager(UserManager):
    def _create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **kwargs):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self._create_user(
            email,
            password=password,
            **kwargs
        )
        return user

class AppUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    objects = AppUserManager()




class FriendRequest(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    from_user = models.ForeignKey(AppUser, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(AppUser, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    def __str__(self):
        return f"From {self.from_user.email} to {self.to_user.email} - Status: {self.status}"

    @staticmethod
    def has_pending_request(from_user, to_user):
        return FriendRequest.objects.filter(from_user=from_user, to_user=to_user, status=FriendRequest.STATUS_CHOICES[0][0]).exists()
