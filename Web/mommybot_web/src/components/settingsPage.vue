<template>
    <div class="settings-page">
      <h1>여기는 설정페이지다</h1>
      <div class="form-container">
        <div class="name-section">
          <h3>이름</h3>
          <input v-model="userLastName" placeholder="성을 입력하세요: " />
          <input v-model="userFirstName" placeholder="이름을 입력하세요: " />
        </div>
        <div class="date-section">
          <h3>생년월일</h3>
          <div class="date-wrap">
            <label for="date">생년월일 : </label>
            <input
              id="date"
              v-model="userBirthDate"
              @input="onInputHandler"
              placeholder="YYYY-MM-DD"
              maxlength="10"
            />
          </div>
          <span class="warning" v-if="!isValidDate && userBirthDate.length === 10">
            유효하지 않은 날짜입니다.
          </span>
        </div>
        <div class="lms-section">
          <h3>LMS 정보</h3>
          <label for="LMS_ID">LMS ID(학번): </label>
          <input v-model="userLmsID" placeholder="ID: " />
          <label for="LMS_Password">LMS Password: </label>
          <input type="password" v-model="userLmsPassword" placeholder="Password: " />
        </div>
        <div class="button-group">
          <button @click="submitAll">정보 저장</button>
          <button @click="resetFields" class="reset-button">초기화</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapActions, mapState } from "vuex";
  
  export default {
    data() {
      return {
        userLastName: "",
        userFirstName: "",
        userBirthDate: "",
        userLmsID: "",
        userLmsPassword: "",
      };
    },
    computed: {
      ...mapState(["firstName", "lastName", "birthDate", "lmsID", "lmsPassword"]),
      isValidDate() {
        return this.checkValidDate(this.userBirthDate);
      },
    },
    methods: {
      ...mapActions(["setLastName", "setFirstName", "setBirthDate", "setLmsID", "setLmsPassword"]),
      submitAll() {
  this.$store.commit("updateState", { key: "lastName", value: this.userLastName });
  this.$store.commit("updateState", { key: "firstName", value: this.userFirstName });
  this.$store.commit("updateState", { key: "birthDate", value: this.userBirthDate });
  this.$store.commit("updateState", { key: "lmsID", value: this.userLmsID });
  this.$store.commit("updateState", { key: "lmsPassword", value: this.userLmsPassword });
  
  this.$router.push("/");
},
      resetFields() {
        this.userLastName = "";
        this.userFirstName = "";
        this.userBirthDate = "";
        this.userLmsID = "";
        this.userLmsPassword = "";
      },
      onInputHandler() {
        let value = this.userBirthDate.replace(/\D/g, "");
        let length = value.length;
  
        if (length < 6) {
          this.userBirthDate = value;
        } else if (length < 8) {
          this.userBirthDate = value.slice(0, 4) + "-" + value.slice(4);
        } else {
          this.userBirthDate = value.slice(0, 4) + "-" + value.slice(4, 6) + "-" + value.slice(6);
        }
      },
      checkValidDate(value) {
        const regex = /^\d{4}-\d{2}-\d{2}$/;
        if (!regex.test(value)) return false;
  
        const [year, month, day] = value.split("-").map(Number);
        const date = new Date(year, month - 1, day);
  
        return (
          date.getFullYear() === year &&
          date.getMonth() === month - 1 &&
          date.getDate() === day
        );
      },
      loadSavedData() {
        this.userLastName = this.lastName;
        this.userFirstName = this.firstName;
        this.userBirthDate = this.birthDate;
        this.userLmsID = this.lmsID;
        this.userLmsPassword = this.lmsPassword;
      },
    },
    mounted() {
      this.loadSavedData();
    },
  };
  </script>
  
  <style scoped>
  /* 기존 스타일 유지 */
  </style>
  