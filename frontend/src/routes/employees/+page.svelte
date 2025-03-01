<script lang="ts">
    import { onMount } from 'svelte';
    import { type Employee, type Company, type EmployeeType } from '$lib/api';
    import { fetchEmployees, fetchCompanies, fetchEmployeeTypes } from '$lib/api/index.js';
    import Modal from '$lib/components/Modal.svelte';


    let employees = $state<Employee[]>([]);
    let companies = $state<Company[]>([]);
    let employeeTypes = $state<EmployeeType[]>([]);
    let showAddModal = $state(false);
    let newEmployee = $state({
        first_name: '',
        last_name: '',
        company_id: '',
        email: '',
        phone: '',
        employee_type_id: '',
        start_date: ''
    });

    onMount(async () => {
        console.log('Component mounted');
        try {
            const response = await fetchEmployees();
            console.log('Employees:', response);
            employees = response;

            const companiesResponse = await fetchCompanies();
            console.log('Companies:', companiesResponse.companies);
            companies = companiesResponse.companies;

            const employeeTypesResponse = await fetchEmployeeTypes();
            console.log('Employee types:', employeeTypesResponse);
            employeeTypes = employeeTypesResponse;
        } catch (e) {
            let error = e instanceof Error ? e.message : 'An error occurred while fetching employees';
        }



    });

    async function handleSubmit(event) {
        console.log('Form submitted');
        event.preventDefault();
        const formData = new FormData(event.target);
        const employeeData = Object.fromEntries(formData);
        console.log('Employee data:', employeeData);

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}api/employees/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(employeeData)
            });

            if (response.ok) {
                const newEmployee = await response.json();
                console.log('New employee added:', newEmployee);
                employees = [...employees, newEmployee];
                event.target.reset();
            }
        } catch (error) {
            console.error('Error adding employee:', error);
        }
    }
</script>

<div class="container">
    <h1>Employees</h1>
    <button class="add-button" onclick={() => showAddModal = true}>
        Add Employee
    </button>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Company</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Type</th>
                <th>Start Date</th>
            </tr>
        </thead>
        <tbody>
            {#each employees as employee}
                <tr>
                    <td>{employee.first_name} {employee.last_name}</td>
                    <td>{ employee.company_name }</td>
                    <td>{employee.email}</td>
                    <td>{employee.phone}</td>
                </tr>
            {/each}
        </tbody>
    </table>
</div>

<Modal
  show={showAddModal}
  title="Add New Employee"
  on:close={() => showAddModal = false}
>
    <form onsubmit={handleSubmit} class="add-form">
        <div class="form-group">
            <label for="first_name">First Name</label>
            <input type="text" id="first_name" name="first_name" required>
        </div>
        <div class="form-group">
            <label for="last_name">Last Name</label>
            <input type="text" id="last_name" name="last_name" required>
        </div>
        <div class="form-group">
            <label for="company_id">Company</label>
            <select id="company_id" name="company_id" required>
                <option value="">Select a company</option>
                {#each companies as company}
                    <option value={company.id}>{company.name}</option>
                {/each}
            </select>
        </div>
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" required>
        </div>
        <div class="form-group">
            <label for="phone">Phone</label>
            <input type="tel" id="phone" name="phone" required>
        </div>
        <div class="form-group">
            <label for="employee_type_id">Employee Type</label>
            <select id="employee_type_id" name="employee_type_id" required>
                <option value="">Select an employee type</option>
                {#each employeeTypes as type}
                    <option value={type.id}>{type.name}</option>
                {/each}
            </select>
        </div>
        <div class="form-group">
            <label for="start_date">Start Date</label>
            <input type="date" id="start_date" name="start_date" required>
        </div>
        <button type="submit">Add Employee</button>
    </form>
</Modal>

<style>
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }

    .form-group {
        margin-bottom: 1rem;
    }

    label {
        display: block;
        margin-bottom: 5px;
    }

    input, select, textarea {
        width: 100%;
        padding: 8px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }

    button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    button:hover {
        background-color: #45a049;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }

    th, td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }

    th {
        background-color: #f2f2f2;
    }

    select {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
</style> 