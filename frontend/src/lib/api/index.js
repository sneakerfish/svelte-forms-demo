// API base URL
export const API_BASE_URL = 'http://localhost:5050/api';

export async function fetchCompanies() {
    const response = await fetch(`${API_BASE_URL}/companies`);
    if (!response.ok) {
        throw new Error('Failed to fetch companies');
    }
    return response.json();
}

export async function fetchCompanyById(id) {
    const response = await fetch(`${API_BASE_URL}/companies/${id}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch company with id ${id}`);
    }
    return response.json();
}

export async function createCompany(company) {
    const response = await fetch(`${API_BASE_URL}/companies`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(company),
    });
    if (!response.ok) {
        throw new Error('Failed to create company');
    }
    return response.json();
}

export async function fetchEmployees() {
    const response = await fetch(`${API_BASE_URL}/employees`);
    if (!response.ok) {
        throw new Error('Failed to fetch employees');
    }
    return response.json();
}

export async function fetchEmployeeTypes() {
    const response = await fetch(`${API_BASE_URL}/employeeTypes`);
    if (!response.ok) {
        throw new Error('Failed to fetch employee types');
    }
    return response.json();
}

export async function fetchEmployeeById(id) {
    const response = await fetch(`${API_BASE_URL}/employees/${id}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch employee with id ${id}`);
    }
    return response.json();
}

export async function createEmployee(employee) {
    const response = await fetch(`${API_BASE_URL}/employees`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(employee),
    });
    if (!response.ok) {
        throw new Error('Failed to create employee');
    }
    return response.json();
}

export async function updateEmployee(id, employee) {
    const response = await fetch(`${API_BASE_URL}/employees/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(employee),
    });
    if (!response.ok) {
        throw new Error(`Failed to update employee with id ${id}`);
    }
    return response.json();
}

export async function deleteEmployee(id) {
    const response = await fetch(`${API_BASE_URL}/employees/${id}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error(`Failed to delete employee with id ${id}`);
    }
    return response.json();
}

