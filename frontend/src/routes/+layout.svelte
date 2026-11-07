<script lang="ts">
  import { onMount } from 'svelte';
  import '../app.css';
  import Nav from '$lib/Nav.svelte';
  import { isAuthenticated, checkAuth } from '$lib/auth';

  onMount(async () => {
    checkAuth();
    if (!('serviceWorker' in navigator)) return;
    try {
      await navigator.serviceWorker.register('/sw.js', { scope: '/' });
    } catch {
      // Service worker registration is optional; app works online
    }
  });
</script>

{#if $isAuthenticated}
  <Nav />
{/if}

<slot />
