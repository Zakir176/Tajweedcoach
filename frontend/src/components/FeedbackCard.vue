<template>
  <div class="bg-white rounded-2xl p-8 border border-gray-100 shadow-sm card-hover overflow-hidden animate-in fade-in zoom-in duration-500 mt-6">
    <div class="flex justify-between items-center mb-6">
      <h3 class="text-xl font-black text-indigo-950 flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-indigo-600"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        AI Analysis
      </h3>
      <div class="flex flex-col items-end">
        <span class="text-3xl font-black text-indigo-600">{{ (feedback.accuracy_score * 100).toFixed(1) }}%</span>
        <span class="text-[10px] uppercase tracking-widest text-gray-400 font-bold">Accuracy Score</span>
      </div>
    </div>
    
    <div class="mb-8">
      <h4 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Word-by-Word Analysis</h4>
      <div class="flex flex-wrap gap-4 text-3xl dir-rtl font-serif bg-gray-50/50 p-8 rounded-2xl border border-gray-100 shadow-inner">
        <span 
          v-for="(item, index) in feedback.diff" 
          :key="index"
          :class="[
            item.status === 'correct' ? 'text-emerald-600' : 'text-red-600 underline decoration-wavy decoration-red-200'
          ]"
          class="transition-colors hover:bg-white px-1 rounded-md cursor-default"
        >
          {{ item.word }}
        </span>
      </div>
    </div>
    
    <div class="bg-indigo-50/50 p-6 rounded-2xl border border-indigo-100 relative overflow-hidden group">
      <div class="absolute -right-4 -top-4 text-indigo-500/10 group-hover:scale-110 transition-transform duration-700">
        <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
      </div>
      <h4 class="text-xs font-black text-indigo-600 uppercase tracking-tighter mb-2 flex items-center gap-2">
        Coach's Advice
      </h4>
      <p class="text-gray-700 leading-relaxed italic text-sm">
        "{{ feedback.feedback }}"
      </p>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  feedback: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.dir-rtl {
  direction: rtl;
}
</style>
