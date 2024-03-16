<script lang="ts">
  import type { Error } from "$lib/types";

  export let error: Error;

</script>

<div id="error-page">
  <h1>Упс!</h1>
  <p>Извините, произошла непредвиденная ошибка.</p>
  <p>
    <i>{error?.statusText || error?.message}</i>
  </p>
</div>
