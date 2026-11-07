
from abc import ABC, abstractmethod


# Abstract Employee class
class Employee(ABC):

    def __init__(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid employee name")

        self.name = name

    @abstractmethod
    def calculate_pay(self):
        pass


# Salaried Employee
class SalariedEmployee(Employee):

    def __init__(self, name, monthly_salary):
        super().__init__(name)

        if monthly_salary < 0:
            raise ValueError("Salary cannot be negative")

        self.monthly_salary = monthly_salary

    def calculate_pay(self):
        return self.monthly_salary


# Hourly Employee
class HourlyEmployee(Employee):

    def __init__(self, name, hourly_rate, hours):
        super().__init__(name)

        if hourly_rate < 0 or hours < 0:
            raise ValueError("Rate and hours cannot be negative")

        self.hourly_rate = hourly_rate
        self.hours = hours

    def calculate_pay(self):

        regular_hours = min(self.hours, 40)
        overtime_hours = max(self.hours - 40, 0)

        regular_pay = regular_hours * self.hourly_rate
        overtime_pay = overtime_hours * self.hourly_rate * 1.5

        return regular_pay + overtime_pay


# Commission Employee
class CommissionEmployee(Employee):

    def __init__(self, name, base_salary, sales, rate):
        super().__init__(name)

        if base_salary < 0 or sales < 0 or not 0 <= rate <= 1:
            raise ValueError("Invalid commission details")

        self.base_salary = base_salary
        self.sales = sales
        self.rate = rate

    def calculate_pay(self):
        return self.base_salary + (self.sales * self.rate)


# Payroll Summary
def generate_payroll(employees):

    if not all(isinstance(employee, Employee) for employee in employees):
        raise TypeError("All records must be Employee objects")

    summary = []

    for employee in employees:

        summary.append({
            "employee": employee.name,
            "type": type(employee).__name__,
            "pay": employee.calculate_pay()
        })

    return summary


# Sample Employees
employees = [
    SalariedEmployee("Ali", 5000),
    HourlyEmployee("Sara", 20, 45),
    CommissionEmployee("Ahmed", 500, 4000, 0.10)
]

# Generate Payroll
payroll = generate_payroll(employees)

for record in payroll:
    print(record)

print("Total Payroll:", sum(item["pay"] for item in payroll))
