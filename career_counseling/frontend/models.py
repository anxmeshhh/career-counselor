from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, aadhaar_no, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, aadhaar_no=aadhaar_no, **extra_fields)
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, aadhaar_no, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, full_name, aadhaar_no, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # Remove username field since email will be used for login
    full_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    aadhaar_no = models.CharField(max_length=12, unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fixing conflicts by setting unique related_name values
    groups = models.ManyToManyField(
        Group,
        related_name="custom_users",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_users_permissions",
        blank=True
    )

    USERNAME_FIELD = "email"  # Email will be used as the unique identifier
    REQUIRED_FIELDS = ["full_name", "aadhaar_no"]  # Fields required when creating a superuser

    objects = CustomUserManager()  # Set custom manager

    class Meta:
        db_table = "users"  # Explicit table name

    def __str__(self):
        return self.email
