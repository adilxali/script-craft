import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface UserProgressState {
  completedLessons: string[]
  streakDays: number
  totalXP: number
  lastActiveDate: string
  activeModuleSlug: string
  activeLessonSlug: string
}

export const useProgressStore = defineStore('progress', () => {
  const completedLessons = ref<string[]>([
    '01-foundations/01-closures'
  ])
  const streakDays = ref<number>(5)
  const totalXP = ref<number>(350)
  const activeModuleSlug = ref<string>('01-foundations')
  const activeLessonSlug = ref<string>('01-closures')

  const totalModules = ref<number>(4)
  const totalLessonsCount = ref<number>(12)

  const progressPercentage = computed(() => {
    return Math.round((completedLessons.value.length / totalLessonsCount.value) * 100)
  })

  function completeLesson(lessonPath: string, xpReward: number = 50) {
    if (!completedLessons.value.includes(lessonPath)) {
      completedLessons.value.push(lessonPath)
      totalXP.value += xpReward
      saveProgress()
    }
  }

  function isLessonCompleted(lessonPath: string): boolean {
    return completedLessons.value.includes(lessonPath)
  }

  function saveProgress() {
    if (import.meta.client) {
      localStorage.setItem('scriptcraft_progress', JSON.stringify({
        completedLessons: completedLessons.value,
        streakDays: streakDays.value,
        totalXP: totalXP.value,
        activeModuleSlug: activeModuleSlug.value,
        activeLessonSlug: activeLessonSlug.value
      }))
    }
  }

  function loadProgress() {
    if (import.meta.client) {
      const raw = localStorage.getItem('scriptcraft_progress')
      if (raw) {
        try {
          const parsed = JSON.parse(raw)
          if (parsed.completedLessons) completedLessons.value = parsed.completedLessons
          if (parsed.streakDays) streakDays.value = parsed.streakDays
          if (parsed.totalXP) totalXP.value = parsed.totalXP
          if (parsed.activeModuleSlug) activeModuleSlug.value = parsed.activeModuleSlug
          if (parsed.activeLessonSlug) activeLessonSlug.value = parsed.activeLessonSlug
        } catch (e) {
          console.error('Failed to parse progress from localStorage', e)
        }
      }
    }
  }

  return {
    completedLessons,
    streakDays,
    totalXP,
    activeModuleSlug,
    activeLessonSlug,
    progressPercentage,
    totalModules,
    totalLessonsCount,
    completeLesson,
    isLessonCompleted,
    saveProgress,
    loadProgress
  }
})
