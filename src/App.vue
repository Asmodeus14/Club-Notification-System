<template>
  <SpeedInsights/>
  <div id="app">
    <router-view></router-view> <!-- This will render the current view/component -->
  </div>
</template>

<script>
import { SpeedInsights } from "@vercel/speed-insights/vue"
export default {
  name: 'App',
};
</script>
