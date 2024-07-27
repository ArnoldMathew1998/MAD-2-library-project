<template>
  <div>
        <div class="input-group rounded" style="padding-bottom: 10px;">
  <input type="search" class="form-control rounded" placeholder="Search" aria-label="Search" aria-describedby="search-addon" v-model="searchQuery" @keypress.enter="searchBooks"/>
</div>
  <div>
    <div class="container mt-6">
      <div
        v-for="(row, rowIndex) in chunkedBooks"
        :key="rowIndex"
        class="row row-cols-1 row-cols-md-6 g-4"
      >
        <div v-for="(book, bookIndex) in row" :key="bookIndex" class="col">
          <div class="card clickable">
            <div class="image-container">
              <i :class="{'bi bi-heart heart-icon': wishlistStatus(book.book_id), 'bi bi-heart-fill heart-icon': !wishlistStatus(book.book_id)}" @click="addtowishlist(book.book_id)" v-if="!isAdmin"
              ></i>
              <img
                :src="resolvedImagePath(book.image_path)"
                class="img-card"
                :alt="book.book_name"
                @click="viewBook(book.book_id)"
              />
            </div>
            <div class="card-body" @click="viewBook(book.book_id)">
              <h4 class="card-title">{{ book.book_name }}</h4>
              <p>Price:₹{{ book.price }}</p>
              <p class="card-text">{{ book.content }}</p>
            </div>
            
            <i :class="{'bi bi-cart btn btn-light btn-md': cartStatus(book.book_id), 'bi bi-cart-fill btn btn-light btn-md text-red': !cartStatus(book.book_id)}" @click="addToCart(book.book_id)" v-if="!isAdmin">Cart</i>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: "",
    };
  },
  computed: {
    isAdmin() {
      return localStorage.getItem("isAdmin") === "true";
    },
    cartItems() {
      return this.$store.getters["cartitem/cartItems"];
    },
    wishlistItems() {
      return this.$store.getters["wishlist/wishItems"];
    },
    chunkedBooks() {
      return this.$store.getters["books/chunkedBooks"];
    },
  },
  methods: {
    async addToCart(book_id) {
      if (this.cartStatus(book_id)) {
        await this.$store.dispatch("cartitem/addCartItem", book_id);
      }
      else {
        await this.$store.dispatch("cartitem/removeCartItem", book_id);
      }
    },
    async addtowishlist(book_id) {
      if (this.wishlistStatus(book_id)) {
        await this.$store.dispatch("wishlist/addwishItem", book_id);
      }
      else {
        await this.$store.dispatch("wishlist/removewishItem", book_id);
      }
    },
    cartStatus(book_id) {
      return !this.cartItems.some((f) => f.book_id === book_id);
    },
    wishlistStatus(book_id) {
      return !this.wishlistItems.some((f) => f.book_id === book_id);
    },
    resolvedImagePath(imagePath) {
      if (!imagePath) {
        return require('@/assets/book_image/default.jpg');
      }
      return require(`@/assets/book_image/${imagePath}`);
    },
    viewBook(book_id) {
      this.$router.push({ name: "Product", params: { book_id: book_id } });
    },
    fetchBooks() {
      const fetchUrl = `http://127.0.0.1:5000/Api/Book`;
      this.$store.dispatch("books/fetchBooks", fetchUrl);
    },
    searchBooks() {
      this.$store.dispatch("searchbook/fetchBooks", this.searchQuery);
      this.$router.push("/search");
    }
  },
  mounted() {
    this.fetchBooks();
  },
};
</script>

<style scoped>
.card-body {
  padding: 1.25rem;
}

.clickable {
  cursor: pointer;
}

.card:hover {
  box-shadow: 0 8px 17px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}

.image-container {
  position: relative;
}

.heart-icon {
  position: absolute;
  top: 10px;
  right: 10px;
  color: rgb(228, 91, 91);
  font-size: 1.5rem;
  z-index: 1;
}

.img-card {
  width: 100%;
}
.text-red {
  color: rgb(228, 91, 91) !important;
}
</style>
