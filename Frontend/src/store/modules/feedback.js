const state = {
  feedbacks: [],
  user: [],
  userfeedbacks: [],
};

const mutations = {
  setFeedbacks(state, feedbacks) {
    state.feedbacks = feedbacks;
  },
  async addFeedback(state, feedback) {
    feedback["Name"] = state.user["first_name"] + " " + state.user["last_name"];
    feedback["profile_photo"] = state.user["profile_photo"];
    feedback["Email"] = state.user["mail_id"];
    console.log("feedback", feedback);
    state.userfeedbacks.push(feedback);
  },
  updateFeedback(state, updatedFeedback) {
    const index = state.userfeedbacks.findIndex(
      (f) => f.user_id === updatedFeedback.user_id
    );
    state.userfeedbacks[index].feedback_rating =
      updatedFeedback.feedback_rating;
    state.userfeedbacks[index].feedback_text = updatedFeedback.feedback_text;
  },
  deleteFeedback(state, user_id) {
    state.userfeedbacks = state.userfeedbacks.filter(
      (f) => f.user_id !== user_id
    );
  },
  setuser(state, user) {
    state.user = user;
  },
  setuserfeedbacks(state, userfeedbacks) {
    state.userfeedbacks = userfeedbacks;
  },
};

const actions = {
  async fetchFeedbacks({ commit }, bookId) {
    const token = localStorage.getItem("accessToken");
    if (token) {
      const fetchUrl = `http://127.0.0.1:5000/Api/Book/${bookId}/Feedback`;
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
          commit("setFeedbacks", data);
        })
        .catch((error) => {
          console.error("There was an error fetching the feedbacks!", error);
          alert(error.message || "Failed to fetch feedbacks");
        });
    }
  },
  async addFeedback({ dispatch, commit }, feedback) {
    const token = localStorage.getItem("accessToken");
    
    if (token) {
      const feedbackUrl = `http://127.0.0.1:5000/Api/Feedback`;
      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(feedback),
      };

      await fetch(feedbackUrl, requestOptions)
        .then(async (response) => response.json())
        .then(async (data) => {
          await dispatch('getUser', data.user_id); 
          commit("addFeedback", data);
        })
        .catch((error) => {
          console.error("There was an error creating the new feedback!", error);
        });
    }
  },
  async editFeedback({ commit }, feedback) {
    const token = localStorage.getItem("accessToken");
    console.log(feedback," i am in PUT");
    if (token) {
      const feedbackUrl = `http://127.0.0.1:5000/Api/Book/${feedback.book_id}/Feedback`;
      const requestOptions = {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(feedback),
      };
      await fetch(feedbackUrl, requestOptions)
        .then(async (response) => response.json())
        .then((data) => {
          commit("updateFeedback", data);
        })
        .catch((error) => {
          console.error("There was an error editing the feedback!", error);
        });
    }
  },
  async deleteFeedback({ commit }, feedback) {
    const token = localStorage.getItem("accessToken");
    if (token) {
      const feedbackUrl = `http://127.0.0.1:5000/Api/Book/${feedback.book_id}/Feedback`;
      const requestOptions = {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      };
      await fetch(feedbackUrl, requestOptions)
        .then(commit("deleteFeedback", feedback.user_id))
        .catch((error) => {
          console.error("There was an error deleting the feedback!", error);
        });
    }
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

  async loadFeedbacksWithUserDetails({ dispatch, commit }, bookId) {
    await dispatch("fetchFeedbacks", bookId);
    const feedbacks = state.feedbacks;

    for (const feedback of feedbacks) {
      await dispatch(`getUser`, feedback.user_id);
      feedback.Name = state.user.first_name + " " + state.user.last_name;
      feedback.profile_photo = state.user.profile_photo;
      feedback.Email = state.user.mail_id;
    }

    commit("setuserfeedbacks", feedbacks);
  },
};

const getters = {
  feedbacks: (state) => state.userfeedbacks,
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
