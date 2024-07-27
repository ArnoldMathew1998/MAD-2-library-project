<template>
    <div class="container mt-4">
      <div class="row">
        <div class="col-md-6">
          <div class="mb-3">
            <img
              :src="resolvedImagePath(books.image_path)"
              class="img-fluid fixed-size-image"
              alt="Product Image"
            />
          </div>
        </div>
        <div class="col-md-6">
          <h2>{{ books.book_name }} : {{ books.content }}</h2>
          <div class="d-flex align-items-center mb-3">
            <span class="badge bg-warning text-dark me-2">{{ averageRating }}</span>
            <span>{{ totalRatings }} ratings</span>
          </div>
          <div class="mb-3">
            <h3 class="text-danger">Monthly Price:₹{{ books.price }}</h3>
          <p><del>₹{{ discountedPrice }}</del> <span class="text-danger">-{{ discountPercentage }}%</span></p>
          <p>Permanent Price:₹{{ discountedPrice*10 }}</p>
          </div>
          <div class="mb-3"  v-if="!isAdmin">
            <button class="btn btn-warning w-100 mb-2" @click="addToCart" :disabled="!cart">
            {{ cart ? "Add to Cart" : "Already in Cart" }}
          </button>
            <button class="btn btn-success w-100 mb-2" @click="checkout()" :disabled="!buy">{{ buy ? "Buy Now" : "Maximum Limit" }}</button>
          </div>
          <div class="mb-3"  v-if="!isAdmin">
            <button class="btn btn-outline-secondary w-100" @click="addToWishlist" :disabled="!wishlist">{{ wishlist ? "Add to Wishlist" : "Already in Wishlist" }}</button>
          </div>
        </div>
      </div>
    </div>
  </template>

<script>

export default {
  props: ["book_id"],
  data() {
    return {
      book_Id: "",
      discountPercentage: 15, // Set your discount percentage here
      cart: true,
      wishlist: true,
      buy: true,
    };
  },
  computed: {
    cartItems() {
      return this.$store.getters["cartitem/cartItems"];
    },
    isAdmin() {
      return localStorage.getItem("isAdmin") === "true";
    },

    wishlistItems() {
      return this.$store.getters["wishlist/wishItems"];
    },
    books() {
      return this.$store.getters["books/books"];
    },
    feedbacks() {
      return this.$store.getters["feedback/feedbacks"];
    },
    totalRatings() {
      /* return this.feedbacks.length; */
      if (this.feedbacks.length === 0) {
        return 0;
      }
      const sum = this.feedbacks.reduce((total, feedback) => {
        return total + feedback.feedback_rating;
      }, 0);
      return sum; 
    },
    
    averageRating() {
      if (this.feedbacks.length === 0) {
        return 0;
      }
      const sum = this.feedbacks.reduce((total, feedback) => {
        return total + feedback.feedback_rating;
      }, 0);
      return (sum / this.feedbacks.length).toFixed(1);
    },
    discountedPrice() {
      if (!this.books.price) return 0;
      const discount = (this.books.price * this.discountPercentage) / 100;
      return (this.books.price + discount).toFixed(2);
    },
  },
  methods: {
    async checkout() {
      // Determine if checking out a single item or the entire cart
      const itemsToCheckout = Array.isArray(this.books) ? this.books : [this.books];

      await this.$store.dispatch("checkout/addCheckoutItem", itemsToCheckout);         

      this.$router.push("/checkout");
    },
    async addToCart() {
      if (this.cart) {
        await this.$store.dispatch("cartitem/addCartItem", this.book_Id);
        this.cart = false;
      }
    },
    async addToWishlist() {
      if (this.wishlist) {
        await this.$store.dispatch("wishlist/addwishItem", this.book_Id);
        this.wishlist = false;
      }
    },
    checkIfInCart() {
      this.cart = !this.cartItems.some((f) => f.book_id == this.book_Id);
    },
    checkIfInwishlist() {
      this.wishlist = !this.wishlistItems.some((f) => f.book_id == this.book_Id);
    },
    async fetchBooks() {
      const fetchUrl = `http://127.0.0.1:5000/Api/Book/${this.book_Id}`;
      await this.$store.dispatch("books/fetchBooks", fetchUrl);
    },
    resolvedImagePath(imagePath) {
        if (imagePath == null) {
          return require('@/assets/book_image/default.jpg');
        }
        return require(`@/assets/book_image/${imagePath}`);
      },
   async totalorders() {
      await this.$store.dispatch("myorder/fetchMyOrders");
      const orders = this.$store.getters["myorder/myorders"];
      let sum=0
      for (const order of orders) {
        if (order.approved >= 0) {
          sum = sum + 1
        }
      }
      
      if (sum >= 5) {
        this.buy = false 
      }
    },
  },
  async created() {
    this.book_Id = this.$route.params.book_id;
    await this.fetchBooks();
    this.checkIfInCart();
    this.checkIfInwishlist();
    this.totalorders();
  },
  watch: {
    cartItems: 'checkIfInCart',
    wishlistItems: 'checkIfInwishlist'

  }
};
</script>

<style scoped>
.fixed-size-image {
  width: 415px; /* Set the desired width */
  height: 600px; /* Set the desired height */
  object-fit: cover; /* Ensures the image covers the area and maintains aspect ratio */
}
</style>