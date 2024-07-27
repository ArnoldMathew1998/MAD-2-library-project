<template>
  <div class="container mt-5">
    <div class="row">
      <!-- Billing & Shipping Form -->
      <div class="col-md-7">
        <h4>BILLING & SHIPPING</h4>
        <p>This is a dummy payment page, so no need to fill in the below details for payment; just select the Return Date</p>
        <form @submit.prevent="submitOrder">
          <div class="row g-3">
            <div class="col-md-6">
              <label for="firstName" class="form-label">First name</label>
              <input type="text" class="form-control" id="firstName" placeholder="" value="" disabled>
            </div>
            <div class="col-md-6">
              <label for="lastName" class="form-label">Last name</label>
              <input type="text" class="form-control" id="lastName" placeholder="" value="" disabled>
            </div>
          </div>

          <div class="my-3">
            <label for="country" class="form-label">Country / Region</label>
            <select class="form-select" id="country" disabled>
              <option value="India" selected>India</option>
              <!-- Add more options as needed -->
            </select>
          </div>

          <div class="mb-3">
            <label for="address" class="form-label">Street address</label>
            <input type="text" class="form-control" id="address" placeholder="Apartment, suite, unit, etc. (optional)" disabled>
          </div>

          <div class="row g-3 my-3">
            <div class="col-md-6">
              <label for="zip" class="form-label">Postcode / ZIP</label>
              <input type="text" class="form-control" id="zip" placeholder="" disabled>
            </div>
            <div class="col-md-6">
              <label for="phone" class="form-label">Phone</label>
              <input type="text" class="form-control" id="phone" placeholder="" disabled>
            </div>
          </div>

          <div class="mb-3">
            <label for="email" class="form-label">Email address</label>
            <input type="email" class="form-control" id="email" placeholder="" disabled>
          </div>

          <div class="row g-3">
            <div class="col-md-6">
              <label for="borrowDate" class="form-label">Borrow Date</label>
              <input type="text" class="form-control" id="borrowDate" v-model="borrowDate" disabled>
            </div>
            <div class="col-md-6">
              <label for="returnDate" class="form-label">Return Date <span class="text-danger">*</span></label>
              <select class="form-select" id="returnDate" v-model="returnDate" required>
                <option value="" selected>Select an option...</option>
                <option value="1 Minute">1 Minute</option>
                <option value="1 Month">1 Month</option>
                <option value="Permanent">Permanent</option>
              </select>
            </div>
          </div>
          <button type="submit" class="btn btn-warning w-100 mt-3">PLACE ORDER</button>
        </form>
      </div>

      <!-- Order Summary -->
      <div class="col-md-5">
        <div class="card">
          <div class="card-body">
            <h4 class="card-title">YOUR ORDER</h4>
            <div class="d-flex justify-content-between">
              <p class="mb-0">PRODUCT</p>
              <p class="mb-0">SUBTOTAL</p>
            </div>
            <hr>
            
            <div v-for="(item, index) in checkoutItems" :key="index" class="d-flex justify-content-between">
              <p class="mb-0">{{ item.name }} × 1</p>
              <p class="mb-0">₹{{ item.price }}</p>
            </div>
            <div class="d-flex justify-content-between mt-2">
              <p class="mb-0">Monthly Price</p>
              <p class="mb-0">₹{{ totalPrice }}</p>
            </div>
            <div class="d-flex justify-content-between mt-2">
              <p class="mb-0">Permanent Price</p>
              <p class="mb-0">₹{{ PermanentPrice }}</p>
            </div>
            <hr>
            <div class="d-flex justify-content-between">
              <h5>Total</h5>
              <h5>₹{{ calculatedTotalPrice }}</h5>
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
      borrowDate: '',
      returnDate: '', // Added to track the selected return date
    };
  },
  computed: {
    checkoutItems() {
      return this.$store.getters['checkout/checkoutItems'];
    },
    totalPrice() {
      return this.checkoutItems.reduce((sum, item) => sum + item.price, 0);
    },
    PermanentPrice() {
      const multiply = (this.totalPrice * 15) / 100;
      const price = this.totalPrice + multiply;
      return (price * 10).toFixed(2);
    },
    calculatedTotalPrice() {
      if (!this.returnDate) {
        return this.totalPrice;
      }
      // Handle special case for '1 Minute'
      if (this.returnDate === '1 Minute') {
        return this.totalPrice; // Assuming the price does not change
      }
      return this.returnDate === 'Permanent' ? this.PermanentPrice : this.totalPrice;
    }
  },
  methods: {
    setBorrowDate() {
      const today = new Date();
      const dd = String(today.getDate()).padStart(2, '0');
      const mm = String(today.getMonth() + 1).padStart(2, '0'); // January is 0!
      const yyyy = today.getFullYear();
      this.borrowDate = `${yyyy}-${mm}-${dd}`;
    },
    async submitOrder() {
      if (!this.returnDate) {
        alert("Please select a return date.");
        return;
      }

      // Determine borrow duration based on returnDate
      let borrowDuration;
      if (this.returnDate === '1 Minute') {
        borrowDuration = 1; // For testing purposes, set a 1-minute duration
      } else if (this.returnDate === '1 Month') {
        borrowDuration = 28; // Approximate number of days in a month
      } else {
        borrowDuration = 100 * 365; // Assuming 100 years for "Permanent"
      }

      for (const item of this.checkoutItems) {
        try {
          await this.$store.dispatch("userLog/addLog", {
            book_id: item.book_id,
            borrow_duration: borrowDuration
          });
        } catch (error) {
          console.error("Failed to submit order:", error);
        }
      }

      // Clear the cart after placing the order
      for (const item of this.checkoutItems) {
        await this.$store.dispatch("cartitem/removeCartItem", item.book_id);
      }

      this.$router.push("/Home");
    }
  },
  created() {
    this.setBorrowDate();
  },
};

</script>

<style scoped>
/* Add any required styling here */
</style>
