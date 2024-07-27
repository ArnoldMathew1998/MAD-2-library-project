const state = {
  userLog: [],
};

const mutations = {
  setUserLog(state, userLog) {
    state.userLog = userLog;
  },

  ADD_USERLOG(state, userLog) {
    state.userLog.push(userLog);
  },
};

const actions = {
  async addLog({ commit }, {book_id, borrow_duration}) {
    const token = localStorage.getItem("accessToken");
    const log = {"book_id": book_id,"borrow_duration": borrow_duration};
    if (token) {
      const Url = `http://127.0.0.1:5000/Api/logs`;
      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(log),
      };
      await fetch(Url, requestOptions)
        .then(async (response) => response.json())
        .then((data) => {
          commit("ADD_USERLOG", data);
        })
        .catch((error) => {
          console.error("There was an error creating the new book!", error);
          alert(error.message || "Failed to create new book");
        });
    }
  },
};

const getters = {
  userLog: (state) => state.userLog,
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
