<template>
  <div>
    <div class="container mt-6">
      <div
        v-for="(row, rowIndex) in chunkedBooks"
        :key="rowIndex"
        class="row row-cols-1 row-cols-md-6 g-4"
      >
        <div v-for="(book, bookIndex) in row" :key="bookIndex" class="col">
          <div class="card clickable" @click="viewBook(book.book_id)">
            <img
              :src="resolvedImagePath(book.image_path)"
              class="img-card"
              :alt="book.book_name"
            />
            <div class="card-body">
              <h4 class="card-title">{{ book.book_name }}</h4>
              <p >Price:₹{{ book.price }}</p>
              <p class="card-text">{{ book.content }}</p>
            </div>
            <button type="button" class="btn btn-light btn-md">Add to Cart</button>
          </div>
          
        </div>
      </div>
    </div>
  </div>
  
</template>

<script>
export default {
  computed: {
    chunkedBooks() {
      return this.$store.getters['books/chunkedBooks'];
    },
  },
  methods: {
    resolvedImagePath(imagePath) {
      if (imagePath == null) {
        return
      }
      return require(`@/assets/book_image/${imagePath}`);
    },
    viewBook(book_id) {
      this.$router.push({ name: 'Product', params: { book_id: book_id } });
    },
    fetchBooks() {
      const fetchUrl=`http://127.0.0.1:5000/Api/Book`
      this.$store.dispatch('books/fetchBooks',fetchUrl);
    },
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
</style>
