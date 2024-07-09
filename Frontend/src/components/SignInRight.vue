<template>
  <div class="sign-in1">
    <div class="button-parent">
      <RouterLink to="/">
        <div class="button">
          <i class="bi bi-arrow-left-circle" style="font-size: 1.2em; color: cornflowerblue; position: relative; width: 24px; height: 24px;"></i>
          <div class="back" style="font-size: 1.3rem; color: black;">Back</div>
        </div>
      </RouterLink>

      <div class="have-an-account-login-wrapper" id="frameContainer">
        <div class="have-an-account-login">
          <div class="already-have-an-container">
            <span class="dont-have-an">Don’t have an account?</span>
            <span class="span"></span>
            <RouterLink to="/Registration" class="link-secondary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">Sign up</RouterLink>
          </div>
        </div>
      </div>
    </div>

    <div class="sign-in-parent">
      <div class="sign-in2">Sign in</div>
      <div class="frame-parent">
        <div class="text-field-wrapper">
          <div class="text-field">
            <div class="label-parent">
              <div class="label">User name or email address</div>
            </div>
            <div class="input-group mb-3 text-field1">
              <input v-model="formData.username" type="text" class="form-control">
            </div>
          </div>
        </div>
        
        <div class="text-field-wrapper">
          <div class="text-field">
            <div class="label-parent">
              <div class="label">Your password</div>
              <div class="password-hide-see1">
                <i v-if="hide" class="bi bi-eye-slash icon"></i>
                <i v-else class="bi bi-eye icon"></i>
                <div @click="toggleHide" class="hide" style="cursor: pointer;">Hide</div>
              </div>
            </div>
            <div class="input-group mb-3 text-field1">
              <input :type="inputType" v-model="formData.password" class="form-control">
            </div>
          </div>
        </div>

        <div class="button-group">
          <button type="button" class="btn btn-dark btn-lg" @click="signIn">Sign in</button>
        </div>

        <div class="have-an-account-login1">
          <div class="already-have-an-container1" id="alreadyHaveAn">
            <span class="dont-have-an">Don’t have an account?</span>
            <span class="span"></span>
            <RouterLink to="/Registration" class="link-secondary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">Sign up</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      hide: true, 
      formData: {
        username: '',
        password: ''
      },
    };
  },
  methods: {
    // Method to toggle the hide property
    toggleHide() {
      this.hide = !this.hide;
    },
    signIn() {
      console.log(this.formData);
      const loginUrl = 'http://127.0.0.1:5000/login';
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.formData)
      };
      
      fetch(loginUrl, requestOptions).then(async response => {
        const data=await response.json();
        console.log(data);
        if (!response.ok) {
          const error=data.msg;
          return Promise.reject(error);
        }
        return data
      }).then(data => {
          const accessToken = data.access_token;
          localStorage.setItem('accessToken', accessToken);
          this.$router.push('/LoginHome');
      }).catch(error => {
        console.error("There was an error!", error);
        alert(error);
      })
    }
  },
  computed: {
    inputType() {
      return this.hide ? "password" : "text";
    },
  },
};
</script>

<style scoped>

.read-with-us {
  position: relative;
  line-height: 64px;
  font-weight: 600;
}
.reading-a-book {
  width: 482px;
  position: relative;
  font-size: 24px;
  text-align: left;
  display: flex;
  align-items: center;
}
.headline-and-subhead,
.image {
  align-self: stretch;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
}
.headline-and-subhead {
  gap: 16px;
}
.image {
  background: linear-gradient(
    180deg,
    #edb294,
    #edb294 22%,
    #edb294 30%,
    #b2cbcf
  );
  overflow: hidden;
  padding: 400px 138px;
}

.back {
  position: relative;
  font-weight: 500;
  backdrop-filter: blur(4px);
}
.button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 9px;
  text-decoration: none;
}
.dont-have-an {
  color: var(--color-darkslategray);
}
.span {
  color: var(--color-dimgray-100);
}

