from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Q, Count
from django.utils import timezone
from django.http import HttpResponse
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import JsonResponse
from .models import Patient, Doctor, Appointment, Bill, Prescription, Notification
from .forms import PatientForm, DoctorForm, AppointmentForm, BillForm, PrescriptionForm
from django.contrib.auth.decorators import login_required
from .models import AuditLog
from django.db.models import Sum
from django.utils import timezone
from .models import (
    Patient,
    Doctor,
    Appointment,
    Bill,
    Notification,
    AuditLog,
)
def log_activity(user, action):
    AuditLog.objects.create(
        user=user,
        action=action
    )
# for "Access Denied feature for unauthorized users "
#    from django.http import HttpResponseForbidden
from django.db.models.functions import TruncMonth
from .decorators import (
    admin_required,
    doctor_required,
    receptionist_required,
    nurse_required,
)
# Dashboard
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone


@login_required
def dashboard(request):

    # Dashboard Cards
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()

    total_revenue = (
        Bill.objects.aggregate(total=Sum("total_amount"))["total"] or 0
    )

    pending_bills = Bill.objects.filter(paid=False).count()
    paid_bills = Bill.objects.filter(paid=True).count()

    # Today's appointments
    today = timezone.localdate()

    today_appointments = Appointment.objects.filter(
        appointment_date=today
    ).order_by("appointment_time")

    # Recent data
    recent_patients = Patient.objects.order_by("-id")[:5]
    recent_bills = Bill.objects.order_by("-created_at")[:5]

    # -------------------------
    # Charts
    # -------------------------

    # Patients per month
    patient_chart = (
        Patient.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    patient_labels = [
        p["month"].strftime("%b %Y")
        for p in patient_chart
        if p["month"]
    ]

    patient_data = [
        p["total"]
        for p in patient_chart
    ]

    # Revenue per month
    revenue_chart = (
        Bill.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("total_amount"))
        .order_by("month")
    )

    revenue_labels = [
        r["month"].strftime("%b %Y")
        for r in revenue_chart
        if r["month"]
    ]

    revenue_data = [
        float(r["total"] or 0)
        for r in revenue_chart
    ]
    recent_appointments = Appointment.objects.order_by("-id")[:5]

    recent_prescriptions = Prescription.objects.order_by("-id")[:5]

    context = {

        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_appointments": total_appointments,
        "revenue": total_revenue,

        "pending_bills": pending_bills,
        "paid_bills": paid_bills,

        "today_appointments": today_appointments,

        "recent_patients": recent_patients,
        "recent_bills": recent_bills,

        "patient_labels": patient_labels,
        "patient_data": patient_data,

        "revenue_labels": revenue_labels,
        "revenue_data": revenue_data,
         "recent_appointments": recent_appointments,
    "recent_prescriptions": recent_prescriptions,

    }

    return render(
        request,
        "dashboard.html",
        context,
    )


# Patient Views
@login_required
def patient_list(request):

    search = request.GET.get("search", "")

    patients = Patient.objects.all().order_by("-id")

    if search:

        patients = patients.filter(

            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search)

        )

    paginator = Paginator(patients, 10)

    page = request.GET.get("page")

    patients = paginator.get_page(page)

    return render(
        request,
        "patients.html",
        {
            "patients": patients,
            "search": search,
        },
    )


@login_required
def add_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient=form.save()
            
            Notification.objects.create(
            title="New Patient Registered",
            message=f"{patient.first_name} {patient.last_name} has been registered."
)
            return redirect("patients")
    else:
        form = PatientForm()
    return render(request, "patient_form.html", {"form": form})


@login_required
def edit_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("patients")
    else:
        form = PatientForm(instance=patient)
    return render(request, "patient_form.html", {"form": form})


@login_required
def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    patient.delete()
    return redirect("patients")


# Doctor Views
@login_required

def doctor_list(request):

    search = request.GET.get("search", "")

    doctors = Doctor.objects.all().order_by("-id")

    if search:

        doctors = doctors.filter(

            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(specialization__icontains=search)

        )

    paginator = Paginator(doctors, 10)

    page = request.GET.get("page")

    doctors = paginator.get_page(page)

    return render(
        request,
        "doctors.html",
        {
            "doctors": doctors,
            "search": search,
        },
    )


@login_required
@admin_required
def add_doctor(request):
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor=form.save()
            Notification.objects.create(
            title="New Doctor Added",
            message=f"Dr. {doctor.first_name} {doctor.last_name} has been added."
)
            return redirect("doctors")
    else:
        form = DoctorForm()
    return render(request, "doctor_form.html", {"form": form})


@login_required
def edit_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    if request.method == "POST":
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect("doctors")
    else:
        form = DoctorForm(instance=doctor)
    return render(request, "doctor_form.html", {"form": form})


