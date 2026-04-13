import { defineStore } from 'pinia'
import axios from 'axios'

export const useVerseStore = defineStore('verses', {
  state: () => ({
    surahs: [],
    verses: [],
    selectedSurah: null,
    selectedVerse: null,
    loading: false,
    error: null
  }),

  actions: {
    async fetchSurahs() {
      this.loading = true
      try {
        const response = await axios.get('/api/v1/surahs')
        this.surahs = response.data
      } catch (err) {
        this.error = 'Failed to fetch surahs'
        console.error(err)
      } finally {
        this.loading = false
      }
    },

    async fetchVerses(surahId) {
      this.loading = true
      this.verses = []
      this.selectedVerse = null
      try {
        const response = await axios.get(`/api/v1/surahs/${surahId}/verses`)
        this.verses = response.data
        console.log('Verses from API:', response.data)
      } catch (err) {
        this.error = 'Failed to fetch verses'
        console.error(err)
      } finally {
        this.loading = false
      }
    },

    setSurah(surah) {
      this.selectedSurah = surah
      if (surah) {
        this.fetchVerses(surah.id)
      }
    },

    setVerse(verse) {
      this.selectedVerse = verse
    }
  }
})
