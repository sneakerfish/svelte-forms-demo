export interface Employee {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    position: string;
    department: string;
    type: EmployeeType;
    phone: string;
    company: Company;
    start_date: string;
    salary: number;
}

export interface Company {
    id: number;
    name: string;
    address: string;
    phone: string;
    url: string;
}

export interface EmployeeType {
    id: number;
    name: string;
}

