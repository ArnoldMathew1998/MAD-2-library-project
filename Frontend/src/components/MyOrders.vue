<template>
  <div>
    <table class="table">
      <thead class="table-secondary">
        <tr>
          <th scope="col">Purchase ID</th>
          <th scope="col">Book ID</th>
          <th scope="col">User ID</th>
          <th scope="col">Borrow Date</th>
          <th scope="col">Return Date</th>
          <th scope="col">Approved</th>
          <th scope="col" v-if="!isAdmin">View</th>
        </tr>
      </thead>
      <tbody v-if="myorders.length > 0">
        <tr
          v-for="(myorder, index) in myorders"
          :key="myorder.book_id"
          :class="{ 'table-secondary': index % 2 === 1 }"
        >
          <th scope="row">{{ myorder.log_id }}</th>
          <td>{{ myorder.user_id }}</td>
          <td>{{ myorder.book_id }}</td>
          <td>
            <div class="date-time">
              <span class="date">{{ formatDate(myorder.borrow_date) }}</span>
              <span class="time">{{ formatTime(myorder.borrow_date) }}</span>
            </div>
          </td>
          <td>
            <div class="date-time">
              <span class="date">{{ formatDate(myorder.return_date) }}</span>
              <span class="time">{{ formatTime(myorder.return_date) }}</span>
            </div>
          </td>
          <td v-if="isAdmin">
            <select
              class="form-select"
              @change="updateApproval(myorder.log_id, $event)"
            >
              <option :value="1" :selected="myorder.approved === 1">
                APPROVED
              </option>
              <option :value="0" :selected="myorder.approved === 0">
                PENDING
              </option>
              <option :value="-1" :selected="myorder.approved === -1">
                REJECTED
              </option>
              <option :value="-2" :selected="myorder.approved === -2">
                EXPIRED
              </option>
            </select>
          </td>
          <td v-else :class="{
            'text-success': myorder.approved === 1,
            'text-warning': myorder.approved === 0,
            'text-danger': myorder.approved === -1,
            'text-secondary': myorder.approved === -2
          }">
            {{ myorder.approved === 1 ? "APPROVED" : (myorder.approved === 0 ? "PENDING" : (myorder.approved === -1 ? "REJECTED" : (myorder.approved === -2 ? "EXPIRED" : ""))) }}
          </td>
          <td v-if="!isAdmin">
            <a v-if="myorder.approved === 1" :href="myorder.pdfUrl" target="_blank" class="text-success"> 
              {{ loadPdfUrl(myorder) ? "Download PDF" : "" }}
            </a>
            <span v-else-if="myorder.approved === 0">
              <p class="text-warning">Pending</p>
            </span>
            <span v-else-if="myorder.approved === -1" class="text-danger">Rejected</span> <span v-else-if="myorder.approved === -2" class="text-secondary">Expired</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  computed: {
    myorders() {
      return this.$store.getters["myorder/myorders"];
    },
    isAdmin() {
      return localStorage.getItem("isAdmin") === "true";
    },
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
    formatTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleTimeString();
      },
    async loadPdfUrl(order) {
      if (order.approved !== 1) return;
      if (order.approved === 1) {
        const today = new Date();
        const returnDate = new Date(order.return_date) < today;
        if (returnDate) {
           this.$store.commit("myorder/UPDATE_ORDER_APPROVED", { log_id: order.log_id, approved: -2 });
           fetch(`http://127.0.0.1:5000/Order/Approve/${order.log_id}`)
           return "Expired";
        }
      }
      if (!order.pdfUrl) {
        const pdfUrl = await this.getPdfUrl(order.book_id);
        
        this.$store.commit("myorder/UPDATE_ORDER_PDF_URL", { log_id: order.log_id, pdfUrl: pdfUrl });
        return "Download PDF";
      }
      return "Download PDF";
    },
    async getPdfUrl(book_id) {
      await this.$store.dispatch("books/fetchBooks", `http://127.0.0.1:5000/Api/Book/${book_id}`);
      const book = this.$store.getters["books/books"];
      return book ? `http://localhost:8080/assets/pdf/${book.pdf_path}` : null;
    },
    async updateApproval(log_id, event) {
      const approved = parseInt(event.target.value);
      await this.$store.dispatch("myorder/updateMyOrder", {
        log_id,
        approved,
      });
    },
  },
  created() {
    this.$store.dispatch("myorder/fetchMyOrders");
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
.clickable {
  cursor: pointer;
}
</style>
