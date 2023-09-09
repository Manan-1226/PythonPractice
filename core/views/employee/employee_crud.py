from datetime import date
from rest_framework import generics, status
from rest_framework.response import Response
from core.components import ErrorCode, ErrorHandling
from core.components.employee import EmployeeComponent
from core.serializers.employee import EmployeeInformationSerializer, EmployeeSerializer
from core.models.employee import Employee


class EmployeeView(generics.GenericAPIView):
    serializer = EmployeeSerializer

    def employee_entity(employee):
        today = date.today()
        age = today.year - employee.date_of_birth.year - ((today.month, today.day) < (employee.date_of_birth.month, employee.date_of_birth.day))
        return {
            'employee_uid': employee.employee_uid,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'is_active': employee.is_active,
            'country': employee.country,
            'department': employee.department,
            'date_of_birth': employee.date_of_birth,
            'age': age,
        }
  
    def employees_entity(employees):
        employee_list = [
            EmployeeView.employee_entity(employee) for employee in employees
        ]
        return employee_list
    
    def get(self, request):
        query = request.query_params.get('name')
        # Set first_name to be default field and order to be asc
        sort_param = request.query_params.get('sort', 'first_name')
        sort_order = request.query_params.get('order', 'asc')

        if query:
            employees = Employee.objects.filter(first_name__icontains=query)
        else:
            employees = Employee.objects.all()

        valid_sort_fields = ['first_name', 'last_name', 'date_of_birth', 'salary', 'age']

        if sort_param not in valid_sort_fields:
            sort_param = 'first_name'
            
        if sort_param == 'age':
            sort_param = 'date_of_birth'
            sort_order = 'desc' if sort_order == 'asc' else 'asc'

        if sort_order == 'desc':
            sort_param = '-' + sort_param
         
        employees = employees.order_by(sort_param)
        return Response(EmployeeView.employees_entity(employees))

    def post(self, request):
        serializer = EmployeeInformationSerializer(data=request.data)
        if not serializer.is_valid():
            error_response = ErrorHandling.get_response(
                "EMPLOYEE_SIGNUP_SERIALIZER_ERROR",
                ErrorCode.ERROR_HTTP_400_BAD_REQUEST,
                ErrorCode.ERROR_INVALID_OR_MISSING_ARGS_8001,
                serializer.errors,
            )
            return error_response

        data = dict(serializer.validated_data)
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        date_of_birth = data.get("date_of_birth")
        hire_date = data.get("hire_date")
        job_title = data.get("job_title")
        department = data.get("department")
        salary = data.get("salary")
        email = data.get("email")
        phone = data.get("phone")
        address = data.get("address")
        city = data.get("city")
        country = data.get("country")

        employee_component = EmployeeComponent()
        response: EmployeeComponent.Result = employee_component.create_employee(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            hire_date=hire_date,
            job_title=job_title,
            department=department,
            salary=salary,
            email=email,
            phone=phone,
            address=address,
            city=city,
            country=country,
        )
        if not response.is_success:
            return response.errors
        return Response(response.result, status=status.HTTP_200_OK)

    def put(self, request, pk):
        serializer = EmployeeInformationSerializer(data=request.data)
        if not serializer.is_valid():
            error_response = ErrorHandling.get_response(
                "EMPLOYEE_UPDATE_SERIALIZER_ERROR",
                ErrorCode.ERROR_HTTP_400_BAD_REQUEST,
                ErrorCode.ERROR_INVALID_OR_MISSING_ARGS_8001,
                serializer.errors,
            )
            return error_response
        
        data = dict(serializer.validated_data)
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        date_of_birth = data.get("date_of_birth")
        hire_date = data.get("hire_date")
        job_title = data.get("job_title")
        department = data.get("department")
        salary = data.get("salary")
        email = data.get("email")
        phone = data.get("phone")
        address = data.get("address")
        city = data.get("city")
        country = data.get("country")

        employee_component = EmployeeComponent()
        response: EmployeeComponent.Result = employee_component.update_employee(
            employee_uid=pk,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            hire_date=hire_date,
            job_title=job_title,
            department=department,
            salary=salary,
            email=email,
            phone=phone,
            address=address,
            city=city,
            country=country,
        )
        if not response.is_success:
            return response.errors
        return Response(response.result, status=status.HTTP_200_OK)

    def delete(self, pk):
        employee_component = EmployeeComponent()
        response: EmployeeComponent.Result = employee_component.delete_employee(pk)

        if not response.is_success:
            return response.errors
        return Response(response.result, status=status.HTTP_200_OK)
        



