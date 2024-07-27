const state = {
  username: "",
  name: "",
  user_id: "",
  profile_photo:"",
  token: null,
  isAdmin: false,
  user: [],
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
  setuser(state, user) {
    state.user = user;
  },
  clearUserState(state) {
    state.username = "";
    state.name = "";
    state.user_id = "";
    state.profile_photo = "";
    state.token = null;
    state.isAdmin = false;
    state.user = [];
    console.log("logging out", state.isAdmin);
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
          profile_photo: data.profile_photo,
        };        
        localStorage.setItem("accessToken", user.token);
        if (user.role == "admin") {
          localStorage.setItem("isAdmin", "true");
        }
        localStorage.setItem("user_id", user.user_id);
        commit("setUser", user);
      })
      .catch(() => {
        console.error("There was an error!");
        alert("Invalid credentials Failed to login");
      });
  },

  async SignUp({ commit }, userData) {
    const loginUrl = "http://127.0.0.1:5000/Api/user";
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    };

    await fetch(loginUrl, requestOptions)
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
          profile_photo: data.profile_photo,
        };        
        localStorage.setItem("accessToken", user.token);
        if (user.role == "admin") {
          localStorage.setItem("isAdmin", "true");
        }
        localStorage.setItem("user_id", user.user_id);
        commit("setUser", user);
      })
      .catch((error) => {
        console.error("There was an error!", error);
        alert(error);
      });
  },

  async getUser({ commit }, userId) {
    const token = localStorage.getItem("accessToken");
    if (token) {
      const fetchUrl = `http://127.0.0.1:5000/Api/user/${userId}`;
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      };
      await fetch(fetchUrl, requestOptions)
        .then(async (response) => {
          const data = await response.json();
          commit("setuser", data);
        })
        .catch((error) => {
          console.error("There was an error!", error);
          return;
        });
    }
  },

  async updateUser(_, updatedUser) {
    const token = localStorage.getItem("accessToken");
    if (token) {
      const user_id=localStorage.getItem("user_id");
      const updateUser = `http://127.0.0.1:5000/Api/user/${user_id}`;
      const requestOptions = {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(updatedUser),
      };
      await fetch(updateUser, requestOptions)
        .then(async (response) => response.json())
        .then((data) => {
          console.log(data.message);
        })
        .catch((error) => {
          console.error("There was an error updating the user!", error);
        });
    }
  },

  async deleteUser(_, password) {
    const token = localStorage.getItem("accessToken");
    if (token) {
      const user_id = localStorage.getItem("user_id");
      const deleteUserUrl = `http://127.0.0.1:5000/Api/user/${user_id}`;
      const requestOptions = {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ currentPassword: password }),
      };
      
      await fetch(deleteUserUrl, requestOptions)
        .then(async (response) => response.json())
        .then((data) => {
          console.log(data.message);
        })
        .catch((error) => {
          console.error("There was an error deleting the user!", error);
          alert(error.message || "Failed to delete user");
        });
    }
  },

  logout({ commit }) {
    const token = localStorage.getItem("accessToken");
    if (token) {
      const logoutUrl = "http://127.0.0.1:5000/logout";
      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      };
      fetch(logoutUrl, requestOptions)
        .then(async (response) => {
          const data = await response.json();
          console.log(data.message);
          localStorage.removeItem("accessToken");
  localStorage.removeItem("user_id");
  localStorage.removeItem("isAdmin");
    commit("clearUserState");
        })
        .catch((error) => {
          console.error("There was an error logging out!", error);
          alert(error.message || "Failed to logout");
        });
    }
    
  },
};

const getters = {
  isAuthenticated: (state) => !!state.token,
  getUsername: (state) => state.username,
  isAdmin: (state) => state.isAdmin,
  getName: (state) => state.name,
  getUserId: (state) => state.user_id ,
  getProfilePhoto: (state) => state.profile_photo,
  user: (state) => state.user,
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
