from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from arikeapp.views import *
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', UserLoginView.as_view()),
    # path('dashboard/', view_dashboard),
    path('home/', GenericHomeView.as_view()),
    path('users/', GenericUsersView.as_view()),
    path('profile/', GenericProfileView.as_view()),
    path('patients/', GenericPatientsView.as_view()),
    path('facilities/', GenericFacilitiesView.as_view()),
    path('create-user/', GenericUserCreateView.as_view()),
    path('create-patient/', GenericPatientCreateView.as_view()),
    path('create-facility/', GenericFacilityCreateView.as_view()),
    path('user-details/<pk>/', GenericUserDetailView.as_view()),
    path('patient-details/<pk>/', GenericPatientDetailView.as_view()),
    path('patient-details/<pk>/family/', GenericFamilyView.as_view()),
    path('patient-details/<pk>/create-family/',GenericFamilyCreateView.as_view()),
    path('patient-details/<pk>/family/update-family/<fampk>/',GenericFamilyUpdateView.as_view()),
    path('patient-details/<pk>/family/delete-family/<fampk>/',GenericFamilyDeleteView.as_view()),
    path('facility-details/<pk>/', GenericFacilityDetailView.as_view()),
    path('delete-patient/<pk>/', GenericPatientDeleteView.as_view()),
    path('delete-facility/<pk>/', GenericFacilityDeleteView.as_view()),
    path('delete-user/<pk>/', GenericUserDeleteView.as_view()),
    path('update-patient/<pk>/',GenericPatientUpdateView.as_view()),
    path('update-facility/<pk>/',GenericFacilityUpdateView.as_view()),
    path('logout/', LogoutView.as_view()),
    # path('signup/', UserCreateView.as_view()),
]
