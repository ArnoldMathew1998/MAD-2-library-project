<template>
    <div>
      <div class="container mt-6">
        <div v-for="(row, rowIndex) in chunkedBooks" :key="rowIndex" class="row row-cols-1 row-cols-md-6 g-4">
          <div v-for="(book, bookIndex) in row" :key="bookIndex" class="col">
            <div class="card">
              <img :src="book.image_path" class="card-img-top book-image" :alt="book.book_name" />
              <div class="card-body">
                <h5 class="card-title">Book Name:</h5>
                <p class="card-text">{{ book.book_name }}</p>
                <h5 class="card-title">Price</h5>
                <p class="card-text">{{ book.price }}₹</p>
                
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
        books: []
      };
    },
    computed: {
      chunkedBooks() {
        const chunkSize = 6;
        let chunks = [];
        for (let i = 0; i < this.books.length; i += chunkSize) {
          chunks.push(this.books.slice(i, i + chunkSize));
        }
        return chunks;
      }
    },
    methods: {
      async fetchBooks() {
        const token = localStorage.getItem('accessToken');
        if (token) {
          const fetchUrl = `http://127.0.0.1:5000/Api/Book`;
          const requestOptions = {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`
            }
          };
  
          await fetch(fetchUrl, requestOptions)
            .then(async response => {
              if (!response.ok) {
                return
              }
              const data = await response.json();
              this.books = data;
            })
            .catch(error => {
              console.error("There was an error fetching the books!", error);
              alert(error.message || 'Failed to fetch books');
            });
        }
      }
    },
    mounted() {
      this.fetchBooks();
    }
  };
  </script>
  
  <style scoped>
  .card {
    border: none; /* Remove card borders */
  }
  .card-body {
    padding: 1.25rem; /* Add padding inside card body */
  }
  .book-image {
    width: 156px;
    height: 104px;
    object-fit: cover; /* Ensures the image covers the entire area without distortion */
  }
  </style>
  