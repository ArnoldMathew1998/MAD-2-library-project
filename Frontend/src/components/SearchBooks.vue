<template>
    <div>
        <div class="input-group rounded" style="padding-bottom: 10px;">
  <input type="search" class="form-control rounded" placeholder="Search" aria-label="Search" aria-describedby="search-addon" v-model="searchQuery" @keypress.enter="searchBooks"/>
</div>

  <div>
    

    <table class="table">
      <thead class="table-secondary">
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Book Name</th>
          <th scope="col">Author Name</th>
          <th scope="col">Description</th>
          <th scope="col">Date Issued</th>
          <th scope="col">Price</th>
          <th scope="col">View</th>
        </tr>
      </thead>

      <tbody v-if="books.length > 0">
        <tr
          v-for="(book, index) in books"
          :key="book.book_id"
          :class="{ 'table-secondary': index % 2 === 1 }"
        >
          <th scope="row">{{ book.book_id }}</th>
          <td>{{ book.book_name }}</td>
          <td>{{ book.author_name }}</td>
          <td>{{ book.content }}</td>
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
        </tr>
      </tbody>
    </table>
  </div>
</div>
</template>

<script>
export default {
  data() {
      return {
        searchQuery: "",
      }
  },
  computed: {
    books() {
      return this.$store.getters["searchbook/SearchBooks"];
    },
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
    viewBook(book_id) {
      this.$router.push({ name: "Product", params: { book_id: book_id } });
    },
    searchBooks() {
      this.$store.dispatch("searchbook/fetchBooks", this.searchQuery);
    }
  }
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
.clickable {
  cursor: pointer;
}
</style>
