from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from circleofcare.models import UserProfile, FunctionalSymptom, PhysicalActivity, PhysioSymptom
from django.core.exceptions import ObjectDoesNotExist
from contextlib import suppress
import json

from .forms import PhysioForm, FunctionalForm, PhysicalActivityForm, UserProfileForm,CustomUserCreationForm

# Used to properly handle next page requests when a user navigates to a page without having logged in
next_addr = ""


@login_required
def physiological_log(request):
    # If this is a POST request we need to process the form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = PhysioForm(request.POST)
        # Check whether it's valid - if not, return them without success message
        if form.is_valid():
            result = form.save(commit=False)
            result.user = request.user
            result.save()
            messages.success(request, "Your information was successfully saved. Thanks!")
        else:
            #TODO: Handle this error gracefully
            print("Physio Log Error")
            pass
        return HttpResponseRedirect(reverse('circleofcare:index'))
    # Otherwise create a blank form
    else:
        form = PhysioForm()

    return render(request, 'circleofcare/physiological_log.html', {'form': form})


@login_required(redirect_field_name=None)
def index(request):
    return render(request, 'circleofcare/cc_index.html')


@login_required
def functional_log(request):
    # If this is a POST request we need to process the form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = FunctionalForm(request.POST)
        # Check whether it's valid - if not, return them without success message
        if form.is_valid():
            result = form.save(commit=False)
            result.user = request.user
            result.save()
            messages.success(request, "Your information was successfully saved. Thanks!")
        else:
            # TODO: Handle this error gracefully
            print("Functional Log Error")
            pass
        return HttpResponseRedirect(reverse('circleofcare:index'))
    # Otherwise create a blank form
    else:
        form = FunctionalForm()

    return render(request, 'circleofcare/functional_log.html', {'form': form})


@login_required
def physical_activity_log(request):
    # If this is a POST request we need to process the form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = PhysicalActivityForm(request.POST)
        # Check whether it's valid - if not, return them without success message
        if form.is_valid():
            result = form.save(commit=False)
            result.user = request.user
            result.save()
            messages.success(request, "Your information was successfully saved. Thanks!")
        else:
            # TODO: Handle this error gracefully
            print("Physical Activity Error")
            pass
        return HttpResponseRedirect(reverse('circleofcare:index'))
    # Otherwise create a blank form
    else:
        form = PhysicalActivityForm()

    return render(request, 'circleofcare/physical_activity_log.html', {'form': form})


@login_required
def user_profile(request):
    main_profile = request.user
    custom_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        custom_update = UserProfileForm(request.POST, instance=custom_profile)
        if custom_update.is_valid():
            custom_update.save()
        return HttpResponseRedirect(reverse('circleofcare:user_profile'), {'user_profile': main_profile,
                                                                           'custom_profile': custom_profile,
                                                                           'custom_update': custom_update})
    else:
        custom_update = UserProfileForm({'address': custom_profile.address,
                                         'age': custom_profile.age,
                                         'phone_number': custom_profile.phone_number,
                                         'diagnosis': custom_profile.diagnosis,
                                         'emergency_name': custom_profile.emergency_name,
                                         'emergency_email': custom_profile.emergency_email,
                                         'emergency_phone_number': custom_profile.emergency_phone_number,
                                         'emergency_relationship': custom_profile.emergency_relationship})
    return render(request, 'circleofcare/user_profile.html', {'user_profile': main_profile,
                                                              'custom_profile': custom_profile,
                                                              'custom_update': custom_update})


@login_required
def user_summary(request):
    user = request.user

    return render(request, 'circleofcare/user_summary.html')


@login_required(redirect_field_name=None)
def physiological_data(request):
    user = request.user
    physio_values = None

    if request.method == 'GET':
        with suppress(ObjectDoesNotExist):
            physio_symptoms = PhysioSymptom.objects.filter(user=user, date__gt=retrieve_days_delta(14))
        physio_values = PhysioSymptom.produce_symptom_dictionary(physio_symptoms)

    return JsonResponse(physio_values, safe=False)


@login_required(redirect_field_name=None)
def functional_data(request):
    user = request.user
    functional_values = None

    if request.method == 'GET':
        with suppress(ObjectDoesNotExist):
            functional_symptoms = FunctionalSymptom.objects.filter(user=user, date__gt=retrieve_days_delta(14))
        functional_values = FunctionalSymptom.produce_symptom_dictionary(functional_symptoms)

    return JsonResponse(functional_values, safe=False)


@login_required(redirect_field_name=None)
def physical_data(request):
    user = request.user
    physical_values = None

    if request.method == 'GET':
        with suppress(ObjectDoesNotExist):
            physical_symptoms = PhysicalActivity.objects.filter(user=user, date__gt=retrieve_days_delta(14))
        physical_values = PhysicalActivity.produce_symptom_dictionary(physical_symptoms)

    return JsonResponse(physical_values, safe=False)


@login_required(redirect_field_name=None)
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('circleofcare:login'))


def register(request):
    # Changed to True when registration succeeds.
    registered = False

    if request.method == 'POST':
        user_form = CustomUserCreationForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database - password is already taken care of.
            user = user_form.save()

            # Now sort out the UserProfile instance.
            profile = profile_form.save(commit=False)
            profile.user = user
            if not profile.age:
                profile.age = 0

            # Now we save the UserProfile model instance.
            profile.save()
            # Log the user in
            new_user = authenticate(username=user_form.cleaned_data['email'],
                                    password=user_form.cleaned_data['password1'])
            login(request, new_user)
            return HttpResponseRedirect(reverse('circleofcare:index'))
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = CustomUserCreationForm()
        profile_form = UserProfileForm()
        # Render the template depending on the context.

    return render(request, 'circleofcare/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    global next_addr
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user:
            # If the account is not active it's been disabled
            if user.is_active:
                login(request, user)
                if next_addr:
                    return HttpResponseRedirect(next_addr)
                else:
                    return HttpResponseRedirect(reverse('circleofcare:index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            return HttpResponse("Invalid login details supplied.")

    else:
        if 'next' in request.GET:
            next_addr = request.GET['next']
        else:
            next_addr = ""
        return render(request, 'circleofcare/login.html')


def retrieve_days_delta(days):
    return timezone.now() - timedelta(days=days)