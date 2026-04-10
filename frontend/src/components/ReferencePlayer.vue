<template>
  <div class="reference-player p-4 border rounded-lg shadow-sm">
    <div class="flex items-center gap-4">
      <button class="bg-indigo-600 text-white p-3 rounded-full hover:bg-indigo-700 transition">
        <!-- Play Icon -->
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </button>
      
      <div class="flex-grow">
        <h4 class="text-sm font-semibold">Reference Recitation</h4>
        <p class="text-xs text-gray-500">Sheikh Mishary Al-Afasy</p>
      </div>

      <div class="flex gap-2">
        <button class="text-xs border px-2 py-1 rounded hover:bg-gray-50">0.75x</button>
        <button class="text-xs border px-2 py-1 bg-gray-100 rounded">1.0x</button>
        <button class="text-xs border px-2 py-1 rounded hover:bg-gray-50">1.25x</button>
      </div>
    </div>
  </div>
</template>

<script setup>
// Section 8.1 - ReferencePlayer.vue placeholder
</script>
