<template>
  <div class="auth-view min-h-[60vh] flex items-center justify-center p-6">
    <div class="w-full max-w-md bg-white p-8 rounded-xl shadow-lg border">
      <h2 class="text-2xl font-bold text-center mb-6">Welcome Back</h2>
      
      <form class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Email Address</label>
          <input type="email" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm border p-2" />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700">Password</label>
          <input type="password" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm border p-2" />
        </div>
        
        <button type="submit" class="w-full bg-indigo-600 text-white py-2 rounded-lg font-semibold hover:bg-indigo-700 transition mt-4">
          Login
        </button>
      </form>
      
      <div class="mt-6 text-center text-sm">
        <span class="text-gray-500">Don't have an account?</span>
        <button class="text-indigo-600 font-semibold ml-1">Register</button>
      </div>
    </div>
  </div>
</template>

<script setup>
// Section 8.1 - AuthView.vue placeholder
</script>
