from django import forms
from .models import Patient, Doctor, Appointment, Bill, Prescription


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = "__all__"


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"
        widgets = {
            "appointment_date": forms.DateInput(attrs={"type": "date"}),
            "appointment_time": forms.TimeInput(attrs={"type": "time"}),
        }


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        exclude = [
            "total_amount",
        ]


class PrescriptionForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = "__all__"
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

from .models import UserProfile


class UserForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
        ]


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile

        fields = [
            "profile_image",
            "phone",
            "department",
            "designation",
            "address",
        ]


class CustomPasswordChangeForm(
    PasswordChangeForm
):
    pass
from .models import HospitalSettings, Specialization, Ward,MedicineCategory, Department
class HospitalSettingsForm(forms.ModelForm):

    class Meta:
        model = HospitalSettings

        fields = "__all__"
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"


class SpecializationForm(forms.ModelForm):
    class Meta:
        model = Specialization
        fields = "__all__"


class WardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = "__all__"


class MedicineCategoryForm(forms.ModelForm):
    class Meta:
        model = MedicineCategory
        fields = "__all__"