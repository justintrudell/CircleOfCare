from django.db import models
from django.utils import timezone
from FunctionalApps import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MaxValueValidator, RegexValidator, EmailValidator
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from abc import ABCMeta, abstractmethod
from collections import defaultdict


class D3Queryable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def summary_boolean_fields(self):
        pass

    @staticmethod
    def produce_symptom_dictionary(query_set):
        """ Used by d3.js to visualize symptoms """
        # All items of query_set should have the same length,
        # so just ensure that the entire set and the first item are valid
        if not query_set or not query_set[0]:
            return {}
        # Create dictionary based on amount of boolean fields for this model
        data_dict = defaultdict(int)
        for item in query_set:
            fields = item.summary_boolean_fields()
            for i in range(len(fields)):
                name, val = fields[i]
                data_dict[name] += 1 if val else 0
        return [({"Category": k, "Frequency": v}) for k, v in sorted(data_dict.items())]


class PhysioSymptom(models.Model, D3Queryable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    tingling = models.BooleanField(blank=True)
    muscle_spasms = models.BooleanField(blank=True)
    dizziness = models.BooleanField(blank=True)
    muscle_weakness = models.BooleanField(blank=True)
    blurry_vision = models.BooleanField(blank=True)
    bladder_dysfunc = models.BooleanField(blank=True)
    bowel_dysfunc = models.BooleanField(blank=True)
    pain_bool = models.BooleanField(blank=True)
    other_issues = models.CharField(max_length=80, blank=True)
    pain_rating = models.IntegerField(choices=[(x, x) for x in range(1, 11)], blank=True, null=True)
    pain_location = models.CharField(max_length=100, blank=True)
    depression = models.BooleanField(blank=True)
    lack_interest = models.BooleanField(blank=True)
    feelings = models.CharField(max_length=1000, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def summary_boolean_fields(self):
        return [(PhysioSymptom._meta.get_field("tingling").verbose_name.title(), self.tingling),
                (PhysioSymptom._meta.get_field("muscle_spasms").verbose_name.title(), self.muscle_spasms),
                (PhysioSymptom._meta.get_field("dizziness").verbose_name.title(), self.dizziness),
                (PhysioSymptom._meta.get_field("muscle_weakness").verbose_name.title(), self.muscle_weakness),
                (PhysioSymptom._meta.get_field("blurry_vision").verbose_name.title(), self.blurry_vision),
                (PhysioSymptom._meta.get_field("bladder_dysfunc").verbose_name.title(), self.bladder_dysfunc),
                (PhysioSymptom._meta.get_field("bowel_dysfunc").verbose_name.title(), self.bowel_dysfunc),
                (PhysioSymptom._meta.get_field("pain_bool").verbose_name.title(), self.pain_bool),
                (PhysioSymptom._meta.get_field("depression").verbose_name.title(), self.depression),
                (PhysioSymptom._meta.get_field("lack_interest").verbose_name.title(), self.lack_interest)]


class FunctionalSymptom(models.Model, D3Queryable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    changing_clothes = models.BooleanField(blank=True)
    out_of_bed = models.BooleanField(blank=True)
    climbing_stairs = models.BooleanField(blank=True)
    cooking = models.BooleanField(blank=True)
    driving = models.BooleanField(blank=True)
    walking = models.BooleanField(blank=True)
    writing = models.BooleanField(blank=True)
    other_issues_physical = models.CharField(max_length=80, blank=True)
    learning_new_info = models.BooleanField(blank=True)
    remembering_tasks = models.BooleanField(blank=True)
    loss_for_words = models.BooleanField(blank=True)
    concentrating = models.BooleanField(blank=True)
    other_issues_cognitive = models.CharField(max_length=80, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def summary_boolean_fields(self):
        return [(FunctionalSymptom._meta.get_field("changing_clothes").verbose_name.title(), self.changing_clothes),
                (FunctionalSymptom._meta.get_field("out_of_bed").verbose_name.title(), self.out_of_bed),
                (FunctionalSymptom._meta.get_field("climbing_stairs").verbose_name.title(), self.climbing_stairs),
                (FunctionalSymptom._meta.get_field("cooking").verbose_name.title(), self.cooking),
                (FunctionalSymptom._meta.get_field("driving").verbose_name.title(), self.driving),
                (FunctionalSymptom._meta.get_field("walking").verbose_name.title(), self.walking),
                (FunctionalSymptom._meta.get_field("writing").verbose_name.title(), self.writing),
                (FunctionalSymptom._meta.get_field("learning_new_info").verbose_name.title(), self.learning_new_info),
                (FunctionalSymptom._meta.get_field("remembering_tasks").verbose_name.title(), self.remembering_tasks),
                (FunctionalSymptom._meta.get_field("loss_for_words").verbose_name.title(), self.loss_for_words),
                (FunctionalSymptom._meta.get_field("concentrating").verbose_name.title(), self.concentrating)]


class PhysicalActivity(models.Model, D3Queryable):
    DURATION_CHOICES = (('0', 'Less than 15 minutes'), ('1', '15-30 minutes'),
                        ('2', '30-45 minutes'), ('3', '45-60 minutes'),
                        ('4', '60-90 minutes'), ('5', 'More than 90 minutes'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    running = models.BooleanField(blank=True)
    walking = models.BooleanField(blank=True)
    tennis = models.BooleanField(blank=True)
    soccer = models.BooleanField(blank=True)
    aerobics = models.BooleanField(blank=True)
    yoga = models.BooleanField(blank=True)
    other_exercises = models.CharField(max_length=80, blank=True)
    exercise_duration = models.CharField(choices=DURATION_CHOICES, max_length=1, default=None, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def summary_boolean_fields(self):
        return [(PhysicalActivity._meta.get_field("running").verbose_name.title(), self.running),
                (PhysicalActivity._meta.get_field("walking").verbose_name.title(), self.walking),
                (PhysicalActivity._meta.get_field("tennis").verbose_name.title(), self.tennis),
                (PhysicalActivity._meta.get_field("soccer").verbose_name.title(), self.soccer),
                (PhysicalActivity._meta.get_field("aerobics").verbose_name.title(), self.aerobics),
                (PhysicalActivity._meta.get_field("yoga").verbose_name.title(), self.yoga)]


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=254, unique=True, db_index=True, default='')
    first_name = models.CharField(_('first name'), max_length=30, blank=True, default='')
    last_name = models.CharField(_('last name'), max_length=30, blank=True, default='')
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    age = models.PositiveIntegerField(validators=[MaxValueValidator(120)], blank=True, default=1)
    address = models.CharField(max_length=80, blank=True, default='')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '999999999'.")
    phone_number = models.CharField(max_length=15, validators=[phone_regex], blank=True, default='')
    diagnosis = models.CharField(max_length=40, blank=True, default='')
    emergency_relationship = models.CharField(max_length=15, blank=True, default='')
    emergency_phone_number = models.CharField(max_length=15, validators=[phone_regex], blank=True, default='')
    emergency_email = models.CharField(max_length=40, validators=[EmailValidator], blank=True, default='')
    emergency_name = models.CharField(max_length=30, blank=True, default='')

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
