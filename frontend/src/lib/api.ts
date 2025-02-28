export interface Employee {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    position: string;
    department: string;
    type: EmployeeType;
    phone: string;
    company_id: number;
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

const API_BASE_URL = 'http://localhost:5000/api';

export async function fetchCompanies(): Promise<Company[]> {
    const response = await fetch(`${API_BASE_URL}/companies`);
    if (!response.ok) {
        throw new Error('Failed to fetch companies');
    }
    return response.json();
}

export async function fetchEmployees(): Promise<Employee[]> {
    const response = await fetch(`${API_BASE_URL}/employees`);
    if (!response.ok) {
        throw new Error('Failed to fetch employees');
    }
    return response.json();
} 