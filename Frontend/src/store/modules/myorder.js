const state = {
    myorders: [],
};

const mutations = {
    SET_MY_ORDERS(state, myorders) {
        state.myorders = myorders;
    },
    UPDATE_MY_ORDER(state, updated) {
        const index = state.myorders.findIndex(
            (myorder) => myorder.log_id === updated.log_id
        )
        state.myorders[index].approved = updated.approved
    },
    UPDATE_ORDER_PDF_URL(state, log_id) {
        
        const index = state.myorders.findIndex(
            (myorder) => myorder.log_id === log_id.log_id
        )
        if (index !== -1) {
          state.myorders[index].pdfUrl = log_id.pdfUrl;
        }
        
    },
    UPDATE_ORDER_APPROVED(state, log_id) {
        const index = state.myorders.findIndex(
            (myorder) => myorder.log_id === log_id.log_id
        )
        if (index !== -1) {
          state.myorders[index].approved = log_id.approved;
        }
    },
};

const actions = {
    async fetchMyOrders({ commit }) {
        const token = localStorage.getItem("accessToken");
    if (token) {
      const fetchUrl = `http://127.0.0.1:5000/Api/logs`;
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
          commit("SET_MY_ORDERS", data);
        })
        .catch((error) => {
          console.error("There was an error fetching the my books!", error);
          alert(error.message || "Failed to fetch my books");
        });
    }
  },
  async updateMyOrder({ commit }, {log_id,approved}) {
    const token = localStorage.getItem("accessToken");
    if (token) {
      const Url = `http://127.0.0.1:5000/Api/logs/${log_id}`;
      const requestOptions = {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ approval: approved }), 
      };
      await fetch(Url, requestOptions)
        .then(async (response) => response.json())
        .then((data) => {
          commit("UPDATE_MY_ORDER", data);
        })
        .catch((error) => {
          console.error("There was an error approving the request!", error);
        });
    }
  },

};  

const getters = {
    myorders: (state) => state.myorders, 
};

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
}