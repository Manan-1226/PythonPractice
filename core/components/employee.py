from core.models.employee import Employee
from core.components import ErrorCode, ErrorHandling


class EmployeeComponent:
    def __init__(self) -> None:
        pass

    class Result:
        def __init__(self, is_success, errors, result=None):
            self.is_success = is_success
            self.errors = errors
            self.result = result

    def create_employee(
        self,
        first_name,
        last_name,
        date_of_birth,
        hire_date,
        job_title,
        department,
        salary,
        email,
        phone,
        address,
        city,
        country,
    ):
        employee_qs = Employee.objects.filter(email=email).first()
        if employee_qs:
            error_response = ErrorHandling.get_response(
                "SIGNUP_ERROR",
                ErrorCode.ERROR_HTTP_400_BAD_REQUEST,
                ErrorCode.ERROR_HTTP_409_CONFLICT,
                "USER_ALREADY_EXISTS",
            )
            return EmployeeComponent.Result(False, True, error_response)

        newEmplyee = Employee.objects.create(
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
        newEmplyee.save()
        message = {"message": "Employee sucessfully registered"}

        return EmployeeComponent.Result(True, None, message)

    def update_employee(
        self,
        employee_uid,
        first_name,
        last_name,
        date_of_birth,
        hire_date,
        job_title,
        department,
        salary,
        email,
        phone,
        address,
        city,
        country,
    ):
        try:
            employee = Employee.objects.get(employee_uid=employee_uid)
        except Employee.DoesNotExist:
            
            error_response = ErrorHandling.get_response(
                "EMPLOYEE UPDATE ERROR",
                ErrorCode.ERROR_HTTP_404_NOT_FOUND,
                ErrorCode.ERROR_INVALID_OR_MISSING_ARGS_8001,
                "Employee does not exist"
            )
            return EmployeeComponent.Result(False, error_response)

        employee.first_name = first_name
        employee.last_name = last_name
        date_of_birth = date_of_birth
        hire_date = hire_date
        job_title = job_title
        department = department
        salary = salary
        email = email
        phone = phone
        address = address
        city = city
        country = country
        
        employee.save()
        message = {"message": "Employee details successfully updated."}

        return EmployeeComponent.Result(True, None, message)

    def delete_employee(self, pk):

        try:
            employee = Employee.objects.get(employee_uid=pk).delete()
        except Employee.DoesNotExist:
            error_response = ErrorHandling.get_response(
                "EMPLOYEE DELETE ERROR",
                ErrorCode.ERROR_HTTP_404_NOT_FOUND,
                ErrorCode.ERROR_INVALID_OR_MISSING_ARGS_8001,
                "Employee does not exist",
            )
            return EmployeeComponent.Result(False, error_response)
        
        # employee = Employee.objects.get(employee_id = pk)
        # print (employee)
        # if not employee:
        #     print ("hi")
        #     return EmployeeComponent.Result(False, "error", "employee not exists")
        
        employee.save()
        message = {"message": "Employee details deleted successfully."}

        return EmployeeComponent.Result(True, None, message)