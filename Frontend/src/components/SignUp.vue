<template>
  <div class="registration">
    <div class="create-an-account">
      <div class="create-an-account1">
        <div class="frame-parent">
          <div class="frame-wrapper">
            <div class="create-an-account-parent">
              <div class="sign-up">Create an account</div>
              <div class="have-an-account-login">
                <div class="already-have-an-container" id="alreadyHaveAn">
                  <span class="already-have-an">Already have an account?</span>
                  <span class="span"> </span>
                  <RouterLink
                    class="link-secondary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover"
                    to="/SignIn"
                  >
                    Sign in</RouterLink
                  >
                </div>
              </div>
            </div>
          </div>
          <div class="name-parent">
            <div class="name">
              <div class="text-field">
                <div class="label-parent">
                  <div class="label">First name</div>
                </div>
                <div class="input-group mb-3 text-field1">
                  <input type="text" class="form-control" v-model="firstName" />
                </div>
              </div>
              <div class="text-field">
                <div class="label-parent">
                  <div class="label">Last name</div>
                </div>
                <div class="input-group mb-3 text-field1">
                  <input type="text" class="form-control" v-model="lastName" />
                </div>
              </div>
            </div>
            <div class="email">
              <div class="label-parent">
                <div class="label">Email address</div>
              </div>
              <div class="input-group mb-3 text-field1">
                <input type="email" class="form-control" v-model="email" />
              </div>
            </div>
            <div class="password-and-instructions">
              <div class="name">
                <div class="text-field">
                  <div class="label-parent">
                    <div class="label">Password</div>
                  </div>
                  <div class="input-group mb-3 text-field1">
                    <input
                      :type="inputType"
                      class="form-control"
                      v-model="inputValue"
                    />
                  </div>
                </div>
                <div class="text-field">
                  <div class="label-parent">
                    <div class="label">Confirm your password</div>
                  </div>
                  <div class="input-group mb-3 text-field1">
                    <input
                      :type="inputType"
                      class="form-control"
                      v-model="confirmPassword"
                      :class="confirmPasswordClass"
                    />
                  </div>
                </div>
              </div>
              <div :class="passwordFeedbackClass">
                Use 8 or more characters with a mix of letters, numbers &
                symbols
              </div>
              <div class="form-check">
                <input
                  class="form-check-input"
                  type="checkbox"
                  value=""
                  id="flexCheckDefault"
                  @click="toggleHide"
                />
                <label class="form-check-label" for="flexCheckDefault">
                  Show password
                </label>
              </div>
            </div>
          </div>
          <button type="button" class="btn btn-dark btn-lg" @click="register">
            Create an account
          </button>
        </div>
      </div>
      <RouterLink to="/">
        <div class="button1">
          <i
            class="bi bi-arrow-left-circle"
            style="
              font-size: 1.2em;
              color: cornflowerblue;
              position: relative;
              width: 24px;
              height: 24px;
            "
          ></i>
          <div class="back" style="font-size: 1.3rem">Back</div>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<script>
/* import { mapActions } from "vuex"; */
export default {
  data() {
    return {
      hide: true,
      inputValue: "",
      confirmPassword: "",
      firstName: "",
      lastName: "",
      email: "",
    };
  },
  computed: {
    inputType() {
      return this.hide ? "password" : "text";
    },
    passwordFeedbackClass() {
      return this.isPasswordValid ? "valid-password" : "invalid-password";
    },
    isPasswordValid() {
      const password = this.inputValue;
      const hasLetter = /[a-zA-Z]/.test(password);
      const hasNumber = /\d/.test(password);
      const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
      const isLongEnough = password.length >= 8;
      return hasLetter && hasNumber && hasSpecialChar && isLongEnough;
    },
    confirmPasswordClass() {
      if (this.confirmPassword === "") return "";
      return this.confirmPassword === this.inputValue
        ? "valid-input"
        : "invalid-input";
    },
  },
  methods: {
    /* ...mapActions("user", ["signIn"]), // Map actions from the user module */
    toggleHide() {
      this.hide = !this.hide;
    },
    async register() {
      if (this.isPasswordValid && this.confirmPassword === this.inputValue) {
        const userData = {
          first_name: this.firstName,
          last_name: this.lastName,
          mail_id: this.email,
          password: this.inputValue,
        };
        await this.$store.dispatch("user/signUp", userData);
        this.$router.push('/Home');
      }
      else {
        alert(
          "Please ensure the password is valid and matches the confirm password."
        );
        
      }
    },
  },
};
</script>

