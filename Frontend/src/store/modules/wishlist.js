const state = {
  wishItems: [],
  books: [],
  wishItemWithBookDetails: [],
};

const mutations = {
    setwishItems(state, wishItems) {
      state.wishItems = wishItems;
    },
    addwishItem(state, wishItem) {
      wishItem["name"] = state.books.book_name;
      wishItem["book_id"] = state.books.book_id;
      wishItem["price"] = state.books.price;
      wishItem["content"] = state.books.content;
      
      state.wishItemWithBookDetails.push(wishItem);
    },
    removewishItem(state, book_id) {
      state.wishItemWithBookDetails = state.wishItemWithBookDetails.filter(
        (f) => f.book_id !== book_id
      );
    },
    SET_BOOKS(state, books) {
      state.books = books;
    },
    wishItemWithBookDetails(state, wishItems) {
      state.wishItemWithBookDetails = wishItems;
    },

  };

const actions = {
  async fetchwishItems({ commit }) {
    const token = localStorage.getItem("accessToken");
    if (token) {
      const fetchUrl = `http://127.0.0.1:5000/Api/wishlist`;
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
          commit("setwishItems", data);
        })
        .catch((error) => {
          console.error("There was an error fetching the wish!", error);
          alert(error.message || "Failed to fetch wish");
        });
    }
  },
  async addwishItem({ dispatch, commit }, book_id) {
    const token = localStorage.getItem("accessToken");
    
    if (token) {
      const wishUrl = `http://127.0.0.1:5000/Api/wishlist`;
      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ "book_id": book_id}),
      };

      await fetch(wishUrl, requestOptions)
        .then(async (response) => response.json())
        .then(async (data) => {
          await dispatch("fetchBooks", book_id);
          await commit("addwishItem", data);
        })
        .catch((error) => {
          console.error("There was an error creating the new feedback!", error);
        });
    }
    
  },
  async removewishItem({ commit }, book_id) {
    const token = localStorage.getItem("accessToken");
    if (token) {
      const wishUrl = `http://127.0.0.1:5000/Api/wishlist/${book_id}`;
      const requestOptions = {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      };
      await fetch(wishUrl, requestOptions)
        .then(commit("removewishItem", book_id))
        .catch((error) => {
          console.error("There was an error deleting the wish!", error);
        });
    }
  },

  async loadwishWithBookDetails({ dispatch, commit }) {
    await dispatch("fetchwishItems");
    const wishItems = state.wishItems;

    for (const wishItem of wishItems) {
      await dispatch(`fetchBooks`, wishItem.book_id);
      wishItem.name = state.books.book_name;
      wishItem.book_id = state.books.book_id;
      wishItem.price = state.books.price;
      wishItem.content = state.books.content;
    }
    commit("wishItemWithBookDetails", wishItems);
  },

  async fetchBooks({ commit }, book_id) {
    const token = localStorage.getItem("accessToken");
    if (token) {
      const fetchUrl = `http://127.0.0.1:5000/Api/Book/${book_id}`;
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      };

      await fetch(fetchUrl, requestOptions)
        .then(async (response) => {
          if (!response.ok) {
            throw new Error("Failed to fetch books");
          }
          const data = await response.json();
          commit("SET_BOOKS", data);
        })
        .catch((error) => {
          console.error("There was an error fetching the books!", error);
          alert(error.message || "Failed to fetch books");
        });
    }
  },
};

const getters = {
    wishItems: (state) => state.wishItemWithBookDetails,
  };

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
