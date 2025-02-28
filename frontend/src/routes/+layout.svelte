<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>

<nav>
	<a href="/">Home</a>
	<a href="/companies">Companies</a>
	<a href="/employees">Employees</a>
</nav>

<main>
	{@render children()}
</main>

<style>
	nav {
		padding: 1rem;
		background-color: #f8f9fa;
		display: flex;
		gap: 1rem;
	}

	nav a {
		text-decoration: none;
		color: #333;
	}

	main {
		padding: 2rem;
	}
</style>
