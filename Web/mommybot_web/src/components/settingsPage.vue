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
        <input v-model="lmsID" placeholder="ID: " />
        <label for="LMS_Password">LMS Password: </label>
        <input type="password" v-model="lmsPassword" placeholder="Password: " />
      </div>
      <div class="button-group">
        <button @click="submitAll">정보 저장</button>
        <button @click="resetFields" class="reset-button">초기화</button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  data() {
    return {
      userLastName: "", // 성
      userFirstName: "", // 이름
      userBirthDate: "", // 생년월일
      lmsID: "", // LMS ID(학번)
      lmsPassword: "", // LMS 비밀번호
    };
  },
  computed: {
    isValidDate() {
      return this.checkValidDate(this.userBirthDate);
    },
  },
  methods: {
    ...mapActions(["updateState"]),
    submitAll() {
      // Vuex에 사용자 정보 저장
      this.updateState({ key: "lastName", value: this.userLastName });
      this.updateState({ key: "firstName", value: this.userFirstName });
      this.updateState({ key: "birthDate", value: this.userBirthDate });
      this.updateState({ key: "lmsID", value: this.lmsID });
      this.updateState({ key: "lmsPassword", value: this.lmsPassword });
      // 메인 페이지로 이동
      this.$router.push("/");
    },
    resetFields() {
      this.userLastName = "";
      this.userFirstName = "";
      this.userBirthDate = "";
      this.lmsID = "";
      this.lmsPassword = "";
    },
    onInputHandler() {
      let value = this.userBirthDate.replace(/\D/g, ""); // 숫자만 남기기
      let length = value.length;

      if (length < 6) {
        this.userBirthDate = value;
      } else if (length < 8) {
        this.userBirthDate = value.slice(0, 4) + "-" + value.slice(4);
      } else {
        this.userBirthDate =
          value.slice(0, 4) + "-" + value.slice(4, 6) + "-" + value.slice(6);
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
  },
};
</script>

<style scoped>
.settings-page {
  font-family: Arial, sans-serif;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.name-section,
.date-section,
.lms-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.date-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}

.warning {
  color: red;
  font-size: 12px;
  margin-top: 5px;
}

.button-group {
  display: flex;
  gap: 10px;
  justify-content: center;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
}

button:hover {
  opacity: 0.8;
}

button:active {
  transform: scale(0.98);
}

.reset-button {
  background-color: #ff6b6b;
  color: white;
}

.reset-button:hover {
  background-color: #ff4c4c;
}
</style>
