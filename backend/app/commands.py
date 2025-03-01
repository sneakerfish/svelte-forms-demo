import click
from faker import Faker
from random import randint
from flask.cli import with_appcontext
from app import db
from app.models import Company, Employee, EmployeeType

fake = Faker()

@click.command('seed-data')
@with_appcontext
def seed_data():
    """Seed the database with fake companies and employees"""
    try:
        # First, get all employee types (assuming they exist)
        employee_types = EmployeeType.query.all()
        if not employee_types:
            click.echo('Warning: No employee types found in database')
            return

        # Create 10 companies
        for _ in range(10):
            company = Company(
                name=fake.company(),
                address=fake.address(),
                url=fake.domain_name()
            )
            db.session.add(company)
            db.session.flush()  # This gets us the company ID

            # Create 1-50 employees for each company
            num_employees = randint(1, 50)
            for _ in range(num_employees):
                employee = Employee(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                    phone=fake.phone_number(),
                    salary=randint(70000, 200000),
                    start_date=fake.date_between(start_date='-5y', end_date='today'),
                    company_id=company.id,
                    employee_type_id=fake.random_element(employee_types).id
                )
                db.session.add(employee)

        db.session.commit()
        click.echo(f'Successfully created 10 companies with random employees')

    except Exception as e:
        db.session.rollback()
        click.echo(f'Error seeding data: {str(e)}') 