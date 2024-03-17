<script lang="ts">
  import { Toast } from 'flowbite-svelte';
  import { CheckCircleSolid, CloseSolid } from "flowbite-svelte-icons";
  import { slide } from 'svelte/transition';

  export let message: string;
  export let open = false;
  export let success = false;
</script>

<Toast 
  transition={slide} 
  bind:open 
  position="top-right" 
  color={success ? 'green' : 'red'}
  on:close={() => open = false}
>
<svelte:fragment slot="icon">
  {#if success}
    <CheckCircleSolid slot="icon" class="w-5 h-5" />
  {:else}
    <CloseSolid slot="icon" class="w-5 h-5" />
  {/if}
  <span class="sr-only">Alert Icon</span>
</svelte:fragment>
  {message}
</Toast>
