<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    
    let { show = false, title = '', children } = $props();
    const dispatch = createEventDispatcher();

    function closeModal() {
        dispatch('close');
    }

    function handleKeydown(event: KeyboardEvent) {
        if (event.key === 'Escape') {
            closeModal();
        }
    }
</script>

{#if show}
    <div 
        class="modal-container"
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        onkeydown={handleKeydown}
        tabindex="-1"
    >
        <button 
            type="button"
            class="modal-backdrop"
            onclick={closeModal}
            aria-label="Close modal background"
        >x</button>
        <div class="modal">
            <div class="modal-header">
                <h2 id="modal-title">{title}</h2>
                <button 
                    type="button" 
                    class="close-button" 
                    onclick={closeModal}
                    aria-label="Close modal"
                >
                    &times;
                </button>
            </div>
            <div class="modal-content">
                {@render children()}
            </div>
        </div>
    </div>
{/if}

<style>
    .modal-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }

    .modal-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        border: none;
        padding: 0;
        margin: 0;
        cursor: pointer;
    }

    .modal {
        position: relative;
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        width: 90%;
        max-width: 500px;
        max-height: 90vh;
        overflow-y: auto;
        z-index: 1001;
    }

    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }

    .modal-header h2 {
        margin: 0;
        font-size: 1.5rem;
    }

    .close-button {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        padding: 0.5rem;
    }

    .close-button:hover {
        color: #666;
    }
</style> 