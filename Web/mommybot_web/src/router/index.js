import { createRouter, createWebHistory } from "vue-router";
import loginPage from "@/components/loginPage.vue";
import settingsPage from "@/components/settingsPage.vue";
import mainPage from "@/components/mainPage.vue";
import store from "@/store"; // Vuex 스토어 가져오기

const routes = [
  { path: "/login", component: loginPage },
  { path: "/settings", component: settingsPage },
  {
    path: "/",
    component: mainPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 전역 가드 추가
router.beforeEach((to, from, next) => {
  const { firstName, lastName, birthDate, lmsID, lmsPassword } = store.state;
  const isLoggedIn = localStorage.getItem("isLoggedIn"); // 로그인 상태 확인

  // 로그인하지 않은 상태에서는 항상 로그인 페이지로 이동
  if (!isLoggedIn && to.path !== "/login") {
    next("/login");
    return;
  }

  // 로그인 후, 사용자 정보가 없으면 설정 페이지로 이동
  if (
    isLoggedIn &&
    (!firstName || !lastName || !birthDate || !lmsID || !lmsPassword) &&
    to.path !== "/settings"
  ) {
    next("/settings");
    return;
  }

  // 모든 조건을 만족하면 정상적으로 이동
  next();
});

export default router;
