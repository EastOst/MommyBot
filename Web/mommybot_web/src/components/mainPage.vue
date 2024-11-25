<template>
  <div class="main-page">
    <div class="greetings">
      <h1>{{ greetingMessage }}</h1>
    </div>
    <div id="calendar"></div> <!-- 캘린더 렌더링할 영역 -->
    <button @click="goToSettings">사용자 설정</button>
    
  </div>
</template>

<script>
import { mapState } from "vuex";
import { onMounted } from "vue";
import {
  createCalendar,
  createViewDay,
  createViewMonthAgenda,
  createViewMonthGrid,
  createViewWeek,
} from "@schedule-x/calendar";
import "@schedule-x/theme-default/dist/index.css";

export default {
  name: "MainPage",
  methods: {
    goToSettings() {
      this.$router.push("/settings");
    },
    getPostfix(name) {
      const lastChar = name[name.length - 1];
      const code = lastChar.charCodeAt(0);
      const hasJongseong = (code - 44032) % 28 !== 0;
      return hasJongseong ? "아" : "야";
    },
  },
  computed: {
    ...mapState(["firstName"]),
    greetingMessage() {
      return `${this.firstName}${this.getPostfix(this.firstName)} 엄마다!`;
    },
  },
  setup() {
    // 캘린더 초기화
    onMounted(() => {
      const calendar = createCalendar({
        views: [
          createViewDay(),
          createViewWeek(),
          createViewMonthGrid(),
          createViewMonthAgenda(),
        ],
        events: [
          {
            id: 1,
            title: "시연회",
            start: "2024-12-05 10:00",
            end: "2024-12-05 17:00",
          },
        ],
      });

      // 캘린더를 렌더링할 DOM 요소 지정
      calendar.render(document.getElementById("calendar"));
    });
  },
};
</script>

<style scoped>
.main-page {
  text-align: center;
  margin-top: 60px;
}
.greetings h1 {
  font-size: 2em;
}
#calendar {
  width: 100%;
  height: 600px;
  margin: 20px auto;
}
</style>
