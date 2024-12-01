<template>
  <div class="main-page">
    <div class="greetings">
      <h1>{{ greetingMessage }}</h1>
    </div>
    <div id="calendar"></div> <!-- 캘린더 렌더링할 영역 -->

    <div class="event-controls">
      <h2>일정 추가</h2>
      <form @submit.prevent="addEvent">
        <input v-model="newEvent.title" placeholder="일정 제목" required />
        <input v-model="newEvent.start" type="datetime-local" required />
        <input v-model="newEvent.end" type="datetime-local" required />
        <button type="submit">추가</button>
      </form>

      <h2>일정 삭제</h2>
      <form @submit.prevent="deleteEvent">
        <input v-model="eventIdToDelete" type="number" placeholder="일정 ID" required />
        <button type="submit">삭제</button>
      </form>
    </div>

    <button @click="goToSettings">사용자 설정</button>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { onMounted, ref } from "vue";
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
    addEvent() {
  const newId = this.events.length ? this.events[this.events.length - 1].id + 1 : 1;

  // Convert input datetime to the desired format
  const formattedStart = this.newEvent.start.replace("T", " ");
  const formattedEnd = this.newEvent.end.replace("T", " ");

  // Push the new event with the formatted dates
  this.events.push({
    id: newId,
    title: this.newEvent.title,
    start: formattedStart,
    end: formattedEnd,
  });

  // Reset form
  this.newEvent = { title: "", start: "", end: "" };

  // Re-render calendar
  this.renderCalendar();
},
    deleteEvent() {
      const index = this.events.findIndex(event => event.id === parseInt(this.eventIdToDelete, 10));
      if (index !== -1) {
        this.events.splice(index, 1);
        this.eventIdToDelete = ""; // Reset form
        this.renderCalendar();
      } else {
        alert("일정 ID를 찾을 수 없습니다.");
      }
    },
    renderCalendar() {
      const calendar = createCalendar({
        views: [
          createViewDay(),
          createViewWeek(),
          createViewMonthGrid(),
          createViewMonthAgenda(),
        ],
        events: this.events,
      });
      calendar.render(document.getElementById("calendar"));
    },
  },
  computed: {
    ...mapState(["firstName"]),
    greetingMessage() {
      return `${this.firstName}${this.getPostfix(this.firstName)} 엄마다!`;
    },
  },
  setup() {
    const events = ref([
      {
        id: 1,
        title: "시연회",
        start: "2024-12-05 10:00",
        end: "2024-12-05 17:00",
      },
    ]);

    const newEvent = ref({
      title: "",
      start: "",
      end: "",
    });

    const eventIdToDelete = ref("");

    onMounted(() => {
      const calendar = createCalendar({
        views: [
          createViewDay(),
          createViewWeek(),
          createViewMonthGrid(),
          createViewMonthAgenda(),
        ],
        events: events.value,
      });
      calendar.render(document.getElementById("calendar"));
    });

    return {
      events,
      newEvent,
      eventIdToDelete,
    };
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
.event-controls {
  margin-top: 20px;
  text-align: left;
}
.event-controls h2 {
  font-size: 1.5em;
  margin-bottom: 10px;
}
.event-controls form {
  margin-bottom: 20px;
}
.event-controls input {
  margin: 5px;
  padding: 5px;
}
</style>
