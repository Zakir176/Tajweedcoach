<script setup>
import { ref, onUnmounted, computed, watch } from 'vue'
import { useVerseStore } from '@/stores/verses'
import axios from 'axios'

const verseStore = useVerseStore()
const isRecording = ref(false)
const audioBlob = ref(null)
const audioUrl = ref(null)
const isLoading = ref(false)
const error = ref(null)
const canvasRef = ref(null)

let mediaRecorder = null
let audioContext = null
let analyser = null
let animationId = null
let chunks = []

const canRecord = computed(() => !!verseStore.selectedVerse)

// Watch for verse changes to reset state
watch(() => verseStore.selectedVerse, () => {
  resetState()
})

const resetState = () => {
  audioBlob.value = null
  audioUrl.value = null
  error.value = null
  if (animationId) cancelAnimationFrame(animationId)
}

const startRecording = async () => {
  try {
    error.value = null
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    
    // Setup Audio Visualization
    setupVisualization(stream)
    
    mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' })
    chunks = []
    
    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) chunks.push(e.data)
    }
    
    mediaRecorder.onstop = () => {
      audioBlob.value = new Blob(chunks, { type: 'audio/webm' })
      audioUrl.value = URL.createObjectURL(audioBlob.value)
      stream.getTracks().forEach(track => track.stop())
    }
    
    mediaRecorder.start()
    isRecording.value = true
  } catch (err) {
    console.error('Mic error:', err)
    if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
      error.value = 'Microphone access denied. Please allow camera/microphone permissions in your browser settings and click Record again.'
    } else if (err.name === 'NotFoundError') {
      error.value = 'No microphone detected. Please plug in a microphone and try again.'
    } else {
      error.value = `Microphone error: ${err.message}. Please try refreshing the page.`
    }
  }
}

const stopRecording = () => {
  if (mediaRecorder && isRecording.value) {
    mediaRecorder.stop()
    isRecording.value = false
    if (animationId) cancelAnimationFrame(animationId)
  }
}

const setupVisualization = (stream) => {
  audioContext = new (window.AudioContext || window.webkitAudioContext)()
  const source = audioContext.createMediaStreamSource(stream)
  analyser = audioContext.createAnalyser()
  analyser.fftSize = 256
  source.connect(analyser)
  
  const bufferLength = analyser.frequencyBinCount
  const dataArray = new Uint8Array(bufferLength)
  
  const canvas = canvasRef.value
  const ctx = canvas.getContext('2d')
  
  const draw = () => {
    animationId = requestAnimationFrame(draw)
    analyser.getByteFrequencyData(dataArray)
    
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    
    const barWidth = (canvas.width / bufferLength) * 2.5
    let x = 0
    
    for (let i = 0; i < bufferLength; i++) {
      const barHeight = (dataArray[i] / 255) * canvas.height
      
      ctx.fillStyle = `rgb(${barHeight + 100}, 50, 50)`
      ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight)
      
      x += barWidth + 1
    }
  }
  
  draw()
}

const submitRecitation = async () => {
  if (!audioBlob.value || !verseStore.selectedVerse) return
  
  isLoading.value = true
  error.value = null
  
  const formData = new FormData()
  formData.append('audio_file', audioBlob.value, 'recitation.webm')
  console.log('Sending verse_id:', verseStore.selectedVerse.id)
  formData.append('verse_id', verseStore.selectedVerse.id)
  
  try {
    const response = await axios.post('/api/v1/recitations/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    // Emit for parent component (FeedbackCard)
    emit('success', response.data)
  } catch (err) {
    console.error('Upload error:', err)
    error.value = 'Failed to upload recitation. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const emit = defineEmits(['success'])

onUnmounted(() => {
  if (animationId) cancelAnimationFrame(animationId)
  if (audioContext) audioContext.close()
})
</script>

<template>
  <div v-if="canRecord" class="bg-white rounded-2xl p-8 border border-gray-100 shadow-sm card-hover mt-8">
    <div class="text-center">
      <h3 class="text-xl font-bold mb-6 text-indigo-900">Record Recitation</h3>

      <!-- Waveform Canvas -->
      <div class="relative h-24 mb-6 bg-black/20 rounded-xl overflow-hidden">
        <canvas ref="canvasRef" width="400" height="100" class="w-full h-full"></canvas>
        <div v-if="!isRecording && !audioUrl" class="absolute inset-0 flex flex-col items-center justify-center text-gray-400 gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="opacity-80"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
          <span class="text-sm font-medium">Ready to capture your recitation</span>
        </div>
      </div>

      <!-- Controls -->
      <div class="flex flex-col items-center gap-6">
        <div class="relative">
          <button
            v-if="!isRecording"
            @click="startRecording"
            class="w-20 h-20 rounded-full bg-red-600 hover:bg-red-500 flex items-center justify-center transition-all hover:scale-105 active:scale-95 shadow-lg shadow-red-900/40 text-white"
            :disabled="isLoading"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
          </button>

          <button
            v-else
            @click="stopRecording"
            class="w-20 h-20 rounded-full bg-gray-800 border-4 border-red-600 flex items-center justify-center transition-all animate-pulse"
          >
            <div class="w-6 h-6 bg-red-600 rounded-sm"></div>
          </button>
        </div>

        <!-- Feedback & Error -->
        <p v-if="!isRecording && !audioUrl" class="text-sm font-bold text-gray-400 uppercase tracking-widest mt-[-1rem]">Tap to Record</p>

        <p v-if="error" class="text-red-400 text-sm bg-red-900/20 px-4 py-2 rounded-lg border border-red-900/40">
          {{ error }}
        </p>

        <!-- Preview & Submit -->
        <div v-if="audioUrl && !isRecording" class="w-full space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div class="flex items-center justify-center bg-gray-50 rounded-xl p-4">
            <audio :src="audioUrl" controls class="w-full h-10 opacity-80"></audio>
          </div>
          
          <button
            @click="submitRecitation"
            class="w-full py-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold transition-all shadow-md flex items-center justify-center gap-2 group"
            :disabled="isLoading"
          >
            <span v-if="!isLoading" class="flex items-center gap-2">
              Submit Recitation
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="transition-transform group-hover:translate-x-1"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
            </span>
            <span v-else class="flex items-center gap-2">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              Analyzing...
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Chrome/Safari audio player custom styles helper */
audio::-webkit-media-controls-enclosure {
  background-color: transparent;
}
</style>
