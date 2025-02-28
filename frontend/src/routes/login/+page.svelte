<script>
    import { goto } from '$app/navigation';
    import api from '$lib/api';
    import { login } from '$lib/stores/auth';

    let email = '';
    let password = '';
    let error = '';

    async function handleSubmit() {
        try {
            const response = await api.post('/auth/login', { email, password });
            login(response.data.access_token, { email });
            goto('/companies');
        } catch (err) {
            error = err.response?.data?.error || 'Login failed';
        }
    }
</script>

<!-- Rest of the template remains the same --> 