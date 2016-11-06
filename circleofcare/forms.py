from django import forms
from FunctionalApps import settings
from django.forms import ModelForm, Textarea
from circleofcare.models import PhysioSymptom, FunctionalSymptom, PhysicalActivity, UserProfile, CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class PhysioForm(ModelForm):
    class Meta:
        model = PhysioSymptom
        fields = ['tingling','muscle_spasms','dizziness','muscle_weakness','blurry_vision','bladder_dysfunc',
                  'bowel_dysfunc','pain_bool','other_issues','pain_rating','pain_location','depression',
                  'lack_interest', 'feelings']
        exclude = ['user']
        widgets = {
            'other_issues': forms.TextInput(attrs={'placeholder': 'Other?'})
        }

    def __init__(self, *args, **kwargs):
        super(PhysioForm, self).__init__(*args, **kwargs)


class FunctionalForm(ModelForm):
    class Meta:
        model = FunctionalSymptom
        fields = ['changing_clothes', 'out_of_bed', 'climbing_stairs', 'cooking', 'driving', 'walking', 'writing',
                  'other_issues_physical', 'learning_new_info', 'remembering_tasks', 'loss_for_words', 'concentrating',
                  'other_issues_cognitive']
        widgets = {
            'other_issues_physical': forms.TextInput(attrs={'placeholder': 'Other?'}),
            'other_issues_cognitive': forms.TextInput(attrs={'placeholder': 'Other?'})
        }

    def __init__(self, *args, **kwargs):
        super(FunctionalForm, self).__init__(*args, **kwargs)


class PhysicalActivityForm(ModelForm):
    class Meta:
        model = PhysicalActivity
        fields = ['running', 'walking', 'tennis', 'soccer', 'aerobics',
                  'yoga', 'other_exercises', 'exercise_duration']
        widgets = {
            'exercise_duration': forms.RadioSelect
        }

    def __init__(self, *args, **kwargs):
        super(PhysicalActivityForm, self).__init__(*args, **kwargs)


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'address', 'phone_number', 'diagnosis', 'emergency_name', 'emergency_email',
                  'emergency_phone_number', 'emergency_relationship']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': Textarea(attrs={'type': 'text'})
        }


class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_active')