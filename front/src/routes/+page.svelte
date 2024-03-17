<script lang="ts">
  import { goto } from '$app/navigation';
  import { isAuthenticated } from '$lib/stores';
  import { onMount } from 'svelte';

  onMount(() => {
    $isAuthenticated ? goto('/dashboard') : goto('/login');
  });
</script>
