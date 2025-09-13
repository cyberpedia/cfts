import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useSolvesStore = defineStore('solves', () => {
  // State
  const solvedChallengeIds = ref(new Set());

  // Actions
  function populateUserSolves(solvesArray) {
    solvedChallengeIds.value.clear();
    if (solvesArray && solvesArray.length) {
      solvesArray.forEach(solve => {
        solvedChallengeIds.value.add(solve.challenge_id);
      });
    }
  }
  
  function clearSolves() {
      solvedChallengeIds.value.clear();
  }

  return { solvedChallengeIds, populateUserSolves, clearSolves };
});
