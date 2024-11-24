<template>
    <div class="main-page">
      <div class="greetings">
        <h1>{{ greetingMessage }}</h1>
      </div>
      <button @click="goToSettings">Go to Settings</button>
    </div>
  </template>
  
  <script>
  import { mapState } from "vuex";
  
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
  </style>
  