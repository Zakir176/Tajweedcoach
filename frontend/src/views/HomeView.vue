<template>
  <div class="home-view max-w-4xl mx-auto p-6">
    <header class="mb-8 text-center">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Tajweed Recitation Coach</h1>
      <p class="text-gray-600">Improve your Quran recitation with AI feedback</p>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div class="space-y-6">
        <VerseSelector />
      </div>

      <div class="space-y-6">
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
import ReferencePlayer from '../components/ReferencePlayer.vue'

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
