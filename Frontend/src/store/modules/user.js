// src/store/modules/user.js
const state = {
  username: "",
  name: "",
  user_id: "",
  profile_photo:"",
  token: null,
  isAdmin: false,
};

const mutations = {
  setUser(state, user) {
    state.username = user.username;
    state.name = user.name;
    state.user_id = user.user_id;
    state.token = user.token;
    state.profile_photo = user.profile_photo;
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
          username: data.username,
          token: data.access_token,
          role: data.role,
          name: data.name,
          user_id: data.user_id,
          profile_photo:data.profile_photo
        };

        commit("setUser", user);
        localStorage.setItem("accessToken", user.token);
        localStorage.setItem("isAdmin", user.role);
        localStorage.setItem("user_id", user.user_id);
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
          username: data.username,
          token: data.access_token,
          role: data.role,
          name: data.name,
          user_id: data.user_id,
          profile_photo:data.profile_photo
        };
        commit("setUser", user);
        localStorage.setItem("accessToken", user.token);
        localStorage.setItem("isAdmin", user.role);
        localStorage.setItem("user_id", user.user_id);
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
  isAdmin: (state) => state.isAdmin=localStorage.getItem("isAdmin")==="admin",
  getName: (state) => state.name,
  getUserId: (state) => state.user_id=localStorage.getItem("user_id"),
  getProfilePhoto: (state) => state.profile_photo
 
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