@login_required
@admin_required
def delete_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    doctor.delete()
    return redirect("doctors")


# Appointment Views
@login_required
def appointment_list(request):

    search = request.GET.get("search", "")

    date = request.GET.get("date", "")

    appointments = Appointment.objects.select_related(
        "patient",
        "doctor"
    ).order_by("-id")

    if search:

        appointments = appointments.filter(

            Q(patient__first_name__icontains=search) |
            Q(patient__last_name__icontains=search) |
            Q(doctor__first_name__icontains=search) |
            Q(doctor__last_name__icontains=search)

        )

    if date:

        appointments = appointments.filter(
            appointment_date=date
        )

    paginator = Paginator(appointments, 10)

    page = request.GET.get("page")

    appointments = paginator.get_page(page)

    return render(
        request,
        "appointments.html",
        {
            "appointments": appointments,
            "search": search,
            "date": date,
        },
    )



@login_required
@receptionist_required
def add_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment=form.save()
            # Create notification
            Notification.objects.create(
                title="Appointment Booked",
                message=f"{appointment.patient} booked an appointment with {appointment.doctor}."
            )
            return redirect("appointments")
    else:
        form = AppointmentForm()
    return render(request, "appointment_form.html", {"form": form})


@login_required
def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect("appointments")
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, "appointment_form.html", {"form": form})


@login_required
def delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.delete()
    return redirect("appointments")


# Billing Views

@login_required

def bill_list(request):

    search = request.GET.get("search", "")

    bills = Bill.objects.select_related(
        "patient"
    ).order_by("-id")

    if search:

        bills = bills.filter(

            Q(patient__first_name__icontains=search) |
            Q(patient__last_name__icontains=search)

        )

    paginator = Paginator(bills, 10)

    page = request.GET.get("page")

    bills = paginator.get_page(page)

    return render(
        request,
        "billing.html",
        {
            "bills": bills,
            "search": search,
        },
    )


@login_required
def add_bill(request):

    if request.method == "POST":

        form = BillForm(request.POST)

        if form.is_valid():

            bill = form.save()

            Notification.objects.create(
                title="Bill Generated",
                message=f"Bill #{bill.id} generated for {bill.patient}."
            )

            return redirect("billing")

    else:

        form = BillForm()

    return render(
        request,
        "bill_form.html",
        {
            "form": form
        }
    )


@login_required
def edit_bill(request, id):
    bill = get_object_or_404(Bill, id=id)
    if request.method == "POST":
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect("billing")
    else:
        form = BillForm(instance=bill)
    return render(request, "bill_form.html", {"form": form})


@login_required
def delete_bill(request, id):
    bill = get_object_or_404(Bill, id=id)
    bill.delete()
    return redirect("billing")


# Authentication Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# Prescription Views
@login_required

def prescription_list(request):
    '''if not (
        has_group(request.user, "Admin") or
        has_group(request.user, "Doctor")
    ):
        return HttpResponseForbidden("Access Denied")'''

    prescriptions = Prescription.objects.all()
    return render(request, "prescriptions.html", {"prescriptions": prescriptions})


@login_required
@doctor_required
def add_prescription(request):
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription=form.save()
            Notification.objects.create(
    title="Prescription Added",
    message=f"Prescription created for {prescription.patient}."
)
            return redirect("prescriptions")
    else:
        form = PrescriptionForm()
    return render(request, "prescription_form.html", {"form": form})


@login_required
def edit_prescription(request, id):
    prescription = get_object_or_404(Prescription, id=id)
    if request.method == "POST":
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect("prescriptions")
    else:
        form = PrescriptionForm(instance=prescription)
    return render(request, "prescription_form.html", {"form": form})


@login_required
def delete_prescription(request, id):
    prescription = get_object_or_404(Prescription, id=id)
    prescription.delete()
    return redirect("prescriptions")

@login_required
def download_bill(request, id):

    bill = get_object_or_404(Bill, id=id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="bill_{bill.id}.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>CITY HOSPITAL</b>", styles["Title"]))
    elements.append(Paragraph("Hospital Management System", styles["Heading2"]))
    elements.append(Paragraph("<br/>", styles["Normal"]))

    elements.append(Paragraph(f"Bill No : {bill.id}", styles["Normal"]))
    elements.append(Paragraph(f"Patient : {bill.patient}", styles["Normal"]))
    elements.append(Paragraph(f"Appointment : {bill.appointment}", styles["Normal"]))
    elements.append(Paragraph("<br/>", styles["Normal"]))

    elements.append(Paragraph(f"Consultation Fee : ${bill.consultation_fee}", styles["Normal"]))
    elements.append(Paragraph(f"Medicine Charge : ${bill.medicine_charge}", styles["Normal"]))
    elements.append(Paragraph(f"Test Charge : ${bill.test_charge}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Total Amount : ${bill.total_amount}</b>", styles["Heading2"]))

    status = "Paid" if bill.paid else "Pending"
    elements.append(Paragraph(f"Payment Status : {status}", styles["Normal"]))

    doc.build(elements)

    return response

