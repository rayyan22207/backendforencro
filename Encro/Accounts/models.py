from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=125, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Add your custom fields here

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

################profile area###################
    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sent_friend_requests'  # Unique related_name
    )
    to_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='received_friend_requests'  # Unique related_name
    )
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')],
        default='pending'
    )


class Profile(models.Model):
    CODING = 'coding'
    EATING = 'eating'
    SINGING_DANCING = 'singing/dancing'
    READING = 'reading'
    CUSTOM = 'custom'
    HOBBY_CHOICES = [
        (CODING, 'Coding'),
        (EATING, 'Eating'),
        (SINGING_DANCING, 'Singing/Dancing'),
        (READING, 'Reading'),
        (CUSTOM, 'Custom'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='pics/pfp_image', default='Default_pfp.jpg', blank=True, null=True)
    Friends = models.ManyToManyField(
        'self',
        symmetrical=True,
    )
    Restriced_Friends = models.ManyToManyField(
        'self',
        related_name='restriced_by',
        symmetrical=False,
        blank=True
    )
    Blocked_Friends = models.ManyToManyField(
        'self',
        related_name='Blocked_by',
        symmetrical=False, blank=True
    )
    Used_to_be_Friends = models.ManyToManyField(
        'self',
        symmetrical=True,
        related_name='was_friends_with', blank=True
    )
    bio = models.TextField(max_length=500, blank=True, null=True)
    Name = models.CharField(max_length=100, blank=True, null=True)
    Hobbies = models.CharField(
        max_length=20,
        choices=HOBBY_CHOICES,
        default=CUSTOM,  # You can set the default choice to 'Custom' if you prefer.
        blank=True,     # Allow an empty (blank) value
        null=True,      # Allow a null value
    )
    def initialize_friends(self):
        # Initialize the Friends field when the profile is created
        self.Friends.add(self.user)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            user_profile = Profile(user=instance)
            user_profile.save()
            #user_profile.initialize_friends()  # Initialize Friends field

class UserSetting(models.Model):
    RED = 'red'
    BLUE = 'blue'
    NEON = 'neon'
    CUSTOM = 'custom'
    DARK = 'dark'
    LIGHT = 'light'
    THEMES = [
        (RED, 'Red'),
        (BLUE,'Blue'),
        (NEON, 'Neon'),
        (DARK, 'Dark'),
        (LIGHT, 'Light'),
        (CUSTOM, 'Custom (not working at the moment)'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_settings')
    color_theme = models.CharField(
        max_length=20,
        choices=THEMES,
        default=DARK,
        blank=True,
        null=True,
    )
    activity_status = models.BooleanField(default=True)