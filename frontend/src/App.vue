<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <nav class="bg-white border-b shadow-sm">
      <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <router-link to="/" class="text-xl font-bold bg-gradient-to-r from-indigo-600 to-blue-500 bg-clip-text text-transparent">
          TajweedCoach
        </router-link>
        
        <div class="flex gap-6">
          <router-link to="/" class="text-gray-600 hover:text-indigo-600 transition">Practice</router-link>
          <router-link to="/history" class="text-gray-600 hover:text-indigo-600 transition">History</router-link>
          <router-link to="/auth" class="bg-indigo-600 text-white px-4 py-1.5 rounded-lg hover:bg-indigo-700 transition">Login</router-link>
        </div>
      </div>
    </nav>

    <main class="flex-grow">
      <router-view />
    </main>

    <footer class="bg-white border-t py-6 text-center text-gray-500 text-sm">
      &copy; 2026 Tajweed Recitation Coach. Built with Vue 3 and FastAPI.
    </footer>
  </div>
</template>

<script setup>
// Main App Component
</script>
