from datetime import datetime, time
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

class State(models.Model):
    name=models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    deleted = models.BooleanField(default=False, blank=True)

    def delete(self):
        self.deleted=True
        self.save()
    
    def __str__(self):
        return f"{self.name}"

class District(models.Model):
    name=models.CharField(max_length=200)
    state=models.ForeignKey(State, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    deleted = models.BooleanField(default=False, blank=True)

    def delete(self):
        self.deleted=True
        self.save()

    def __str__(self):
        return f"{self.name}"

LOCAL_BODY_KINDS = (
    # Panchayath levels
    (1, "Grama Panchayath"),
    (2, "Block Panchayath"),
    (3, "District Panchayath"),
    (4, "Nagar Panchayath"),
    # Municipality levels
    (10, "Municipality"),
    # Corporation levels
    (20, "Corporation"),
    # Unknown
    (50, "Others"),
)

class LSG_body(models.Model):
    name=models.CharField(max_length=200)
    lsg_body_code= models.CharField(max_length=20, blank=True, null=True)
    kind=models.IntegerField(choices=LOCAL_BODY_KINDS)
    district= models.ForeignKey(District, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    deleted = models.BooleanField(default=False, blank=True)

    def delete(self):
        self.deleted=True
        self.save()

    def __str__(self):
        return f"{self.name} : ({self.kind})"

class Ward(models.Model):
    local_body = models.ForeignKey(LSG_body, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    deleted = models.BooleanField(default=False, blank=True)

    def delete(self):
        self.deleted=True
        self.save()

    def __str__(self):
        return f"{self.name}"

FACILITY_TYPES = ((1, "PHC"),(2, "CHC"))
class Facility(models.Model):
    name = models.CharField(max_length=255)
    address=models.TextField(max_length=500)
    pincode=models.IntegerField()
    phone=models.CharField(max_length=10, blank=True)
    kind=models.IntegerField(choices=FACILITY_TYPES)
    ward=models.ForeignKey(Ward, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    deleted = models.BooleanField(default=False, blank=True)

    def delete(self):
        self.deleted=True
        self.save()

    def __str__(self):
        return f"{self.name}: {self.kind}"

ROLE_TYPES=(('District Admin','District Admin'),('Primary Nurse','Primary Nurse'),('Secondary Nurse','Secondary Nurse'))
class Myuser(AbstractUser):
    role=models.CharField(choices=ROLE_TYPES, max_length=30)
    phone=models.CharField(blank=True, max_length=10)
    is_verified=models.BooleanField(default=False)
    district=models.ForeignKey(District, null=True, blank=True, on_delete=models.SET_NULL)
    facility=models.ForeignKey(Facility, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    deleted = models.BooleanField(default=False, blank=True)

    def delete(self):
        self.deleted=True
        self.save()

    def __str__(self):
        return f"{self.get_full_name()}"



GENDER_CHOICES = [(1, "Male"), (2, "Female"), (3, "Non-binary")]
class Patient(models.Model):
    first_name=models.CharField(max_length=50, blank=False)  
    last_name=models.CharField(max_length=50, blank=False)  
    date_of_birth=models.DateField(blank=True,null=True)
    address=models.TextField(max_length=500, blank=True)
    landmark=models.CharField(max_length=255, blank=True,null=True)
    phone=models.CharField(max_length=10)
    email=models.EmailField(blank=True)
    gender=models.IntegerField(choices=GENDER_CHOICES)
    emergency_phone_number=models.CharField(max_length=10, blank=True)
    expired_time=models.TimeField(default=None, blank=True,null=True)
    ward=models.ForeignKey(Ward, null=True,on_delete=models.SET_NULL)
    facility=models.ForeignKey(Facility, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    deleted = models.BooleanField(default=False, blank=True)

    def delete(self):
        self.deleted=True
        self.save()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# @receiver(post_save, sender=Patient)
# def update_patient(sender, **kwargs):
#     kwargs["instance"].updated_at=datetime.now()
#     kwargs["instance"].save()
RELATION_TYPES=[("Daughter", "Daughter"), ("Son", "Son"), ("Mother", "Mother"),("Father","Father"),("Sister","Sister"),("Brother","Brother"),("Aunt","Aunt"),("Uncle","Uncle"),("Grandmother","Grandmother"),
("Grandfather","Grandfather"),("Grandson","Grandson"),("Granddaughter","Granddaughter"),("Nephew","Nephew"),("Niece","Niece"),("Friend","Friend")]

class family_detail(models.Model):
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE,null=True)
    first_name=models.CharField(max_length=50, blank=False)  
    last_name=models.CharField(max_length=50, blank=False)  
    phone=models.CharField(max_length=10)
    date_of_birth=models.DateTimeField(blank=True)
    email=models.EmailField(blank=True)
    relation=models.CharField(choices=RELATION_TYPES, max_length=20)
    address=models.TextField(max_length=500, blank=True)
    gender=models.IntegerField(choices=GENDER_CHOICES)
    education=models.CharField(max_length=255, blank=True)
    occupation=models.CharField(max_length=255, blank=True,null=True)
    remarks=models.TextField(max_length=500, blank=True,null=True)
    is_primary=models.BooleanField(default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    deleted = models.BooleanField(default=False, blank=True)

    def delete(self):
        self.deleted=True
        self.save()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Disease(models.Model):
    name=models.CharField(max_length=255)
    icds_code=models.CharField(blank=False, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    deleted = models.BooleanField(default=False, blank=True)

    def delete(self):
        self.deleted=True
        self.save()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Patient_Disease(models.Model):
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE)
    disease=models.ForeignKey(Disease, on_delete=models.PROTECT)
    note=models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    deleted = models.BooleanField(default=False, blank=True)

    def delete(self):
        self.deleted=True
        self.save()

    class Meta:
        unique_together = (('patient', 'disease'))

class Visit_schedule(models.Model):
    date=models.DateField(blank=True)
    time=models.TimeField(blank=True)
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE)
    nurse=models.ForeignKey(Myuser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    deleted = models.BooleanField(default=False, blank=True)

    def delete(self):
        self.deleted=True
        self.save()

    def __str__(self):
        return f"Patient {self.patient} visited by {self.nurse} on {self.date} at {self.time}"

class Visit_details(models.Model):
    palliative_phase=models.CharField(max_length=100)
    blood_pressure=models.DecimalField(max_digits=6, decimal_places=3)
    pulse=models.IntegerField()
    general_random_blood_sugar=models.DecimalField(max_digits=6, decimal_places=3)
    personal_hygiene=models.CharField(max_length=100)
    mouth_hygiene=models.CharField(max_length=100)
    pubic_hygiene=models.CharField(max_length=100)
    systemic_examination=models.CharField(max_length=100)
    patient_at_peace=models.BooleanField(default=True)
    pain=models.BooleanField(default=False)
    symptoms=models.TextField(max_length=500)
    note=models.TextField(max_length=500)
    visit_schedule=models.ForeignKey(Visit_schedule, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    deleted = models.BooleanField(default=False, blank=True)

    def delete(self):
        self.deleted=True
        self.save()

treatment_groups = {
    'General care' : ['Mouth care', 'Bath', 'Nail cutting', 'Shaving'],
    'Genito urinary care' : [
    'Perennial care',
    'Condom catheterisation & training',
    'Nelcath catheterisation & training',
    'Foley’s catheterisation',
    'Foley’s catheter care',
    'Suprapubic catheterisation',
    'Suprapubic catheter care',
    'Bladder wash with normal saline',
    'Bladder wash with soda bicarbonate',
    'Urostomy care',
  ],
  'Gastro-intestinal care' : [
    'Ryles tube insertion',
    'Ryles tube care',
    'Ryles tube feeding & training',
    'PEG care',
    'Per Rectal Enema',
    'High enema',
    'Bisacodyl Suppository',
    'Digital evacuation',
    'Colostomy care',
    'Colostomy irrigation care',
    'ileostomy care',
  ],
  'Wound care' : [
    'Wound care training given to family',
    'Wound dressing',
    'Suture removal',
    'Vacuum dressing',
  ],
  'Respiratory care' : [
    'Tracheostomy care',
    'Chest physiotherapy',
    'Inhaler training',
    'Oxygen concentrator - training',
    'Bi-PAP training',
    'Bandaging',
    'Upper limb lymphedema bandaging',
    'Lower limb lymphedema bandaging',
    'Upper limb lymphedema hosiery',
    'PVOD bandaging',
  ],
  'Invasive care': [
    'IV fluid infusion',
    'IV medicine bolus administration',
    'IV cannula care',
    'IV cannula insertion',
    'S/C cannula insertion',
    'S/C fluid infusion (subcutaneous)',
    'S/C medicine bolus administration',
    'S/C cannula care',
    'Ascites tapping',
    'Ascitic catheter care',
  ],
  'Physiotherapy' : [
    'Passive Movement',
    'Active Movement',
    'Strengthening exercises',
    'NDT',
    'GAIT Training',
    'Modalities + text field',
    'Breathing exercises',
    'Balance & Coordination exercises',
    'Stretching',
    'Postural correction',
  ]
}

CARE_TYPES=((i+1, key) for i, key in enumerate(treatment_groups))
# CARE_SUBTYPES=([i+1 for i in range(len(val))] for (key,val) in treatment_groups.items())

class Treatment(models.Model):
    description=models.TextField(max_length=500)
    care_type=models.IntegerField(choices=CARE_TYPES)
    care_sub_type=models.IntegerField()
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    deleted = models.BooleanField(default=False, blank=True)

    def delete(self):
        self.deleted=True
        self.save()

class Treatment_notes(models.Model):
    description=models.TextField(max_length=500)
    care_type=models.IntegerField(choices=CARE_TYPES)
    care_sub_type=models.IntegerField()
    treatment=models.ForeignKey(Treatment, on_delete=models.CASCADE)
    visit=models.ForeignKey(Visit_schedule,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    deleted = models.BooleanField(default=False,blank=True)

    def delete(self):
        self.deleted=True
        self.save()

class Nurses_Report(models.Model):
    user = models.ForeignKey(Myuser, on_delete=models.CASCADE,)
    confirmation = models.BooleanField(blank=True, default=False, help_text="I want to receive daily reports")
    send_time = models.TimeField(default=time(12, 0, 0), help_text="Enter time in UTC format hh:mm:ss .")
    last_updated = models.DateTimeField(null=True)