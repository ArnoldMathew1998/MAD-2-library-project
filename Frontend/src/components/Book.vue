<template>
  <div>
    <h1>Books for Section: {{ sectionId }}</h1>
    <table class="table">
      <thead class="table-secondary">
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Book Name</th>
          <th scope="col">Author Name</th>
          <th scope="col">Date Issued</th>
          <th scope="col">Price</th>
          <th scope="col">View</th>
          <th v-if="isAdmin" scope="col">Edit</th>
          <th v-if="isAdmin" scope="col">Delete</th>
        </tr>
      </thead>
      <tbody v-if="books.length > 0">
        <tr v-for="(book, index) in books" :key="book.book_id" :class="{ 'table-secondary': index % 2 === 1 }">
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ book.book_name }}</td>
          <td>{{ book.author_name }}</td>
          <td>
            <div class="date-time">
              <span class="date">{{ formatDate(book.date_issued) }}</span>
            </div>
          </td>
          <td>{{ book.price }}₹</td>
          <td class="link-info link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover clickable" @click="viewBook(book.book_id)">Click</td>
          <td v-if="isAdmin" class="link-warning link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover clickable" @click="editBook(book, index)">Edit</td>
          <td v-if="isAdmin" class="link-danger link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover clickable" @click="confirmDeleteBook(book.book_id)">Delete</td>
        </tr>
      </tbody>
    </table>
    <div v-if="isAdmin" class="text-end mt-3">
      <button class="btn btn-primary" @click="showAddBookModal = true">+ Add New Book</button>
    </div>
    <div v-if="showAddBookModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeAddBook">&times;</span>
        <h2>Add New Book</h2>
        <form @submit.prevent="newBook.book_id ? updateBook() : addNewBook()">
          <div class="form-group">
            <label for="book_name">Book Name</label>
            <input type="text" id="book_name" v-model="newBook.book_name" required>
          </div>
          <div class="form-group">
            <label for="author_name">Author Name</label>
            <input type="text" id="author_name" v-model="newBook.author_name" required>
          </div>
          <div class="form-group">
            <label for="date_issued">Date Issued</label>
            <input type="date" id="date_issued" v-model="newBook.date_issued" required>
          </div>
          <div class="form-group">
            <label for="price">Price</label>
            <input type="number" id="price" v-model="newBook.price" required>
          </div>
          <div class="form-group">
            <label for="content">Content</label>
            <input type="text" id="content" v-model="newBook.content" required>
          </div>
          <div class="form-group">
            <label for="language">Language</label>
            <input type="text" id="language" v-model="newBook.language" required>
          </div>
          <div class="form-group">
            <label for="image">Upload Image</label>
            <input type="file" id="image" @change="handleImageUpload($event)">
          </div>
          <div class="form-group">
            <label for="pdf">Upload PDF</label>
            <input type="file" id="pdf" ref="pdf" accept=".pdf" @change="handlePDFUpload($event)">
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['section_id'],
  data() {
    return {
      books: [],
      sectionId: '',
      searchQuery: '',
      isAdmin: false,
      showAddBookModal: false,
      currentBookIndex: null,
      newBook: {
        book_id: '',
        book_name: '',
        author_name: '',
        date_issued: '',
        price: 0,
        content: '',
        language: '',
        image_path: '',
        pdf_path: ''
      },
      selectedImageFile: null,
      selectedPDFFile: null
    };
  },
  methods: {
    handleImageUpload(event) {
      this.selectedImageFile = event.target.files[0];
    },
    handlePDFUpload(event) {
      this.selectedPDFFile = event.target.files[0];
    },
    async uploadfile(file, type) {
      const formData = new FormData();
      formData.append('file', file);
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

        await fetch(uploadUrl, requestOptions)
        .then(async response => response.json())
        .then(data => {
          if (data.path) {
            console.log(data.path);
            if (type==='image') {
              this.newBook.image_path = data.path;
            }
            if (type==='pdf') {
              this.newBook.pdf_path = data.path;
            }
          } else {
            throw new Error('Image path not received from server');
          }
        })
        .catch(error => {
            console.error("There was an error uploading the image!", error);
            alert(error.message || 'Failed to upload image');
        });
      }
    },

    closeAddBook() {
      this.showAddBookModal = false;
      this.newBook = {
        book_id: '',
        book_name: '',
        author_name: '',
        date_issued: '',
        price: 0,
        content: '',
        language: '',
        image_path: '',
        pdf_path: ''
      };
      this.selectedImageFile = null;
      this.selectedPDFFile = null;
      this.currentBookIndex = null;
    },
    async fetchBooks() {
      const token = localStorage.getItem('accessToken');
      if (token) {
        const roleUrl = `http://127.0.0.1:5000/Api/Section/${this.sectionId}/Book`;
        const requestOptions = {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        };

        await fetch(roleUrl, requestOptions)
          .then(async response => {
            if (response.status === 404) {
              console.log("Resource not found");
              this.books = [];
            } else {
              const data = await response.json();
              this.books = data;
            }
          })
          .catch(error => {
            console.error("There was an error fetching the books!", error);
            alert(error);
          });
      }
    },
    async fetchUserRole() {
      const token = localStorage.getItem('accessToken');
      if (token) {
        const roleUrl = 'http://127.0.0.1:5000/Api/user/role';
        const requestOptions = {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        };

        await fetch(roleUrl, requestOptions)
          .then(async response => {
            const data = await response.json();
            this.isAdmin = data.role === 'admin';
          })
          .catch(error => {
            console.error("There was an error fetching the user role!", error);
            alert(error);
          });
      }
    },
    async addNewBook() {
        const token = localStorage.getItem('accessToken');
        if (token) {
          if (this.selectedImageFile) {
            await this.uploadfile(this.selectedImageFile, 'image');
          }
          if (this.selectedPDFFile) {
            await this.uploadfile(this.selectedPDFFile, 'pdf');
          }
          const bookUrl = `http://127.0.0.1:5000/Api/Section/${this.sectionId}/Book`;
          const requestOptions = {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(this.newBook)
          };
          await fetch(bookUrl, requestOptions)
            .then(async response => response.json())
            .then(data => {
              this.books.push(data);
              this.closeAddBook();
            })
            .catch(error => {
              console.error("There was an error creating the new book!", error);
              alert(error);
            });
        }
      },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
    viewBook(book_id) {
      this.$router.push({ name: 'Product', params: { book_id: book_id } });
    },
    async editBook(book, index) {
      this.newBook = { ...book };
      this.currentBookIndex = index;
      this.showAddBookModal = true;
    },
    async updateBook() {
        const token = localStorage.getItem('accessToken');
        if (token) {
          if (this.selectedImageFile) {
            await this.uploadfile(this.selectedImageFile, 'image');
          }
          if (this.selectedPDFFile) {
            await this.uploadfile(this.selectedPDFFile, 'pdf');
          }
          const bookUrl = `http://127.0.0.1:5000/Api/Book/${this.newBook.book_id}`;
          const requestOptions = {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(this.newBook)
          };
          await fetch(bookUrl, requestOptions)
            .then(response => response.json())
            .then(updatedBook => {
              this.books.splice(this.currentBookIndex, 1, updatedBook);
              this.closeAddBook();
            })
            .catch(error => {
              console.error("There was an error updating the book!", error);
              alert(error);
            });
        }
      },
    confirmDeleteBook(book_id) {
      if (confirm("Are you sure you want to delete this book?")) {
        this.deleteBook(book_id);
      }
    },
    async deleteBook(book_id) {
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
          .then(() => this.books = this.books.filter(book => book.book_id !== book_id))
          .catch(error => {
            console.error("There was an error deleting the book!", error);
            alert(error);
          });
      }
    }
  },
  async mounted() {
    this.sectionId = this.$route.params.section_id;
    await this.fetchBooks();
    await this.fetchUserRole();
  }
};
</script>

<style scoped>
.input-group>.form-control {
  width: 20rem;
}
.date-time {
  display: flex;
  flex-direction: column;
}
.date-time .time {
  font-size: 0.85em;
  color: gray;
}
.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0,0,0);
  background-color: rgba(0,0,0,0.4);
}
.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}
.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}
.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
.clickable {
  cursor: pointer;
}
</style>
