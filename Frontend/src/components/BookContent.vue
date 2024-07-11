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
        <tr
          v-for="(book, index) in books"
          :key="book.book_id"
          :class="{ 'table-secondary': index % 2 === 1 }"
        >
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ book.book_name }}</td>
          <td>{{ book.author_name }}</td>
          <td>
            <div class="date-time">
              <span class="date">{{ formatDate(book.date_issued) }}</span>
            </div>
          </td>
          <td>{{ book.price }}₹</td>
          <td
            class="link-info link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover clickable"
            @click="viewBook(book.book_id)"
          >
            Click
          </td>
          <td
            v-if="isAdmin"
            class="link-warning link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover clickable"
            @click="editBook(book, index)"
          >
            Edit
          </td>
          <td
            v-if="isAdmin"
            class="link-danger link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover clickable"
            @click="confirmDeleteBook(book.book_id)"
          >
            Delete
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="isAdmin" class="text-end mt-3">
      <button class="btn btn-primary" @click="showAddBookModal = true">
        + Add New Book
      </button>
    </div>
    <div v-if="showAddBookModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeAddBook">&times;</span>
        <h2>Add New Book</h2>
        <form @submit.prevent="newBook.book_id ? updateBook() : addNewBook()">
          <div class="form-group">
            <label for="book_name">Book Name</label>
            <input
              type="text"
              id="book_name"
              v-model="newBook.book_name"
              required
            />
          </div>
          <div class="form-group">
            <label for="author_name">Author Name</label>
            <input
              type="text"
              id="author_name"
              v-model="newBook.author_name"
              required
            />
          </div>
          <div class="form-group">
            <label for="date_issued">Date Issued</label>
            <input
              type="date"
              id="date_issued"
              v-model="newBook.date_issued"
              required
            />
          </div>
          <div class="form-group">
            <label for="price">Price</label>
            <input type="number" id="price" v-model="newBook.price" required />
          </div>
          <div class="form-group">
            <label for="content">Content</label>
            <input
              type="text"
              id="content"
              v-model="newBook.content"
              required
            />
          </div>
          <div class="form-group">
            <label for="language">Language</label>
            <input
              type="text"
              id="language"
              v-model="newBook.language"
              required
            />
          </div>
          <div class="form-group">
            <label for="image">Upload Image</label>
            <input type="file" id="image" @change="handleImageUpload($event)" />
          </div>
          <div class="form-group">
            <label for="pdf">Upload PDF</label>
            <input
              type="file"
              id="pdf"
              ref="pdf"
              accept=".pdf"
              @change="handlePDFUpload($event)"
            />
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["section_id"],
  data() {
    return {
      sectionId: "",
      showAddBookModal: false,
      currentBookIndex: null,
      newBook: {
        book_id: "",
        book_name: "",
        author_name: "",
        date_issued: "",
        price: 0,
        content: "",
        language: "",
        image_path: "",
        pdf_path: "",
      },
      selectedImageFile: null,
      selectedPDFFile: null,
    };
  },
  computed: {
    books() {
      return this.$store.getters["books/books"];
    },
    isAdmin() {
      return this.$store.getters["user/isAdmin"];
    },
  },
  methods: {
    handleImageUpload(event) {
      this.selectedImageFile = event.target.files[0];
    },
    handlePDFUpload(event) {
      this.selectedPDFFile = event.target.files[0];
    },

    closeAddBook() {
      this.showAddBookModal = false;
      this.newBook = {
        book_id: "",
        book_name: "",
        author_name: "",
        date_issued: "",
        price: 0,
        content: "",
        language: "",
        image_path: "",
        pdf_path: "",
      };
      this.selectedImageFile = null;
      this.selectedPDFFile = null;
      this.currentBookIndex = null;
    },

    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
    viewBook(book_id) {
      this.$router.push({ name: "Product", params: { book_id: book_id } });
    },
    editBook(book, index) {
      this.newBook = { ...book };
      this.currentBookIndex = index;
      this.showAddBookModal = true;
    },
    async addNewBook() {
      await this.$store.dispatch("books/addNewBook", {
        sectionId: this.sectionId,
        newBook: this.newBook,
        selectedImageFile: this.selectedImageFile,
        selectedPDFFile: this.selectedPDFFile,
      });
      this.closeAddBook();
    },
    async updateBook() {
      await this.$store.dispatch("books/updateBook", {
        newBook: this.newBook,
        selectedImageFile: this.selectedImageFile,
        selectedPDFFile: this.selectedPDFFile,
      });
      this.closeAddBook();
    },

    async confirmDeleteBook(book_id) {
      if (confirm("Are you sure you want to delete this book?")) {
        await this.$store.dispatch("books/deleteBook", book_id);
      }
    },
    async fetchBooks() {
      await this.$store.dispatch("books/fetchBooks", this.sectionId);
    },
  },
  async mounted() {
    this.sectionId = this.$route.params.section_id;
    await this.fetchBooks();
  },
};
</script>

<style scoped>
.input-group > .form-control {
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
  background-color: rgb(0, 0, 0);
  background-color: rgba(0, 0, 0, 0.4);
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
