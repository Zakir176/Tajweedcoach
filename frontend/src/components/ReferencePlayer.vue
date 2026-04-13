<template>
  <div v-if="verseStore.selectedVerse" class="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 shadow-xl mt-6 animate-in fade-in zoom-in duration-500">
    <div class="flex flex-col gap-4">
      
      <!-- Header & Sheikh Selector -->
      <div class="flex justify-between items-center sm:flex-row flex-col gap-4">
        <h4 class="text-lg font-bold text-white flex items-center gap-2 self-start sm:self-auto">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-indigo-400"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path><path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path></svg>
          Reference Audio
        </h4>
        
        <select 
          v-model="sheikhCode" 
          class="bg-black/20 text-white text-sm border border-white/10 rounded-lg px-3 py-1.5 focus:ring-2 focus:ring-indigo-500 outline-none appearance-none pr-8 cursor-pointer relative self-start sm:self-auto w-full sm:w-auto"
          style="background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23FFFFFF%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E'); background-repeat: no-repeat; background-position: right .7rem top 50%; background-size: .65rem auto;"
        >
          <option value="Husary_128kbps" class="text-gray-900">Sheikh Husary</option>
          <option value="Minshawi_128kbps" class="text-gray-900">Sheikh Minshawi</option>
          <option value="Afasy_128kbps" class="text-gray-900">Sheikh Al-Afasy</option>
        </select>
      </div>

      <!-- Audio Element (Hidden) -->
      <audio 
        ref="audioRef" 
        :src="audioUrl" 
        preload="auto"
        @canplay="onCanPlay"
        @error="onError"
        @timeupdate="onTimeUpdate"
        @ended="isPlaying = false"
      ></audio>

      <!-- Status Indicator -->
      <div v-if="isLoading" class="flex items-center gap-2 text-indigo-300 text-sm italic py-2">
        <div class="animate-spin h-4 w-4 border-2 border-indigo-400 border-t-transparent rounded-full"></div>
        Loading audio...
      </div>
      <div v-else-if="audioError" class="text-red-400 text-sm py-2 bg-red-900/20 rounded-lg px-3 border border-red-900/40">
        {{ audioError }}
      </div>

      <!-- Controls UI (Only show when loaded and no error) -->
      <div v-if="!isLoading && !audioError && duration > 0" class="flex flex-col gap-3 mt-2">
        
        <!-- Progress Bar -->
        <div class="w-full bg-black/30 rounded-full h-1.5 cursor-pointer relative" @click="seekAudio">
          <div class="bg-indigo-500 h-1.5 rounded-full relative" :style="{ width: progressPercentage + '%' }">
            <div class="absolute -right-1.5 -top-1.5 w-3 h-3 bg-white rounded-full shadow-sm shadow-indigo-900 pointer-events-none transition-transform active:scale-150"></div>
          </div>
        </div>

        <div class="flex items-center justify-between">
          
          <!-- Play / Replay Controls -->
          <div class="flex items-center gap-3">
            <button 
              @click="togglePlay" 
              class="w-10 h-10 rounded-full bg-indigo-600 hover:bg-indigo-500 text-white flex items-center justify-center transition-all shadow-lg hover:scale-105 active:scale-95"
            >
              <svg v-if="!isPlaying" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="translate-x-[1px]"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>
            </button>

            <button 
              @click="replayAudio" 
              class="p-2 text-white/70 hover:text-white hover:bg-white/10 rounded-full transition-colors"
              title="Replay from start"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
            </button>
          </div>

          <!-- Speed Controls -->
          <div class="flex bg-black/20 rounded-lg p-1 border border-white/5">
            <button 
              v-for="rate in [0.75, 1, 1.25]" 
              :key="rate"
              @click="setSpeed(rate)"
              class="px-2 py-1 text-xs font-medium rounded-md transition-colors"
              :class="playbackRate === rate ? 'bg-indigo-600 text-white shadow-sm' : 'text-white/60 hover:text-white hover:bg-white/10'"
            >
              {{ rate }}x
            </button>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useVerseStore } from '../stores/verses'

const verseStore = useVerseStore()
const audioRef = ref(null)

const sheikhCode = ref('Husary_128kbps')
const isPlaying = ref(false)
const isLoading = ref(false)
const audioError = ref(null)
const currentTime = ref(0)
const duration = ref(0)
const playbackRate = ref(1)

// Compute URL
const audioUrl = computed(() => {
  const verse = verseStore.selectedVerse
  if (!verse) return ''
  
  const surah = verse.surah_id.toString().padStart(3, '0')
  const ayah = verse.ayah_number.toString().padStart(3, '0')
  
  return `https://everyayah.com/data/${sheikhCode.value}/${surah}${ayah}.mp3`
})

// Progress percentage
const progressPercentage = computed(() => {
  if (!duration.value) return 0
  return (currentTime.value / duration.value) * 100
})

// Watchers to auto-load logic
watch([() => verseStore.selectedVerse, sheikhCode], () => {
  if (verseStore.selectedVerse) {
    isLoading.value = true
    audioError.value = null
    isPlaying.value = false
    currentTime.value = 0
    duration.value = 0
  }
})

// Audio Events
const onCanPlay = () => {
  isLoading.value = false
  if (audioRef.value) {
    duration.value = audioRef.value.duration
    audioRef.value.playbackRate = playbackRate.value // Maintain speed
  }
}

const onError = () => {
  isLoading.value = false
  audioError.value = "Audio unavailable for this verse."
  isPlaying.value = false
}

const onTimeUpdate = () => {
  if (audioRef.value) {
    currentTime.value = audioRef.value.currentTime
  }
}

// Player Controls
const togglePlay = () => {
  if (!audioRef.value) return
  if (isPlaying.value) {
    audioRef.value.pause()
    isPlaying.value = false
  } else {
    // If it was ended, restart
    if (currentTime.value >= duration.value) {
      audioRef.value.currentTime = 0
    }
    audioRef.value.play().catch(e => console.error("Playback failed", e))
    isPlaying.value = true
  }
}

const replayAudio = () => {
  if (!audioRef.value) return
  audioRef.value.currentTime = 0
  audioRef.value.play().catch(e => console.error(e))
  isPlaying.value = true
}

const setSpeed = (rate) => {
  playbackRate.value = rate
  if (audioRef.value) {
    audioRef.value.playbackRate = rate
  }
}

const seekAudio = (e) => {
  if (!audioRef.value || !duration.value) return
  const rect = e.currentTarget.getBoundingClientRect()
  const clickPosition = (e.clientX - rect.left) / rect.width
  audioRef.value.currentTime = clickPosition * duration.value
  currentTime.value = audioRef.value.currentTime
}
</script>
