<template>
  <div class="row">
    <!-- Sidebar -->
    <div class="col-md-2 sidebar">
      <div class="d-flex flex-column p-3">
        <h3>Dashboard</h3>
        <input type="text" class="form-control mb-3" placeholder="Search..." v-model="searchQuery" @keypress.enter="searchSection">
        <h4>Section</h4>
        
        <ul class="list-group" v-if="sections.length > 0">
          <li
            class="list-group-item"
            v-for="section in sections"
            :key="section.sec_id"
          >
            <input
              class="form-check-input me-1"
              type="radio"
              name="listGroupRadio"
              :id="'radio' + section.sec_id"
              :checked="section.sec_id == sectionId"
              @click="viewSection(section.sec_id)"
            />
            <label class="form-check-label" :for="'radio' + section.sec_id">
              {{ section.sec_name }}
            </label>
          </li>
        </ul>
      </div>
    </div>
    <!-- Main Content -->
    <div class="col-md-10 content">
      <input type="text" class="form-control mb-3" placeholder="Search..." v-model="bookSearchQuery" @keypress.enter="fetchBooks">
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
            <th v-if="!isAdmin" scope="col">Cart</th>
            <th v-if="isAdmin" scope="col">Delete</th>
            <th v-if="!isAdmin" scope="col">Wishlist</th>
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
              v-if="!isAdmin"
              class="link-warning link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover clickable"
              @click="addToCart(book.book_id)"
            >
              <i
                :class="{
                  'bi bi-cart btn btn-light btn-md': cartStatus(book.book_id),
                  'bi bi-cart-fill btn btn-light btn-md text-red': !cartStatus(
                    book.book_id
                  ),
                }"
              ></i>
            </td>
            <td
              v-if="isAdmin"
              class="link-danger link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover clickable"
              @click="confirmDeleteBook(book.book_id)"
            >
              Delete
            </td>
            <td
              v-if="!isAdmin"
              class="link-warning link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover clickable"
              @click="addtowishlist(book.book_id)"
            >
              <i
                :class="{
                  'bi bi-heart btn btn-light btn-md': wishlistStatus(book.book_id),
                  'bi bi-heart-fill btn btn-light btn-md text-red': !wishlistStatus(
                    book.book_id
                  ),
                }"
              ></i>
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
              <input
                type="number"
                id="price"
                v-model="newBook.price"
                required
              />
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
              <input
                type="file"
                id="image"
                @change="handleImageUpload($event)"
              />
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
      searchQuery: "",
      bookSearchQuery:"",
    };
  },
  computed: {
    books() {
      return this.$store.getters["searchbook/SearchBooks"];
    },
    isAdmin() {
      return localStorage.getItem("isAdmin") === "true";
    },
    sections() {
      return this.$store.getters["searchbook/SearchSection"];
    },
    cartItems() {
      return this.$store.getters["cartitem/cartItems"];
    },
    wishlistItems() {
      return this.$store.getters["wishlist/wishItems"];
    },
  },
  methods: {
    searchSection() {
      this.$store.dispatch("searchbook/fetchSection", this.searchQuery);
    },
    async addToCart(book_id) {
      if (this.cartStatus(book_id)) {
        await this.$store.dispatch("cartitem/addCartItem", book_id);
      } else {
        await this.$store.dispatch("cartitem/removeCartItem", book_id);
      }
    },
    async addtowishlist(book_id) {
      if (this.wishlistStatus(book_id)) {
        await this.$store.dispatch("wishlist/addwishItem", book_id);
      } else {
        await this.$store.dispatch("wishlist/removewishItem", book_id);
      }
    },
    cartStatus(book_id) {
      return !this.cartItems.some((f) => f.book_id === book_id);
    },
    wishlistStatus(book_id) {
      return !this.wishlistItems.some((f) => f.book_id === book_id);
    },
    viewSection(sec_id) {
      this.$router.push({ name: "Book", params: { section_id: sec_id } });
    },
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
      await this.$store.dispatch("searchbook/addNewBook", {
        sectionId: this.sectionId,
        newBook: this.newBook,
        selectedImageFile: this.selectedImageFile,
        selectedPDFFile: this.selectedPDFFile,
      });
      this.closeAddBook();
    },
    async updateBook() {
      await this.$store.dispatch("searchbook/updateBook", {
        newBook: this.newBook,
        selectedImageFile: this.selectedImageFile,
        selectedPDFFile: this.selectedPDFFile,
      });
      this.closeAddBook();
    },

    async confirmDeleteBook(book_id) {
      if (confirm("Are you sure you want to delete this book?")) {
        await this.$store.dispatch("searchbook/deleteBook", book_id);
      }
    },
    async fetchBooks() {
      await this.$store.dispatch("searchbook/fetchSectionBook", {'sec_id':this.sectionId,'searchQuery':this.bookSearchQuery});
    },
  },
  async mounted() {
    this.sectionId = this.$route.params.section_id;
    this.searchSection();
    await this.fetchBooks();
    
  },
  watch: {
    $route: {
      immediate: true,
      async handler(to) {
        this.sectionId = to.params.section_id || "";
        await this.fetchBooks();
      },
    },
  },
};
</script>
<style scoped>
.sidebar {
  background-color: #6c757d7f;
  min-height: 100vh;
}
.content {
  padding: 20px;
}
.table-secondary {
  background-color: #6c757d;
}
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
.text-red {
  color: rgb(228, 91, 91) !important;
}
</style>
