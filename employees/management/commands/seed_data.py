from django.core.management.base import BaseCommand
from faker import Faker
from employees.models import Employee
from departments.models import Department
from attendance.models import Attendance
from performance.models import Performance
from random import choice, randint
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seeds the database with fake data'
    
    def handle(self, *args, **kwargs):
        fake = Faker()
        Department.objects.all().delete()
        Employee.objects.all().delete()
        Attendance.objects.all().delete()
        Performance.objects.all().delete()
        
        #create departments
        departments = ['HR', 'Engineering', 'Sales', 'Marketing', 'Finance']
        dept_objects = [Department.objects.create(name=name) for name in departments]
        
        #create employees
        for _ in range(50):
            Employee.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                phone_number=fake.phone_number()[:15],
                address=fake.address(),
                date_joined=fake.date_between(start_date='-5y', end_date='today'),
                department=choice(dept_objects)
            )
            
            #create attendance
            employees = Employee.objects.all()
            for employee in employees:
                for i in range(30):
                    Attendance.objects.create(
                        employee=employee,
                        date=date.today() - timedelta(days=i),
                        status=choice(['P', 'A', 'L'])
                    )
                    
            #create performance
            for employee in employees:
                for _ in range(3):
                    Performance.objects.create(
                        employee=employee,
                        rating=randint(1, 5),
                        review_date=fake.date_between(start_date='-2y', end_date='today')
                    )
            
            self.stdout.write(self.style.SUCCESS('Successfully seeded database'))