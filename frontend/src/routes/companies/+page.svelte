<script lang="ts">
	import { onMount } from 'svelte';
	import Modal from '$lib/components/Modal.svelte';
	import { createCompany, fetchCompanies } from '$lib/api/index.js';
	import type { Company } from '$lib/api';

	let companies = $state<Company[]>([]);
	let showAddModal = $state(false);
	let newCompany = $state({
		name: '',
		address: '',
		phone: '',
		url: ''
	});
	let error = $state<string | null>(null);

	onMount(async () => {
		try {
			const response = await fetchCompanies();
			companies = response;
		} catch (e) {
			error = e instanceof Error ? e.message : 'An error occurred while fetching companies';
		}
	});

	async function handleSubmit(event: Event) {
		event.preventDefault();
		const response = await createCompany(newCompany);
		console.log('Company created:', response);
		const createdCompany = await response;
		companies = [...companies, createdCompany];
			
		// Reset form
		newCompany = {
			name: '',
			address: '',
			phone: '',
			url: ''
		};
		showAddModal = false;
	}
</script>

<div class="page-header">
	<h1>Companies</h1>
	<button class="add-button" onclick={() => showAddModal = true}>
		Add Company
	</button>
</div>

{#if error}
	<div class="error-message">
		{error}
	</div>
{/if}

<div class="companies-grid">
	{#each companies as company}
		<div class="company-card">
			<h2>{company.name}</h2>
			<div class="company-details">
				<p>{company.address}</p>
				<p>Phone: {company.phone}</p>
				<p>Website: <a href={company.url} target="_blank" rel="noopener noreferrer">{company.url}</a></p>
			</div>
		</div>
	{/each}
</div>

<Modal 
	show={showAddModal} 
	title="Add New Company"
	on:close={() => showAddModal = false}
>
	<form onsubmit={handleSubmit} class="add-form">
		<div class="form-group">
			<label for="name">Company Name</label>
			<input 
				type="text" 
				id="name" 
				bind:value={newCompany.name} 
				required
			/>
		</div>
		<div class="form-group">
			<label for="address">Address</label>
			<input 
				type="text" 
				id="address" 
				bind:value={newCompany.address} 
				required
			/>
		</div>
		<div class="form-group">
			<label for="phone">Phone</label>
			<input 
				type="tel" 
				id="phone" 
				bind:value={newCompany.phone} 
				required
			/>
		</div>
		<div class="form-group">
			<label for="url">Website URL</label>
			<input 
				type="url" 
				id="url" 
				bind:value={newCompany.url} 
				required
			/>
		</div>
		<div class="form-actions">
			<button type="button" class="cancel" onclick={() => showAddModal = false}>
				Cancel
			</button>
			<button type="submit" class="submit">
				Add Company
			</button>
		</div>
	</form>
</Modal>

<style>
	.page-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 2rem;
	}

	.add-button {
		background: #4CAF50;
		color: white;
		border: none;
		padding: 0.5rem 1rem;
		border-radius: 4px;
		cursor: pointer;
		font-size: 1rem;
	}

	.add-button:hover {
		background: #45a049;
	}

	.companies-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
		gap: 1rem;
		padding: 1rem 0;
	}

	.company-card {
		background: white;
		padding: 1rem;
		border-radius: 8px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.company-card h2 {
		margin: 0 0 0.5rem 0;
		font-size: 1.2rem;
	}

	.company-card p {
		margin: 0;
		color: #666;
	}

	.add-form {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.form-group {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.form-group label {
		font-weight: 500;
	}

	.form-group input {
		padding: 0.5rem;
		border: 1px solid #ddd;
		border-radius: 4px;
		font-size: 1rem;
	}

	.form-actions {
		display: flex;
		gap: 1rem;
		justify-content: flex-end;
		margin-top: 1rem;
	}

	.form-actions button {
		padding: 0.5rem 1rem;
		border-radius: 4px;
		cursor: pointer;
		font-size: 1rem;
		border: none;
	}

	.cancel {
		background: #f1f1f1;
		color: #333;
	}

	.submit {
		background: #4CAF50;
		color: white;
	}

	.submit:hover {
		background: #45a049;
	}

	.error-message {
		background-color: #fee;
		color: #c00;
		padding: 1rem;
		border-radius: 4px;
		margin-bottom: 1rem;
	}
</style> 