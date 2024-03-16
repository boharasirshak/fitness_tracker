<script lang="ts">
  import { goto } from "$app/navigation";
  import { isAuthenticated } from "$lib/stores";
  </script>

{#if $isAuthenticated}
  {
    goto("/dashboard").then(() => {})
  }
{:else}
  {
    goto("/login").then(() => {})
  }
{/if}
