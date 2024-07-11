// src/store/modules/user.js
const state = {
  username: "",
  token: null,
  isAdmin: false,
};

const mutations = {
  setUser(state, user) {
    state.username = user.username;
    state.token = user.token;
    if (user.role == "admin") {
      state.isAdmin = true;
    }
  },
};

const actions = {
  async signIn({ commit }, formData) {
    const loginUrl = "http://127.0.0.1:5000/login";
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    };

    await fetch(loginUrl, requestOptions)
      .then(async (response) => response.json())
      .then((data) => {
        const user = {
          username: formData.username,
          token: data.access_token,
          role: data.role,
        };

        commit("setUser", user);
        localStorage.setItem("accessToken", user.token);
        localStorage.setItem("isAdmin", user.role);
      })
      .catch((error) => {
        console.error("There was an error!", error);
        alert(error);
      });
  },

  async SignUp({ commit }, userData) {
    const loginUrl = "http://127.0.0.1:5000/Api/user";
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    };

    fetch(loginUrl, requestOptions)
      .then(async (response) => {
        const data = await response.json();
        return data;
      })
      .then((data) => {
        const user = {
          username: this.userData.mail_id,
          token: data.access_token,
          role: "user",
        };
        commit("setUser", user);
        localStorage.setItem("accessToken", user.token);
        localStorage.setItem("isAdmin", user.role);
      })
      .catch((error) => {
        console.error("There was an error!", error);
        alert(error);
      });
  },
};

const getters = {
  isAuthenticated: (state) => !!state.token,
  getUsername: (state) => state.username,
  isAdmin: (state) => state.isAdmin,
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
