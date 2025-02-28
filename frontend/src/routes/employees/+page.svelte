<script lang="ts">
    import { onMount } from 'svelte';
    import { type Employee, type Company, type EmployeeType } from '$lib/api';
    import { fetchEmployees } from '$lib/api/index.js';


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
                    <td>{companies.find(c => c.id === employee.company_id)?.name || ''}</td>
                    <td>{employee.email}</td>
                    <td>{employee.phone}</td>
                </tr>
            {/each}
        </tbody>
    </table>
</div>

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