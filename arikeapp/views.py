from datetime import datetime
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.forms import ModelForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import *
from django.views import View
from arikeapp.models import *
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Authorization------------------------------------------------
class UserLoginView(LoginView):
    template_name="login.html"

class AuthorisedPatientsGenerator(LoginRequiredMixin):
    def get_queryset(self):
        return Patient.objects.filter(deleted=False, facility= self.request.user.facility)    
#--------------------------------------------------------------------
# Patient----------------------------------------------------------------
class GenericPatientsView(LoginRequiredMixin,View):
    template = "patients_list.html"
    login_url = '/'
    redirect_field_name="/patients/"

    def get(self, request):
        current_user = request.user
        patients_data= Patient.objects.filter(deleted=False)
        print(len(patients_data))
        search_term=request.GET.get('search')
        sort_by = request.GET.get('sort')
        if search_term:
            patients_data= patients_data.filter(first_name__icontains=search_term) | patients_data.filter(last_name__icontains=search_term)
        if sort_by == "AZ":
            patients_data= patients_data.order_by('first_name')  
        if sort_by == "ZA":
            patients_data= patients_data.order_by('-first_name')  

        return render(request, self.template, {"myuser": current_user,"patients_data":patients_data})

class GenericPatientDetailView(LoginRequiredMixin,View):
    template = "patient_details.html"
    login_url = '/'
    
    def get(self, request,pk):
        current_user = request.user
        patient_obj = Patient.objects.get(id=pk)
        return render(request, self.template, {"myuser": current_user,"patientobj":patient_obj}) 
      

