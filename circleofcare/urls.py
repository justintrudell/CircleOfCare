from django.conf.urls import url
from . import views

app_name = 'circleofcare'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^physiological_log/?$', views.physiological_log, name='physiological_log'),
    url(r'^functional_log/?$', views.functional_log, name='functional_log'),
    url(r'^physical_activity/?$', views.physical_activity_log, name='physical_activity_log'),
    url(r'^user_profile/?$', views.user_profile, name='user_profile'),
    url(r'^user_summary/?$', views.user_summary, name='user_summary'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^login/?$', views.user_login, name='login'),
    url(r'^logout/?$', views.user_logout, name='logout'),
    url(r'^api/physiological_data/?$', views.physiological_data, name='physiological_data'),
    url(r'^api/functional_data/?$', views.functional_data, name='functional_data'),
    url(r'^api/physical_data/?$', views.physical_data, name='physical_data')
]