.already-have-an-container {
  position: relative;
}
.have-an-account-login {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
  padding: var(--padding-11xs);
}
.button-parent,
.have-an-account-login-wrapper {
  display: flex;
  align-items: flex-start;
  justify-content: center;
}
.have-an-account-login-wrapper {
  flex-direction: column;
  cursor: pointer;
  color: var(--color-gray);
  font-family: var(--font-poppins);
}
.button-parent {
  flex-direction: row;
  gap: 310px;
}
.sign-in2 {
  position: relative;
  font-weight: 500;
}
.icon,
.label {
  position: absolute;
}
.label {
  top: 0;
  left: 0;
}
.icon {
  top: 3px;
  right: 49px;
  width: 24px;
  height: 24px;
  overflow: hidden;
}

.label-parent {
  align-self: stretch;
  position: relative;
  height: 27px;
}
.inputs-child {
  width: 1px;
  position: relative;
  background-color: var(--color-gray);
  height: 24px;
  display: none;
}
.icons,
.inputs {
  position: absolute;
  display: none;
}
.inputs {
  top: 15px;
  left: 24px;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
}
.icons {
  top: 40px;
  right: 24px;
  width: 24px;
  height: 24px;
  overflow: hidden;
}
.text-field1 {
  align-self: stretch;
  position: relative;
  border-radius: var(--br-xs);
  border: 1px solid var(--color-dimgray-300);
  box-sizing: border-box;
  height: 56px;
  overflow: hidden;
  flex-shrink: 0;
  color: var(--color-gray);
}
.error-message {
  width: 101px;
  position: relative;
  font-size: var(--font-size-sm);
  color: var(--color-crimson);
  display: none;
}
.text-field {
  width: 568px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: var(--gap-9xs);
}
.text-field-wrapper {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.password-hide-see1 {
  position: absolute;
  top: 0;
  right: 8.9px;
  width: 73px;
  height: 27px;
  text-align: right;
  font-size: var(--font-size-lg);
  color: var(--color-dimgray-200);
}
.icons2,
.inputs-item {
  position: relative;
  height: 24px;
}
.inputs-item {
  width: 1px;
  background-color: var(--color-gray);
}
.icons2 {
  width: 24px;
  overflow: hidden;
  flex-shrink: 0;
  display: none;
}
.icons-parent {
  position: absolute;
  top: calc(50% - 15.5px);
  left: calc(50% - 33.5px);
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: var(--gap-5xs);
}
.button1 {
  width: 304px;
  position: relative;
  border-radius: 32px;
  background-color: var(--color-gray);
  height: 64px;
  overflow: hidden;
  flex-shrink: 0;
  opacity: 0.25;
}
.already-have-an-container1 {
  position: relative;
  cursor: pointer;
}
.have-an-account-login1 {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
  padding: var(--padding-11xs);
  text-align: left;
  font-size: var(--font-size-base);
  color: var(--color-gray);
}
.button-group,
.frame-parent {
  align-self: stretch;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-end;
}
.button-group {
  gap: var(--gap-5xs);
  text-align: center;
  font-size: 20px;
  color: var(--color-white);
}
.frame-parent {
  gap: 18px;
  font-size: var(--font-size-base);
  color: var(--color-dimgray-100);
}
.sign-in,
.sign-in-parent,
.sign-in1 {
  display: flex;
  justify-content: flex-start;
}
.sign-in-parent {
  height: 406px;
  flex-direction: column;
  align-items: flex-start;
  gap: 48px;
  font-size: 32px;
  color: var(--color-darkslategray);
  font-family: var(--font-poppins);
}
.sign-in,
.sign-in1 {
  height: 1024px;
  overflow: hidden;
}
.sign-in1 {
  width: 682px;
  flex-shrink: 0;
  flex-direction: column;
  align-items: center;
  padding: 48px 10px;
  box-sizing: border-box;
  gap: 103px;
  text-align: left;
  font-size: var(--font-size-base);
  font-family: var(--font-gilroy);
}
.sign-in {
  width: 100%;
  position: relative;
  background-color: var(--color-white);
  flex-direction: row;
  align-items: flex-start;
  text-align: center;
  font-size: 56px;
  color: var(--color-black);
  font-family: var(--font-poppins);
}

</style>