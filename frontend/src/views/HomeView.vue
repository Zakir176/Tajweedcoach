<template>
  <div class="home-view max-w-7xl mx-auto p-6">
    <header class="mb-12 text-center">
      <h1 class="text-4xl md:text-5xl font-black text-indigo-950 mb-4 tracking-tight">Tajweed Recitation Coach</h1>
      <p class="text-lg text-gray-400 font-medium max-w-lg mx-auto">Master your Quran recitation with precise AI-powered feedback</p>
    </header>

    <div class="grid grid-cols-1 lg:grid-cols-5 gap-8 items-start">
      <div class="space-y-6 lg:col-span-3">
        <VerseSelector />
      </div>

      <div class="space-y-6 lg:col-span-2">
        <AudioRecorder @success="handleRecordingSuccess" />
        <FeedbackCard v-if="currentFeedback" :feedback="currentFeedback" />
        <ReferencePlayer />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import VerseSelector from '../components/VerseSelector.vue'
import AudioRecorder from '../components/AudioRecorder.vue'
import FeedbackCard from '../components/FeedbackCard.vue'
import ReferencePlayer from '@/components/ReferencePlayer.vue'

const currentFeedback = ref(null)

const handleRecordingSuccess = (feedback) => {
  currentFeedback.value = feedback
}
</script>

<style scoped>
.dir-rtl {
  direction: rtl;
}
</style>
