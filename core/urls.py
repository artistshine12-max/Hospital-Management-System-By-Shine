from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]

urlpatterns = [

    # Dashboard
    path("", views.dashboard, name="dashboard"),

    # Authentication
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Patients
    path("patients/", views.patient_list, name="patients"),
    path("patients/add/", views.add_patient, name="add_patient"),
    path("patients/edit/<int:id>/", views.edit_patient, name="edit_patient"),
    path("patients/delete/<int:id>/", views.delete_patient, name="delete_patient"),

    # Doctors
    path("doctors/", views.doctor_list, name="doctors"),
    path("doctors/add/", views.add_doctor, name="add_doctor"),
    path("doctors/edit/<int:id>/", views.edit_doctor, name="edit_doctor"),
    path("doctors/delete/<int:id>/", views.delete_doctor, name="delete_doctor"),

    # Appointments
    path("appointments/", views.appointment_list, name="appointments"),
    path("appointments/add/", views.add_appointment, name="add_appointment"),
    path("appointments/edit/<int:id>/", views.edit_appointment, name="edit_appointment"),
    path("appointments/delete/<int:id>/", views.delete_appointment, name="delete_appointment"),

    # Billing
    path("billing/", views.bill_list, name="billing"),
    path("billing/add/", views.add_bill, name="add_bill"),
    path("billing/edit/<int:id>/", views.edit_bill, name="edit_bill"),
    path("billing/delete/<int:id>/", views.delete_bill, name="delete_bill"),
    path("billing/pdf/<int:id>/", views.download_bill, name="download_bill"),

    # Prescriptions
    path("prescriptions/", views.prescription_list, name="prescriptions"),
    path("prescriptions/add/", views.add_prescription, name="add_prescription"),
    path("prescriptions/edit/<int:id>/", views.edit_prescription, name="edit_prescription"),
    path("prescriptions/delete/<int:id>/", views.delete_prescription, name="delete_prescription"),
    path("reports/", views.reports, name="reports"),
    path(
    "notifications/",
    views.notifications,
    name="notifications"
),

path(
    "notifications/read/<int:id>/",
    views.mark_notification,
    name="read_notification"
),

path(
    "notifications/delete/<int:id>/",
    views.delete_notification,
    name="delete_notification"
),
path(
    "notifications/read/<int:id>/",
    views.mark_notification,
    name="mark_notification"
),

path(
    "notifications/read-all/",
    views.mark_all_notifications,
    name="mark_all_notifications"
),

path(
    "notifications/delete/<int:id>/",
    views.delete_notification,
    name="delete_notification"
),

path(
    "notifications/delete-all/",
    views.delete_all_notifications,
    name="delete_all_notifications"
),

path(
    "notifications/count/",
    views.notification_count,
    name="notification_count"
),
path(
    "profile/",
    views.profile,
    name="profile",
),

path(
    "profile/edit/",
    views.edit_profile,
    name="edit_profile",
),

path(
    "change-password/",
    views.change_password,
    name="change_password",
),
path(
    "settings/",
    views.hospital_settings,
    name="hospital_settings",
),

]