<style scoped>
.invalid-password {
  color: red;
}

.valid-password {
  color: green;
}

.invalid-input {
  border-color: red;
}

.valid-input {
  border-color: green;
}

.already-have-an {
  color: var(--color-darkslategray);
}

.span {
  color: var(--color-dimgray-100);
}

.log-in {
  text-decoration: underline;
  white-space: pre-wrap;
}

.already-have-an-container {
  position: relative;
  cursor: pointer;
}

.have-an-account-login {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
  padding: 2px;
  font-size: var(--font-size-base);
  color: var(--color-gray-100);
}

.create-an-account-parent,
.frame-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.create-an-account-parent {
  justify-content: center;
  gap: var(--gap-11xs);
}

.frame-wrapper {
  justify-content: flex-start;
}

.label-parent {
  align-self: stretch;
  height: 27px;
}

.div,
.label-parent {
  position: relative;
}

.text-field1 {
  align-self: stretch;
  position: relative;
  border-radius: var(--br-xs);
  border: 1px solid var(--color-dimgray-400);
  box-sizing: border-box;
  height: 56px;
  overflow: hidden;
  flex-shrink: 0;
  color: var(--color-dimgray-300);
}

.error-message {
  width: 101px;
  position: relative;
  font-size: var(--font-size-sm);
  color: var(--color-crimson);
  display: none;
}

.email,
.name,
.text-field {
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
}

.text-field {
  width: 259px;
  flex-direction: column;
  gap: var(--gap-9xs);
}

.email,
.name {
  flex-direction: row;
  gap: var(--gap-base);
}

.email {
  width: 534px;
  flex-direction: column;
  gap: var(--gap-9xs);
}

.name-parent {
  gap: 24px;
  font-size: var(--font-size-base);
  color: var(--color-dimgray-100);
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  flex-direction: column;
}

.sign-up {
  position: relative;
  font-weight: 500;
}

.button {
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  border-radius: 32px;
  background-color: var(--color-gray-100);
  overflow: hidden;
  opacity: 0.25;
}

.frame-parent {
  position: absolute;
  top: 56px;
  left: 56px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 40px;
}

.create-an-account1 {
  width: 1017px;
  position: relative;
  border-radius: 24px;
  background-color: var(--color-white);
  border: 1px solid rgba(102, 102, 102, 0.5);
  box-sizing: border-box;
  height: 100vh;
  overflow: hidden;
  flex-shrink: 0;
  z-index: 0;
}

.back {
  position: relative;
  font-weight: 500;
  backdrop-filter: blur(4px);
}

.button1,
.create-an-account {
  position: absolute;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.button1 {
  margin: 0 !important;
  top: calc(50% - 375.5px);
  right: 936px;
  justify-content: flex-start;
  gap: var(--gap-11xs);
  z-index: 1;
  font-size: var(--font-size-base);
  color: #000;
  font-family: var(--font-gilroy);
}

.create-an-account {
  top: calc(50% - 393.5px);
  left: calc(50% - 509px);
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.registration {
  width: 100%;
  position: relative;
  background-color: #fbfbfb;
  height: 971px;
  overflow: hidden;
  text-align: left;
  font-size: 32px;
  color: var(--color-darkslategray);
  font-family: var(--font-poppins);
}
</style>
