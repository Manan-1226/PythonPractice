from rest_framework import serializers
from core.models.employee import Employee


class EmployeeSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    date_of_birth = serializers.DateField()
    hire_date = serializers.DateField()
    job_title = serializers.CharField(max_length=100)
    department = serializers.CharField(max_length=100)
    salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    email = serializers.EmailField(max_length=100)
    country_code = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=200)
    city = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)

    def validate(self, data):
        return data


class EmployeeInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "employee_uid",
            "first_name",
            "last_name",
            "date_of_birth",
            "hire_date",
            "job_title",
            "department",
            "salary",
            "email",
            "phone",
            "address",
            "city",
            "country",
            "is_active",
            "last_login",
            "last_logout_time",
            "date_created",
            "date_updated",
        )
        read_only_fields = ()
