from django.contrib.auth.decorators import user_passes_test


def admin_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name="Admin").exists()
    )(view_func)


def doctor_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name="Doctor").exists()
    )(view_func)


def receptionist_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name="Receptionist").exists()
    )(view_func)


def nurse_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name="Nurse").exists()
    )(view_func)