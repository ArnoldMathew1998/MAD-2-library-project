// src/store/modules/books.js
const state = {
  books: [],
};

const mutations = {
  setBooks(state, books) {
    state.books = books;
  },
};

const actions = {
  async fetchBooks({ commit }) {
    const token = localStorage.getItem("accessToken");
    if (token) {
      const fetchUrl = `http://127.0.0.1:5000/Api/Book`;
      const requestOptions = {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };

      await fetch(fetchUrl, requestOptions)
        .then(async (response) => {
          if (!response.ok) {
            return;
          }
          const data = await response.json();
          commit("setBooks", data);
        })
        .catch((error) => {
          console.error("There was an error fetching the books!", error);
          alert(error.message || "Failed to fetch books");
        });
    }
  },
};

const getters = {
  allBooks: (state) => state.books,
  chunkedBooks: (state) => {
    const chunkSize = 6;
    let chunks = [];
    for (let i = 0; i < state.books.length; i += chunkSize) {
      chunks.push(state.books.slice(i, i + chunkSize));
    }
    return chunks;
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
