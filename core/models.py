from django.db import models

class Patient(models.Model):
    GENDER = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField()
    disease = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Doctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    fee = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"


class Appointment(models.Model):
    STATUS = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS, default="Pending")
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient} - {self.doctor}"


class Bill(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE
    )

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    medicine_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    test_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        editable=False
    )

    paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        self.total_amount = (
            self.consultation_fee +
            self.medicine_charge +
            self.test_charge
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill #{self.id}"

class Prescription(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE
    )

    medicines = models.TextField()

    dosage = models.TextField()

    instructions = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Prescription #{self.id}"
    
class Notification(models.Model):

    title = models.CharField(max_length=200)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Doctor", "Doctor"),
        ("Receptionist", "Receptionist"),
        ("Nurse", "Nurse"),
        ("Pharmacist", "Pharmacist"),
        ("Lab Technician", "Lab Technician"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    department = models.CharField(
        max_length=100,
        blank=True
    )

    designation = models.CharField(
        max_length=100,
        blank=True
    )

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default="Receptionist"
    )

    address = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username    
class HospitalSettings(models.Model):

    hospital_name = models.CharField(
        max_length=200,
        default="City Hospital"
    )

    logo = models.ImageField(
        upload_to="hospital/",
        blank=True,
        null=True
    )

    favicon = models.ImageField(
        upload_to="hospital/",
        blank=True,
        null=True
    )

    address = models.TextField()

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField()

    website = models.URLField(
        blank=True
    )

    currency = models.CharField(
        max_length=5,
        default="₹"
    )

    timezone = models.CharField(
        max_length=50,
        default="Asia/Kolkata"
    )

    date_format = models.CharField(
        max_length=20,
        default="d M Y"
    )

    footer = models.CharField(
        max_length=255,
        default="Hospital Management System"
    )

    about = models.TextField(
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.hospital_name

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Ward(models.Model):
    name = models.CharField(max_length=100)
    total_beds = models.PositiveIntegerField(default=0)
    occupied_beds = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class MedicineCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
from django.contrib.auth.models import User

class AuditLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    action = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"