<template>
    <div class="login-page">
      <h1>로그인</h1>
      <input type="password" v-model="password" placeholder="비밀번호를 입력하세요" />
      <button @click="login">로그인</button>
      <span v-if="errorMessage">{{ errorMessage }}</span>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        password: "",
        errorMessage: "",
      };
    },
    methods: {
      login() {
        const savedPassword = localStorage.getItem("appPassword");
        if (this.password === savedPassword) {
          localStorage.setItem("isLoggedIn", true);
          this.$router.push("/");
        } else {
          this.errorMessage = "비밀번호가 일치하지 않습니다.";
        }
      },
    },
    mounted() {
      if (!localStorage.getItem("appPassword")) {
        localStorage.setItem("appPassword", "1234");
      }
    },
  };
  </script>
  
  <style scoped>
  .login-page {
    max-width: 400px;
    margin: 100px auto;
    text-align: center;
  }
  </style>
  