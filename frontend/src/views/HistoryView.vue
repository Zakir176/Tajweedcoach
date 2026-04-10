<template>
  <div class="history-view max-w-4xl mx-auto p-6">
    <h2 class="text-2xl font-bold mb-6">Practice History</h2>
    
    <div class="space-y-4">
      <div v-for="i in 3" :key="i" class="p-4 border rounded-lg hover:bg-gray-50 transition cursor-pointer flex justify-between items-center shadow-sm bg-white">
        <div>
          <div class="flex items-center gap-2 mb-1">
            <span class="font-bold text-gray-900">Surah Al-Mulk</span>
            <span class="text-sm text-gray-500">Ayah 1</span>
          </div>
          <div class="text-xs text-gray-400">April 8, 2026 • 4.2 seconds</div>
        </div>
        <div class="text-right">
          <div class="text-lg font-bold text-green-600">87%</div>
          <div class="text-xs text-gray-500">Accuracy</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Section 8.1 - HistoryView.vue placeholder
</script>