class PatientCreateForm(ModelForm):
    class Meta:
        model=Patient
        fields=['first_name', 'last_name','email', 'date_of_birth','phone','emergency_phone_number','address','ward','facility','gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = ''   
        self.fields['last_name'].widget.attrs['class'] = ''   
        self.fields['email'].widget.attrs['class'] = '' 
        self.fields['date_of_birth'].widget.attrs['class'] = '' 
        self.fields['phone'].widget.attrs['class'] = ''  
        self.fields['emergency_phone_number'].widget.attrs['class'] = ''  
        self.fields['address'].widget.attrs['class'] = 'col-span-2'  
        self.fields['ward'].widget.attrs['class'] = ''  
        self.fields['facility'].widget.attrs['class'] = ''  
        self.fields['gender'].widget.attrs['class'] = ''  


class GenericPatientCreateView(LoginRequiredMixin,CreateView):
    form_class= PatientCreateForm
    template_name="create_patient.html"
    success_url="/patients/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect("/patients")

    # def get(self, request):
    #     form = self.form_class()
    #     return render(request, self.template, {"form": form,"myuser":request.user})
        
    # def post(self, request):
    #     data = request.POST
    #     form = self.form_class(data)
    #     if form.is_valid():
    #         patient_obj = form.save()
    #         patient_obj.save()
    #         return redirect("/patients/")
    #     return render(request, self.template, {"form": form,"myuser":request.user})
 

class GenericPatientDeleteView(AuthorisedPatientsGenerator, DeleteView):
    model=Patient
    template_name="delete_patient.html"
    success_url="/patients/"

    def get_object(self, queryset=None):
        return get_object_or_404(Patient, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context

class GenericPatientUpdateView(AuthorisedPatientsGenerator, UpdateView):  
    model=Patient
    form_class=PatientCreateForm
    template_name="update_patient.html"
    success_url="/patients/"

    def get_object(self, queryset=None):
        return get_object_or_404(Patient, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect("/patients/")

class PatientUpdateView(AuthorisedPatientsGenerator, View):
    template="update_patient.html"
    form_class=PatientCreateForm
    model=Patient

    def get(self, request, pk):
        patient_obj = Patient.objects.get(id=pk, deleted=False)
        form = self.form_class(instance=patient_obj)
        return render(request, self.template, {"form": form,"myuser":request.user})
    

    def post(self, request, pk):
        print("inside post method")
        patient_obj = Patient.objects.get(id=pk, deleted=False)
        data = request.POST
        form = self.form_class(data, instance=patient_obj)
        if form.is_valid():
            print("form valid")
            form.save()
            return redirect("/patients/")
        print("form invalid")    
        return render(request, self.template, {"form": form,"myuser":request.user})
       
#--------------------------------------------------------------------
# Profile ------------------------------------------------------------
class GenericProfileView(LoginRequiredMixin,View):
    template = "profile.html"
    login_url = '/'
    redirect_field_name="/profile/"

    def get(self, request):
        current_user = request.user
        return render(request, self.template, {"myuser": current_user})

    def post(self, request):
        
        current_user = request.user
        data = request.POST
        if ((data['password1'])!=''):
            if (data['password1'] == data['password2']):
                Myuser.objects.filter(username=current_user.username).update(first_name=data['first_name'], last_name=data['last_name'],phone=data['phone'],email=data['email'],password=data['password1'])
            else:
                pass    
        else:
            Myuser.objects.filter(username=current_user.username).update(first_name=data['first_name'], last_name=data['last_name'],phone=data['phone'],email=data['email'])
        return redirect("/profile/")

#---------------------------------------------------------------------------
# Facility ------------------------------------------------------------------

class GenericFacilitiesView(LoginRequiredMixin, View):
    template = "facility_list.html"
    login_url = '/'
    redirect_field_name="/facilities/"

    def get(self, request):
        current_user = request.user
        facility_data=Facility.objects.filter(deleted=False)
        wards_data=Ward.objects.filter(deleted=False)
        search_term=request.GET.get('search')
        sort_by=request.GET.get('sort')
        filter_ward_term=request.GET.get('filter-ward')
        filter_kind_term=request.GET.get('filter-kind')
        if search_term:
            facility_data= facility_data.filter(name__icontains=search_term) | facility_data.filter(address__icontains=search_term) 
        if sort_by == "AZ":
            facility_data= facility_data.order_by('name')
        if sort_by == "ZA":
            facility_data= facility_data.order_by('-name')
        if filter_ward_term not in [ None,"default"]:
            facility_data= facility_data.filter(ward__name=filter_ward_term) 
        if filter_kind_term not in [ None,"default"]:
            facility_data= facility_data.filter(kind=filter_kind_term)     
        return render(request, self.template, {"myuser": current_user,"facility_data":facility_data,"wards_data":wards_data})

class GenericFacilityDetailView(LoginRequiredMixin,View):
    template = "facility_details.html"
    login_url = '/'

    def get(self, request,pk):
        current_user = request.user
        facility_obj = Facility.objects.get(id=pk)
        return render(request, self.template, {"myuser": current_user,"facility":facility_obj})        
            
class FacilityCreateForm(ModelForm):
    class Meta:
        model=Facility
        fields=['kind', 'name','address', 'ward','pincode','phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kind'].widget.attrs['class'] = ''   
        self.fields['name'].widget.attrs['class'] = ''   
        self.fields['address'].widget.attrs['class'] = '' 
        self.fields['ward'].widget.attrs['class'] = '' 
        self.fields['pincode'].widget.attrs['class'] = ''  
        self.fields['phone'].widget.attrs['class'] = ''  
       

class GenericFacilityCreateView(LoginRequiredMixin,CreateView):
    form_class= FacilityCreateForm
    template_name="create_facility.html"
    success_url="/facilities/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect("/facilities")

class GenericFacilityDeleteView(AuthorisedPatientsGenerator, DeleteView):
    model=Facility
    template_name="delete_facility.html"
    success_url="facilities/"

    def get_object(self, queryset=None):
        return get_object_or_404(Facility, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context

class GenericFacilityUpdateView(AuthorisedPatientsGenerator, UpdateView):  
    model=Facility
    form_class=FacilityCreateForm
    template_name="update_facility.html"
    success_url="/facilities/"

    def get_object(self, queryset=None):
        return get_object_or_404(Facility, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect("/facilities/")

#--------------------------------------------------------------------
# Family details ---------------------------------------------------

class GenericFamilyView(LoginRequiredMixin, View):
    template = "family_list.html"
    login_url = '/'
    redirect_field_name="/patients/"

    # def get_object(self, queryset=None):
    #     return get_object_or_404(family_detail, patient_id=self.kwargs.get('pk'))

    def get(self, request,pk):
        current_user = request.user
        patientobj=Patient.objects.get(id=pk)
        family_data= family_detail.objects.filter(deleted=False, patient__id=pk)
        return render(request, self.template, {"myuser": current_user,"family_data":family_data,"patientobj":patientobj})  
            
class FamilyCreateForm(ModelForm):
    class Meta:
        model=family_detail
        fields=['first_name', 'last_name','email', 'date_of_birth','phone','relation', 'education','address','gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = ''   
        self.fields['last_name'].widget.attrs['class'] = ''   
        self.fields['email'].widget.attrs['class'] = '' 
        self.fields['date_of_birth'].widget.attrs['class'] = '' 
        self.fields['relation'].widget.attrs['class'] = ''  
        self.fields['phone'].widget.attrs['class'] = ''  
        self.fields['education'].widget.attrs['class'] = ''  
        self.fields['address'].widget.attrs['class'] = ''  
        self.fields['gender'].widget.attrs['class'] = ''  
       

class GenericFamilyCreateView(LoginRequiredMixin, View):
    form_class= FamilyCreateForm
    template="create_family.html"
    success_url="/patients/"

    def get(self, request,pk):
        form = self.form_class()
        return render(request, self.template, {"form": form,"myuser":request.user})
        
    def post(self, request,pk):
        data = request.POST
        form = self.form_class(data)
        if form.is_valid():
            print("form valid")
            family_obj = form.save()
            family_obj.patient= Patient.objects.get(id=pk)
            family_obj.save()
            return redirect("/patients/")
        print("form not valid")    
        return render(request, self.template, {"form": form,"myuser":request.user})

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['myuser'] = self.request.user
    #     return context

    # def form_valid(self, form):
    #     print("reached here")
    #     patient_obj=Patient.objects.get(id=self.kwargs.get('pk'))
    #     self.object = form.save()
    #     print("no prob till here")
    #     self.object.patient =patient_obj
    #     self.object.save()
    #     return HttpResponseRedirect("/patients/")

class GenericFamilyDeleteView(AuthorisedPatientsGenerator, DeleteView):
    model=family_detail
    template_name="delete_family.html"
    success_url="/patients/"

    def get_object(self, queryset=None):
        return get_object_or_404(family_detail, pk=self.kwargs.get('fampk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context

class GenericFamilyUpdateView(AuthorisedPatientsGenerator, UpdateView):  
    model=family_detail
    form_class=FamilyCreateForm
    template_name="update_family.html"
    success_url="/patients/"

    def get_object(self, queryset=None):
        return get_object_or_404(family_detail, pk=self.kwargs.get('fampk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect("/patients/")
#-----------------------------------------------------------------------------
# Home
class GenericHomeView(LoginRequiredMixin,View):
    template = "home2.html"
    login_url = '/'
    redirect_field_name="/home/"

    def get(self, request):
        current_user = request.user
        return render(request, self.template, {"myuser": current_user})









# def view_dashboard(request):
#     return render(request,"dashboard_layout.html")

# @login_required
# def view_home(request):
#     return render(request,"home2.html",{"myusername":"Alex Doe"})

# def view_users(request):
#     return render(request,"user_list.html",{"myusername":"Alex Doe"})    

# def view_profile(request):
#     return render(request,"profile.html",{"myusername":"Alex Doe"})   

# def create_user_view(request):
#     return render(request,"create_user.html",{"myusername":"Alex Doe"})        

# User ------------------------------------------------------------------------
class UserSignUpForm(UserCreationForm):

    class Meta:
        model = Myuser
        fields = ('username', 'first_name', 'last_name','email','password1', 'password2', 'role', 'phone', 'is_verified','district','facility')


class GenericUserCreateView(CreateView):
    form_class= UserSignUpForm
    template_name="signup.html"
    success_url="/users/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context

    def form_valid(self, form):
        return super(GenericUserCreateView, self).form_valid(form)


class GenericUsersView(LoginRequiredMixin, View):
    template = "user_list.html"
    login_url = '/'
    redirect_field_name="/users/"

    def get(self, request):
        current_user = request.user
        users_data=Myuser.objects.filter(deleted=False)
        superusers = Myuser.objects.filter(is_superuser=True)
        search_term=request.GET.get('search')
        sort_by = request.GET.get('sort')
        
        if sort_by == "AZ":
            users_data= users_data.order_by('first_name')  
            superusers= superusers.order_by('first_name')  
        if sort_by == "ZA":
            users_data= users_data.order_by('-first_name')
            superusers= superusers.order_by('-first_name')  
        if search_term:
            users_data= users_data.filter(first_name__icontains=search_term) | users_data.filter(last_name__icontains=search_term)
            superusers = superusers.filter(first_name__icontains=search_term)| superusers.filter(last_name__icontains=search_term) 

        return render(request, self.template, {"myuser": current_user,"userdata":users_data,"superusers":superusers})

class GenericUserDetailView(LoginRequiredMixin,View):
    template = "user_details.html"
    login_url = '/'

    def get(self, request,pk):
        current_user = request.user
        user_obj = Myuser.objects.get(id=pk)
        return render(request, self.template, {"myuser": current_user,"userobj":user_obj}) 

class GenericUserDeleteView(LoginRequiredMixin, DeleteView):
    model=Myuser
    template_name="delete_user.html"
    success_url="/users/"

    def get_object(self, queryset=None):
        return get_object_or_404(Myuser, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context        

class GenericUserUpdateView(LoginRequiredMixin, UpdateView):  
    model=Myuser
    form_class=UserSignUpForm
    template_name="update_user.html"
    success_url="/users/"

    def get_object(self, queryset=None):
        return get_object_or_404(Myuser, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect("/users/")        