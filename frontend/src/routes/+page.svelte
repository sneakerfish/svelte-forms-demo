<script lang="ts">
    import { onMount } from 'svelte';
    import Modal from '$lib/components/Modal.svelte';
    import { createCompany, fetchCompanies, fetchEmployeesByCompanyId } from '$lib/api/index.js';
    import type { Company, Employee } from '$lib/api';

    let companies = $state<Company[]>([]);
    let employees = $state<Employee[]>([]);
    let showAddModal = $state(false);
    let newCompany = $state({
        name: '',
        address: '',
        phone: '',
        url: ''
    });
    let error = $state<string | null>(null);
    let searchTerm = '';
    let selectedCompany = $state<Company | null>(null);
    let sortBy = 'name'; // Default sort
    let sortOrder = 'asc';

    onMount(async () => {
        try {
            const response = await fetchCompanies();
            companies = response;
        } catch (e) {
            error = e instanceof Error ? e.message : 'An error occurred while fetching companies';
        }
    });

    async function handleCompanyClick(company) {
        selectedCompany = company;
        const response = await fetchEmployeesByCompanyId(company.id);
        console.log("Employees:", response);
        employees = response;
    }

    async function handleSortHeaderClick(columnName) {
        if (sortBy === columnName) {
            sortOrder = sortOrder === 'asc' ? 'desc' : 'asc'; // Toggle order
        } else {
            sortBy = columnName;
            sortOrder = 'asc'; // Default to ascending when changing column
        }
        const response = await fetchEmployeesByCompanyId(selectedCompany.id, columnName);
        console.log("Employees:", response);
        employees = response;

    }
</script>

<div class="flex h-screen">
    <div class="w-1/4 p-4 border-r">
        <input type="text" placeholder="Search companies..." bind:value={searchTerm} class="w-full p-2 border rounded mb-2">
        <ul class="space-y-2">
            {#each companies as company}
                <li class="p-2 bg-white rounded shadow cursor-pointer hover:bg-gray-100" on:click={() => handleCompanyClick(company)}>
                    {company.name}
                </li>
            {/each}
        </ul>
    </div>

    <div class="w-3/4 p-4">
        {#if selectedCompany}
            <h2 class="text-2xl font-bold mb-4">{selectedCompany.name}</h2>
            <div class="company-details">
                <p>{selectedCompany.address}</p>
                <p>Phone: {selectedCompany.phone}</p>
                <p>Website: <a href={selectedCompany.url} target="_blank" rel="noopener noreferrer">{selectedCompany.url}</a></p>
            </div>

            <h3 class="text-xl font-semibold mb-2">Employee Roster</h3>
            {#if employees.length > 0}
                <table class="w-full">
                    <thead>
                    <tr>
                        <th class="cursor-pointer" on:click={() => handleSortHeaderClick('name')}>Name</th>
                        <th class="cursor-pointer" on:click={() => handleSortHeaderClick('salary')}>Salary</th>
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
                            <td>${employee.salary}</td>
                            <td>{employee.email}</td>
                            <td>{employee.phone}</td>
                            <td>{employee.type.name}</td>
                            <td>{employee.start_date}</td>
                        </tr>
                    {/each}
                    </tbody>
                </table>
            {:else}
                <p>No employees in this company yet.</p>
            {/if}
        {:else}
            <p>Select a company to view its details and employee roster.</p>
        {/if}
    </div>
</div>
