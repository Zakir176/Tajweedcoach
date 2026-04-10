<template>
  <div class="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 shadow-xl overflow-hidden animate-in fade-in zoom-in duration-500">
    <div class="flex justify-between items-center mb-6">
      <h3 class="text-xl font-bold text-white flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-cyan-400"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        AI Analysis
      </h3>
      <div class="flex flex-col items-end">
        <span class="text-3xl font-black text-cyan-400">{{ Math.round(feedback.accuracy_score * 100) }}%</span>
        <span class="text-[10px] uppercase tracking-widest text-white/40 font-bold">Accuracy Score</span>
      </div>
    </div>
    
    <div class="mb-8">
      <h4 class="text-xs font-bold text-white/50 uppercase tracking-widest mb-4">Word-by-Word Analysis</h4>
      <div class="flex flex-wrap gap-3 text-2xl dir-rtl font-amiri bg-black/20 p-6 rounded-xl border border-white/5">
        <span 
          v-for="(item, index) in feedback.diff" 
          :key="index"
          :class="[
            item.status === 'correct' ? 'text-emerald-400' : 'text-red-400 underline decoration-wavy decoration-red-900/50'
          ]"
          class="transition-colors hover:bg-white/5 px-1 rounded-sm cursor-default"
        >
          {{ item.word }}
        </span>
      </div>
    </div>
    
    <div class="bg-gradient-to-br from-cyan-900/40 to-blue-900/40 p-5 rounded-xl border border-cyan-500/20 relative overflow-hidden group">
      <div class="absolute -right-4 -top-4 text-cyan-500/10 group-hover:scale-110 transition-transform duration-700">
        <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
      </div>
      <h4 class="text-xs font-black text-cyan-400 uppercase tracking-tighter mb-2 flex items-center gap-2">
        Coach's Advice
      </h4>
      <p class="text-white/90 leading-relaxed italic text-sm">
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
