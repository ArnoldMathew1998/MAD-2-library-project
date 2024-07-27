const state = {
  cartItems: [],
  books: [],
  cartItemWithBookDetails: [],
};

const mutations = {
    setCartItems(state, cartItems) {
      state.cartItems = cartItems;
    },
    addCartItem(state, cartItem) {
      cartItem["name"] = state.books.book_name;
      cartItem["book_id"] = state.books.book_id;
      cartItem["price"] = state.books.price;
      cartItem["content"] = state.books.content;
      
      state.cartItemWithBookDetails.push(cartItem);
    },
    removeCartItem(state, book_id) {
      
      state.cartItemWithBookDetails = state.cartItemWithBookDetails.filter(
        (f) => f.book_id !== book_id
      );
    },
    SET_BOOKS(state, books) {
      state.books = books;
    },
    cartItemWithBookDetails(state, cartItems) {
      state.cartItemWithBookDetails = cartItems;
    },

  };

const actions = {
  async fetchCartItems({ commit }) {
    const token = localStorage.getItem("accessToken");
    if (token) {
      const fetchUrl = `http://127.0.0.1:5000/Api/cart`;
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
          commit("setCartItems", data);
        })
        .catch((error) => {
          console.error("There was an error fetching the cart!", error);
          alert(error.message || "Failed to fetch cart");
        });
    }
  },
  async addCartItem({ dispatch, commit }, book_id) {
    const token = localStorage.getItem("accessToken");
    
    if (token) {
      const CartUrl = `http://127.0.0.1:5000/Api/cart`;
      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ "book_id": book_id}),
      };

      await fetch(CartUrl, requestOptions)
        .then(async (response) => response.json())
        .then(async (data) => {
          await dispatch("fetchBooks", book_id);
          await commit("addCartItem", data);
        })
        .catch((error) => {
          console.error("There was an error creating the new feedback!", error);
        });
    }
    
  },
  async removeCartItem({ commit }, book_id) {
    const token = localStorage.getItem("accessToken");
    if (token) {
      const cartUrl = `http://127.0.0.1:5000/Api/cart/${book_id}`;
      const requestOptions = {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      };

      await fetch(cartUrl, requestOptions)
        .then(commit("removeCartItem", book_id))
        .catch((error) => {
          console.error("There was an error deleting the cart!", error);
        });
    }
  },

  async loadCartWithBookDetails({ dispatch, commit }) {
    await dispatch("fetchCartItems");
    const cartItems = state.cartItems;

    for (const cartItem of cartItems) {
      await dispatch(`fetchBooks`, cartItem.book_id);
      cartItem.name = state.books.book_name;
      cartItem.book_id = state.books.book_id;
      cartItem.price = state.books.price;
      cartItem.content = state.books.content;
    }
    commit("cartItemWithBookDetails", cartItems);
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
    cartItems: (state) => state.cartItemWithBookDetails,
  };

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
