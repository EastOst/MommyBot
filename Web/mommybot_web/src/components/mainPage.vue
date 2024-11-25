<template>
  <div class="main-page">
    <div class="greetings">
      <h1>{{ greetingMessage }}</h1>
    </div>
    <div id="calendar"></div> <!-- 캘린더 렌더링할 영역 -->
    <div class="button-group">
      <button @click="addEvent">일정 추가</button>
    </div>
    <button class="settings-button" @click="goToSettings">Go to Settings</button>
  </div>
</template>

<script>
import { mapState } from "vuex"; 
import {
  createCalendar,
  createViewDay,
  createViewWeek,
  createViewMonthGrid,
  createViewMonthAgenda,
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
    addEvent() {
      // 새로운 이벤트 추가
      const newEvent = {
        id: this.events.length + 1,
        title: `New Event ${this.events.length + 1}`,
        start: "2024-11-26 14:00",
        end: "2024-11-26 15:00",
      };

      // 이벤트 배열 업데이트
      this.events.push(newEvent);

      // 캘린더를 재렌더링
      this.renderCalendar();
    },
    renderCalendar() {
      // 기존 캘린더를 제거하고 새로 생성
      if (this.calendar) {
        this.calendar.destroy(); // 기존 캘린더 제거 (필요 시)
      }
      this.calendar = createCalendar({
        views: [
          createViewDay(),
          createViewWeek(),
          createViewMonthGrid(),
          createViewMonthAgenda(),
        ],
        events: this.events,
      });
      this.calendar.render(document.getElementById("calendar"));
    },
  },
  computed: {
    ...mapState(["firstName"]),
    greetingMessage() {
      return `${this.firstName}${this.getPostfix(this.firstName)} 엄마다!`;
    },
  },
  data() {
    return {
      calendar: null, // 캘린더 인스턴스
      events: [
        {
          id: 1,
          title: "Meeting",
          start: "2024-11-25 10:00",
          end: "2024-11-25 11:00",
        },
      ],
    };
  },
  mounted() {
    this.renderCalendar(); // 캘린더 초기 렌더링
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
.button-group {
  margin-top: 20px;
}
button {
  margin: 0 10px;
  padding: 10px 20px;
  font-size: 16px;
}
.settings-button {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.settings-button:hover {
  background-color: #0056b3;
}
</style>