def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@login_required
@doctor_required
def reports(request):

    date = request.GET.get("date", "")

    appointments = Appointment.objects.select_related(
        "patient",
        "doctor"
    )

    bills = Bill.objects.select_related("patient")

    if date:

        appointments = appointments.filter(
            appointment_date=date
        )

        bills = bills.filter(
            appointment__appointment_date=date
        )

    revenue = bills.aggregate(
        Sum("total_amount")
    )["total_amount__sum"] or 0

    context = {

        "total_patients": Patient.objects.count(),

        "total_doctors": Doctor.objects.count(),

        "total_appointments": appointments.count(),

        "revenue": revenue,

        "recent_appointments": appointments.order_by("-id")[:10],

        "recent_bills": bills.order_by("-id")[:10],

        "selected_date": date,

    }

    return render(
        request,
        "reports.html",
        context,
    )
@login_required
def notifications(request):

    notifications = Notification.objects.all().order_by("-created_at")

    return render(
        request,
        "notifications.html",
        {
            "notifications": notifications,
        }
    )
@login_required
def mark_notification(request, id):

    notification = Notification.objects.get(id=id)

    notification.is_read = True

    notification.save()

    return redirect("notifications")
@login_required
def delete_notification(request, id):

    notification = Notification.objects.get(id=id)

    notification.delete()

    return redirect("notifications")
@login_required
def mark_all_notifications(request):

    Notification.objects.filter(
        is_read=False
    ).update(
        is_read=True
    )

    return redirect("notifications")
@login_required
def delete_all_notifications(request):

    Notification.objects.all().delete()

    return redirect("notifications")
@login_required
def notification_count(request):

    unread = Notification.objects.filter(
        is_read=False
    ).count()

    return JsonResponse({

        "count": unread

    })
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .forms import (
    UserForm,
    UserProfileForm,
    CustomPasswordChangeForm
)

from .models import UserProfile

@login_required
def profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "profile.html",
        {
            "profile": profile
        }
    )
@login_required
def edit_profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        user_form = UserForm(
            request.POST,
            instance=request.user
        )

        profile_form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()

            profile_form.save()

            messages.success(
                request,
                "Profile Updated Successfully."
            )

            return redirect("profile")

    else:

        user_form = UserForm(
            instance=request.user
        )

        profile_form = UserProfileForm(
            instance=profile
        )

    return render(
        request,
        "edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        }
    )
@login_required
def change_password(request):

    if request.method == "POST":

        form = CustomPasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "Password Changed Successfully."
            )

            return redirect("profile")

    else:

        form = CustomPasswordChangeForm(
            request.user
        )

    return render(
        request,
        "change_password.html",
        {
            "form": form
        }
    )
from .models import HospitalSettings,Department
from .forms import HospitalSettingsForm,DepartmentForm
@login_required
def hospital_settings(request):

    settings_obj, created = HospitalSettings.objects.get_or_create(id=1)

    if request.method == "POST":

        form = HospitalSettingsForm(
            request.POST,
            request.FILES,
            instance=settings_obj
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Hospital settings updated successfully."
            )

            return redirect("hospital_settings")

    else:

        form = HospitalSettingsForm(instance=settings_obj)

    return render(
        request,
        "settings.html",
        {
            "form": form
        }
    )
@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(
        request,
        "departments.html",
        {"departments": departments},
    )


@login_required
def add_department(request):
    form = DepartmentForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("departments")

    return render(
        request,
        "department_form.html",
        {"form": form},
    )
import shutil
import datetime
from pathlib import Path
@login_required
def create_backup(request):

    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)

    filename = datetime.datetime.now().strftime(
        "backup_%Y%m%d_%H%M%S.sqlite3"
    )

    destination = backup_dir / filename

    shutil.copy(
        "db.sqlite3",
        destination
    )

    messages.success(
        request,
        "Database backup created successfully."
    )

    return redirect("backup_history")
@login_required
def backup_history(request):

    backup_dir = Path("backups")

    backup_dir.mkdir(exist_ok=True)

    backups = sorted(
        backup_dir.glob("*.sqlite3"),
        reverse=True
    )

    return render(
        request,
        "backup_history.html",
        {
            "backups": backups
        }
    )

@login_required
def delete_backup(request, filename):

    file = Path("backups") / filename

    if file.exists():

        file.unlink()

        messages.success(
            request,
            "Backup deleted."
        )

    return redirect("backup_history")
###########################
