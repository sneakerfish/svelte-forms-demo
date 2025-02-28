from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
from database import engine, get_db
import schemas

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data to populate the database
SAMPLE_COMPANIES = [
    {"name": "Acme Corp", "industry": "Technology"},
    {"name": "Globex", "industry": "Manufacturing"},
    {"name": "Initech", "industry": "Software"},
    {"name": "Umbrella Corp", "industry": "Biotechnology"},
    {"name": "Wayne Enterprises", "industry": "Technology"}
]

SAMPLE_EMPLOYEES = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@acme.com",
        "position": "Software Engineer",
        "department": "Engineering",
        "company_id": 1
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@globex.com",
        "position": "Product Manager",
        "department": "Product",
        "company_id": 2
    },
    {
        "first_name": "Mike",
        "last_name": "Johnson",
        "email": "mike.johnson@initech.com",
        "position": "UX Designer",
        "department": "Design",
        "company_id": 3
    },
    {
        "first_name": "Sarah",
        "last_name": "Wilson",
        "email": "sarah.wilson@umbrella.com",
        "position": "Research Scientist",
        "department": "R&D",
        "company_id": 4
    },
    {
        "first_name": "David",
        "last_name": "Brown",
        "email": "david.brown@wayne.com",
        "position": "Project Manager",
        "department": "Operations",
        "company_id": 5
    }
]

@app.on_event("startup")
async def populate_db():
    db = SessionLocal()
    
    # Check if we already have data
    if db.query(models.Company).count() == 0:
        # Add companies
        for company_data in SAMPLE_COMPANIES:
            company = models.Company(**company_data)
            db.add(company)
        db.commit()

        # Add employees
        for employee_data in SAMPLE_EMPLOYEES:
            employee = models.Employee(**employee_data)
            db.add(employee)
        db.commit()
    
    db.close()

@app.get("/api/companies", response_model=List[schemas.Company])
def get_companies(db: Session = Depends(get_db)):
    return db.query(models.Company).all()

@app.get("/api/employees", response_model=List[schemas.Employee])
def get_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all() 