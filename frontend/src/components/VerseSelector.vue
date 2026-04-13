<script setup>
import { onMounted, computed, ref, watch } from 'vue'
import { useVerseStore } from '../stores/verses'

const store = useVerseStore()

onMounted(() => {
  store.fetchSurahs()
})

const selectedSurahId = ref(null)
const selectedVerseId = ref(null)

// When surah changes, reset ayah and notify store
watch(selectedSurahId, (newId) => {
    selectedVerseId.value = null
    const surah = store.surahs.find(s => s.id === parseInt(newId))
    store.setSurah(surah)
})

// When ayah changes, notify store
watch(selectedVerseId, (newId) => {
    if (!newId) return
    const verse = store.verses.find(v => v.id === parseInt(newId))
    store.setVerse(verse)
})

const surahOptions = computed(() => store.surahs)
const verseOptions = computed(() => store.verses)
</script>

<template>
  <div class="max-w-4xl mx-auto p-6 space-y-8 bg-white/50 backdrop-blur-md border border-white/20 rounded-2xl shadow-xl transition-all duration-300">
    
    <!-- Selectors Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Surah Dropdown -->
      <div class="space-y-2">
        <label for="surah-select" class="block text-sm font-medium text-indigo-900/70 ml-1">Surah</label>
        <div class="relative group">
          <select 
            id="surah-select"
            v-model="selectedSurahId"
            class="block w-full px-4 py-3 text-gray-700 bg-white border border-indigo-100 rounded-xl shadow-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all appearance-none"
          >
            <option :value="null" disabled>Select a Surah</option>
            <option v-for="surah in surahOptions" :key="surah.id" :value="surah.id">
              {{ surah.id }}. {{ surah.name_english }} ({{ surah.ayah_count }} verses)
            </option>
          </select>
          <div class="absolute right-4 top-1/2 -translate-y-1/2 p-1 pointer-events-none opacity-50 group-hover:opacity-100 transition-opacity">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Ayah Dropdown -->
      <div class="space-y-2 transition-all duration-500" :class="{ 'opacity-100 translate-y-0': store.selectedSurah, 'opacity-0 translate-y-2 pointer-events-none': !store.selectedSurah }">
        <label for="ayah-select" class="block text-sm font-medium text-indigo-900/70 ml-1">Ayah</label>
        <div class="relative group">
          <select 
            id="ayah-select"
            v-model="selectedVerseId"
            class="block w-full px-4 py-3 text-gray-700 bg-white border border-indigo-100 rounded-xl shadow-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all appearance-none"
          >
            <option :value="null" disabled>Select Ayah</option>
            <option v-for="verse in verseOptions" :key="verse.id" :value="verse.id">
              Ayah {{ verse.ayah_number }}
            </option>
          </select>
          <div class="absolute right-4 top-1/2 -translate-y-1/2 p-1 pointer-events-none opacity-50 group-hover:opacity-100 transition-opacity">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="store.loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-500"></div>
    </div>

    <!-- Results Display -->
    <div v-else-if="store.selectedVerse" class="space-y-6 pt-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div class="text-center space-y-8">
        <!-- Arabic Text -->
        <h2 class="font-serif text-5xl md:text-6xl leading-[1.6] text-gray-900 dir-rtl px-4 py-8 bg-indigo-50/30 rounded-3xl border border-indigo-100/50 shadow-inner overflow-x-auto whitespace-normal">
          {{ store.selectedVerse.text_arabic }}
        </h2>
        
        <!-- English Translation -->
        <div class="max-w-2xl mx-auto space-y-2">
            <div class="p-4 rounded-xl border border-indigo-50 bg-white/80 shadow-sm relative group overflow-hidden">
                <div class="absolute inset-0 bg-gradient-to-r from-indigo-500/0 via-indigo-500/5 to-indigo-500/0 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
                <p class="text-lg text-gray-600 italic relative z-10 leading-relaxed">
                    "{{ store.selectedVerse.text_english }}"
                </p>
                <div class="mt-4 flex justify-center">
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-700 uppercase tracking-widest border border-indigo-200">
                        {{ store.selectedSurah.name_english }} : {{ store.selectedVerse.ayah_number }}
                    </span>
                </div>
            </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!store.loading" class="text-center py-20 opacity-30 select-none">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto mb-4 text-indigo-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
        </svg>
        <p class="text-xl font-medium">Search for a verse to begin</p>
    </div>
  </div>
</template>

<style scoped>
/* Ensure Arabic font and layout work nicely */
.font-serif {
    font-family: 'Amiri', "Scheherazade New", serif;
}

select {
  background-image: none !important;
}

/* Custom fade animations */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
