# frontend/src/components/Footer.vue
<template>
  <footer class="bg-gray-800 p-4 text-center text-gray-400 text-sm mt-auto">
    <div class="container mx-auto">
      &copy; {{ new Date().getFullYear() }} CTF Platform. All rights reserved.
    </div>
  </footer>
</template>

<script setup>
// No script logic needed for a static footer
</script>

<style scoped>
/* Tailwind CSS handles most of the styling */
</style>
