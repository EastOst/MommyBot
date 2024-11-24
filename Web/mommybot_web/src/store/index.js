import { createStore } from "vuex";

// 로컬 스토리지에서 상태 불러오기
function getSavedState() {
  try {
    return JSON.parse(localStorage.getItem("userState")) || {};
  } catch (error) {
    console.error("로컬 스토리지 접근 실패:", error);
    return {};
  }
}

// 로컬 스토리지에 상태 저장
function saveState(state) {
  try {
    localStorage.setItem("userState", JSON.stringify(state));
  } catch (error) {
    console.error("로컬 스토리지 저장 실패:", error);
  }
}

const store = createStore({
  state() {
    const savedState = getSavedState();
    return {
      firstName: savedState.firstName || "",
      lastName: savedState.lastName || "",
      birthDate: savedState.birthDate || "",
      lmsID: savedState.lmsID || "",
      lmsPassword: savedState.lmsPassword || "",
    };
  },
  mutations: {
    updateState(state, { key, value }) {
      state[key] = value;
    },
  },
  actions: {
    updateState({ commit }, payload) {
      commit("updateState", payload);
    },
  },
});

// Vuex 상태 변경을 감지하고 로컬 스토리지에 저장
store.subscribe((mutation, state) => {
  saveState(state);
});

export default store;
