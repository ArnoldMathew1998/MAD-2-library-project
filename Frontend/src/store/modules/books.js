// src/store/modules/books.js
const state = {
  books: [],
};

const mutations = {
  SET_BOOKS(state, books) {
    state.books = books;
  },
  ADD_BOOK(state, book) {
    state.books.push(book);
  },
  UPDATE_BOOK(state, updatedBook) {
    const index = state.books.findIndex(book => book.book_id === updatedBook.book_id);
    if (index !== -1) {
      state.books.splice(index, 1, updatedBook);
    }
  },
  DELETE_BOOK(state, book_id) {
    state.books = state.books.filter(book => book.book_id !== book_id);
  },
  
};

const actions = {
  async fetchBooks({ commit }, sectionId = null) {
    const token = localStorage.getItem("accessToken");
    if (token) {
      const fetchUrl = sectionId
        ? `http://127.0.0.1:5000/Api/Section/${sectionId}/Book`
        : `http://127.0.0.1:5000/Api/Book`;

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

  async uploadfile(_, file) {
    const formData = new FormData();
    formData.append('file', file);
    console.log(formData.file);
    const token = localStorage.getItem('accessToken');
    if (token) {
      const uploadUrl = 'http://127.0.0.1:5000/Api/Book/upload';
      const requestOptions = {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      };

      // Send the file to the server
      return await fetch(uploadUrl, requestOptions)
        .then(async response => response.json())
        .then(data => {
          if (data.path) {
            console.log(data.path);
            return data.path;
          } else {
            throw new Error('File path not received from server');
          }
        })
        .catch(error => {
          console.error("There was an error uploading the file!", error);
          alert(error.message || "Failed to upload file");
          throw error;
        });
    }
  },

  async addNewBook({ commit, dispatch }, { sectionId, newBook, selectedImageFile, selectedPDFFile }) {
    const token = localStorage.getItem('accessToken');
    if (token) {
      if (selectedImageFile) {
        const imagePath = await dispatch('uploadfile', selectedImageFile);
        newBook.image_path = imagePath;
      }
      if (selectedPDFFile) {
        const pdfPath = await dispatch('uploadfile',selectedPDFFile);
        newBook.pdf_path = pdfPath;
      }
      const bookUrl = `http://127.0.0.1:5000/Api/Section/${sectionId}/Book`;
      const requestOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(newBook)
      };
      await fetch(bookUrl, requestOptions)
        .then(async response => response.json())
        .then(data => {
          commit('ADD_BOOK', data);
        })
        .catch(error => {
          console.error("There was an error creating the new book!", error);
          alert(error.message || "Failed to create new book");
        });
    }
  },

  async updateBook({commit, dispatch }, { newBook, selectedImageFile, selectedPDFFile }) {
    const token = localStorage.getItem('accessToken');
    if (token) {
      if (selectedImageFile) {
        const imagePath =await dispatch('uploadfile',selectedImageFile);
        newBook.image_path = imagePath;
      }
      if (selectedPDFFile) {
        const pdfPath = await dispatch('uploadfile',selectedPDFFile);
        newBook.pdf_path = pdfPath;
      }
      if (!newBook || !newBook.book_id) {
        throw new Error('Invalid book data');
      }
     console.log(newBook);
      const bookUrl = `http://127.0.0.1:5000/Api/Book/${newBook.book_id}`;
      const requestOptions = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(newBook)
      };
      await fetch(bookUrl, requestOptions)
        .then(async response => response.json())
        .then(updatedBook => {
          commit('UPDATE_BOOK', updatedBook);
        })
        .catch(error => {
          console.error("There was an error updating the book!", error);
          alert(error.message || "Failed to update book");
        });
    }
  },


  async deleteBook({ commit }, book_id) {
    const token = localStorage.getItem('accessToken');
    if (token) {
      const bookUrl = `http://127.0.0.1:5000/Api/Book/${book_id}`;
      const requestOptions = {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      };

      await fetch(bookUrl, requestOptions)
        .then(response => {
          if (response.ok) {
            commit('DELETE_BOOK', book_id);
          } else {
            throw new Error('Failed to delete book');
          }
        })
        .catch(error => {
          console.error("There was an error deleting the book!", error);
          alert(error.message || "Failed to delete book");
        });
    }
  }
};

const getters = {
  allBooks: (state) => state.books,
  books: (state) => state.books,
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
