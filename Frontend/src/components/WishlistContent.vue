<template>
  <div class="wishlist-dropdown" :class="{ show: isVisible }">
    <!-- <h4>Wishlist Items</h4> -->
    <div v-for="item in wishlistItems" :key="item.id" class="wishlist-item">
      <h5>{{ item.name }}</h5>
      <p>{{ item.name }}</p>
      <p>Content: {{ item.content }}</p>
      <p>${{ item.price }}</p>
      <div class="d-grid gap-2 d-md-flex justify-content-md-end">
  <button class="btn btn-outline-danger me-md-2 btn-sm" type="button" @click="removeFromWishlist(item)">Remove</button>
  <button class="btn btn-outline-secondary btn-sm" type="button" @click="addToCart(item)">Add to Cart</button>
</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
    wishlistItems: {
      type: Array,
      default: () => [],
    },
  },
  methods: {
    async removeFromWishlist(item) {
      await this.$store.dispatch("wishlist/removewishItem", item.book_id);
    },
    async addToCart(item) {
      await this.$store.dispatch("cartitem/addCartItem", item.book_id);
      await this.$store.dispatch("wishlist/removewishItem", item.book_id);
    },
  },
};
</script>

<style scoped>
.wishlist-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 250px;
  background-color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  display: none;
  z-index: 1000;
}
.wishlist-dropdown.show {
  display: block;
}
.wishlist-item {
  padding: 10px;
  border-bottom: 1px solid #e0e0e0;
}
.wishlist-item:last-child {
  border-bottom: none;
}
</style>
