<template>
  <div class="container mt-4">
    <div v-for="feedback in feedbacks" :key="feedback.feedback_id" class="review-container">
      <div class="row">
        <div class="col-md-12">
          <div class="review-header">
            <img :src="resolvedImagePath(feedback.profile_photo)" alt="Avatar" class="review-avatar">
            <div>
              <div class="name">{{ feedback.Name }}</div>
              <div class="text-muted">{{ feedback.Email }}</div>

            </div>
            <div class="ms-auto review-rating">
              <span>{{ '⭐'.repeat(feedback.feedback_rating) }}</span>
            </div>
          </div>
          <p>{{ feedback.feedback_text }}</p>
          <div v-if="feedback.user_id == userId">
            <p v-bind="add=false" ></p>
            <button @click="editFeedback(feedback)" class="btn btn-outline-secondary me-md-2 btn-sm">Edit</button>
            <button @click="deleteFeedback(feedback)" class="btn btn-outline-danger btn-sm">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <div class="text-center mt-4">
      <button v-if="add && !isAdmin" @click="showAddReviewModal" class="btn btn-outline-secondary">Add Your Review</button>
    </div>

    <AddReviewModal
      v-if="showModal"
      :feedback="selectedFeedback"
      @close="showModal = false"
      @submit="handleFeedbackSubmit"
    />
  </div>
</template>


<script>
import AddReviewModal from './AddReview.vue'; // Ensure the path is correct

export default {
  components: {
    AddReviewModal
  },
  data() {
    return {
      showModal: false,
      selectedFeedback: null,
      userId: localStorage.getItem("user_id"),
      action: '',
      add: 'true'
    };
  },  
  computed: {
    isAdmin() {
        return localStorage.getItem("isAdmin") === "true";
    },
    feedbacks() {
      return this.$store.getters['feedback/feedbacks'];
    }
  },
  methods: {
    async fetchFeedbacks() {
      const bookId = this.$route.params.book_id;
      await this.$store.dispatch('feedback/loadFeedbacksWithUserDetails', bookId);
      this.add='true'
    },
      resolvedImagePath(imagePath) {
        if (imagePath == null) {
          return require('@/assets/book_image/default.jpg');
        }
        return require(`@/assets/book_image/${imagePath}`);
      },
   
     showAddReviewModal() {
      this.selectedFeedback = null; // Reset the selected feedback for new review
      this.showModal = true;
    },
    handleFeedbackSubmit(feedback) {
      if(feedback.book_id==null) return
      if (this.action === 'edit') {
        // Edit existing feedback
        this.$store.dispatch('feedback/editFeedback', feedback).then(() => {
          this.showModal = false;
        });
      } 

      if (this.add === 'true') {
        // Add new feedback
        this.$store.dispatch('feedback/addFeedback', feedback).then(() => {
          this.showModal = false;
        });
      }
    },
    editFeedback(feedback) {
      this.selectedFeedback = { ...feedback }; // Clone the feedback to avoid direct mutation
      this.showModal = true;
      this.action = 'edit';
      
    },
    deleteFeedback(feedback) {
      this.$store.dispatch('feedback/deleteFeedback', feedback);
      this.add = 'true';
      this.action = '';
    }
  },
  mounted() {
    this.fetchFeedbacks();
  }
};
</script>

<style scoped>
.review-container {
  border: 1px solid #e0e0e0;
  padding: 20px;
  border-radius: 5px;
  margin-bottom: 20px;
}
.review-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}
.review-header {
  display: flex;
  align-items: center;
}
.review-header img {
  margin-right: 15px;
}
.review-header .name {
  font-weight: bold;
}
.review-rating {
  color: orange;
}
</style>
