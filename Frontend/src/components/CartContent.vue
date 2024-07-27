<template>
  <div class="cart-dropdown" :class="{ show: isVisible }">
    <div v-for="item in cartItems" :key="item.book_id" class="cart-item">
      <h5>{{ item.name }}</h5>
      <p>{{ item.content }}</p>
      <p>₹{{ item.price }}</p>
      <div class="d-grid gap-2 d-md-flex justify-content-md-end">
        <button class="btn btn-outline-danger me-md-2 btn-sm" type="button" @click="removeFromCart(item)">Remove</button>
        <button class="btn btn-outline-secondary btn-sm" type="button" @click="checkout(item)">Buy Now</button>
      </div>
    </div>
    <div class="d-grid gap-2">
      <button
        type="button"
        class="btn btn-outline-success"
        style="
          --bs-btn-padding-y: 0.25rem;
          --bs-btn-padding-x: 0.5rem;
          --bs-btn-font-size: 0.75rem;
        "
        @click="checkout(cartItems)"
      >
        Checkout
      </button>
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
    cartItems: {
      type: Array,
      default: () => [],
    },
  },
  methods: {
    async removeFromCart(item) {
      await this.$store.dispatch("cartitem/removeCartItem", item.book_id);
    },
    async checkout(itemOrCart) {
      // Determine if checking out a single item or the entire cart
      const itemsToCheckout = Array.isArray(itemOrCart) ? itemOrCart : [itemOrCart];

      // Checkout logic
      await this.$store.dispatch("checkout/addCheckoutItem", itemsToCheckout);

      // Remove items from the cart after checkout
      /* for (const item of itemsToCheckout) {
        await this.$store.dispatch("cartitem/removeCartItem", item.book_id);
      } */

      this.$router.push("/checkout");
    },
  },
};
</script>

<style scoped>
.cart-dropdown {
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
.cart-dropdown.show {
  display: block;
}
.cart-item {
  padding: 10px;
  border-bottom: 1px solid #e0e0e0;
}
.cart-item:last-child {
  border-bottom: none;
}
</style>
