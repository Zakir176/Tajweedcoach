<template>
  <div v-if="versesStore.selectedVerse" class="bg-white/80 backdrop-blur-md rounded-2xl p-6 border border-indigo-100 shadow-xl mt-6 animate-in fade-in zoom-in duration-500">
    <div class="flex flex-col gap-4">
      
      <!-- Header & Sheikh Selector -->
      <div class="flex justify-between items-center sm:flex-row flex-col gap-4 border-b border-indigo-50 pb-4">
        <h4 class="text-lg font-bold text-gray-900 flex items-center gap-2 self-start sm:self-auto">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-indigo-600"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path><path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path></svg>
          Reference Audio
        </h4>
        
        <select 
          v-model="sheikhCode" 
          class="bg-white text-gray-700 text-sm border border-indigo-200 rounded-lg px-3 py-1.5 focus:ring-2 focus:ring-indigo-500 outline-none appearance-none pr-8 cursor-pointer relative self-start sm:self-auto w-full sm:w-auto shadow-sm"
          style="background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%234F46E5%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E'); background-repeat: no-repeat; background-position: right .7rem top 50%; background-size: .65rem auto;"
        >
          <option v-for="sheikh in sheikhOptions" :key="sheikh.code" :value="sheikh.code">{{ sheikh.name }}</option>
        </select>
      </div>

      <!-- Selected Sheikh Name Display -->
      <div class="text-center py-2">
        <p class="text-xs font-semibold tracking-wider text-indigo-400 uppercase mb-1">Now Playing</p>
        <p class="text-xl font-bold text-gray-800">{{ selectedSheikhName }}</p>
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
        @play="isPlaying = true"
        @pause="isPlaying = false"
        autoplay
      ></audio>

      <!-- Status Indicator -->
      <div v-if="isLoading" class="flex justify-center items-center gap-2 text-indigo-600 text-sm italic py-4">
        <div class="animate-spin h-5 w-5 border-2 border-indigo-600 border-t-transparent rounded-full"></div>
        Loading audio...
      </div>
      <div v-else-if="audioError" class="text-red-600 text-sm text-center py-3 bg-red-50 rounded-lg px-3 border border-red-100">
        {{ audioError }}
      </div>

      <!-- Controls UI (Only show when loaded and no error) -->
      <div v-if="!isLoading && !audioError && duration > 0" class="flex flex-col gap-4 mt-2 bg-indigo-50/50 p-4 rounded-xl border border-indigo-50">
        
        <!-- Progress Bar -->
        <div class="w-full bg-indigo-200 rounded-full h-2 cursor-pointer relative group" @click="seekAudio">
          <div class="bg-indigo-600 h-2 rounded-full relative transition-[width] duration-100" :style="{ width: progressPercentage + '%' }">
            <div class="absolute -right-2 -top-1.5 w-5 h-5 bg-white border-2 border-indigo-600 rounded-full shadow-sm pointer-events-none transition-transform group-active:scale-110"></div>
          </div>
        </div>
        
        <div class="flex justify-between text-xs text-indigo-600 font-medium px-1 mt-[-8px]">
            <span>{{ formatTime(currentTime) }}</span>
            <span>{{ formatTime(duration) }}</span>
        </div>

        <div class="flex items-center justify-between">
          
          <!-- Replay Button -->
          <button 
            @click="replayAudio" 
            class="p-2 text-indigo-400 hover:text-indigo-600 hover:bg-indigo-100 rounded-full transition-colors"
            title="Replay from start"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          </button>

          <!-- Play / Pause Controls -->
          <button 
            @click="togglePlay" 
            class="w-14 h-14 rounded-full bg-indigo-600 hover:bg-indigo-700 text-white flex items-center justify-center transition-all shadow-md hover:shadow-lg hover:scale-105 active:scale-95"
          >
            <svg v-if="!isPlaying" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="translate-x-[2px]"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>
          </button>

          <!-- Speed Controls -->
          <div class="flex bg-indigo-100/80 rounded-lg p-1 border border-indigo-200">
            <button 
              v-for="rate in [0.75, 1, 1.25]" 
              :key="rate"
              @click="setSpeed(rate)"
              class="px-2 py-1 text-xs font-bold rounded-md transition-colors"
              :class="playbackRate === rate ? 'bg-white text-indigo-700 shadow-sm' : 'text-indigo-500 hover:text-indigo-700 hover:bg-indigo-50'"
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
import { useVerseStore as useVersesStore } from '@/stores/verses'

const versesStore = useVersesStore()
const audioRef = ref(null)

const sheikhOptions = [
  { name: 'Husary',  code: 'Husary_128kbps' },
  { name: 'Sudais',  code: 'Abdurrahmaan_As-Sudais_192kbps' },
]

const sheikhCode = ref('Husary_128kbps')
const isPlaying = ref(false)
const isLoading = ref(false)
const audioError = ref(null)
const currentTime = ref(0)
const duration = ref(0)
const playbackRate = ref(1)

const selectedSheikhName = computed(() => {
  const option = sheikhOptions.find(o => o.code === sheikhCode.value)
  return option ? option.name : ''
})

// Compute URL
const audioUrl = computed(() => {
  const verse = versesStore.selectedVerse
  if (!verse || !verse.surah_id || !verse.ayah_number) return ''
  
  const surah = verse.surah_id.toString().padStart(3, '0')
  const ayah = verse.ayah_number.toString().padStart(3, '0')
  
  return `https://everyayah.com/data/${sheikhCode.value}/${surah}${ayah}.mp3`
})

// Progress percentage
const progressPercentage = computed(() => {
  if (!duration.value) return 0
  return (currentTime.value / duration.value) * 100
})

const formatTime = (time) => {
    if (isNaN(time)) return "0:00";
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

// Watchers to auto-load logic
watch([() => versesStore.selectedVerse, sheikhCode], () => {
  if (versesStore.selectedVerse) {
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
  } else {
    // If it was ended, restart
    if (currentTime.value >= duration.value) {
      audioRef.value.currentTime = 0
    }
    audioRef.value.play().catch(e => console.error("Playback failed", e))
  }
}

const replayAudio = () => {
  if (!audioRef.value) return
  audioRef.value.currentTime = 0
  audioRef.value.play().catch(e => console.error(e))
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
