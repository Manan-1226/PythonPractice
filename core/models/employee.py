import uuid
from django.db import models
from django.utils import timezone


class Employee(models.Model):
    employee_uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_code = models.CharField(max_length=255, blank=False, null=False)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    date_of_birth = models.DateField(blank=False, null=False)
    hire_date = models.DateField(blank=False, null=False)
    job_title = models.CharField(max_length=100, blank=False, null=False)
    department = models.CharField(max_length=100, blank=False, null=False)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    email = models.EmailField(max_length=100, blank=False, null=False)
    country_code = models.CharField(max_length=255, blank=False, null=False)
    phone = models.CharField(max_length=20, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    country = models.CharField(max_length=100, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True, null=False)
    last_logout_time = models.DateTimeField(null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
