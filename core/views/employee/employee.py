from .employee_crud import EmployeeView


def employee_view():
    return EmployeeView.as_view()
