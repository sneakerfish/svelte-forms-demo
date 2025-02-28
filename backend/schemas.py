from pydantic import BaseModel
from typing import Optional, List

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    position: str
    department: str
    company_id: int

class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True

class CompanyBase(BaseModel):
    name: str
    industry: str

class Company(CompanyBase):
    id: int
    employees: List[Employee] = []

    class Config:
        from_attributes = True 