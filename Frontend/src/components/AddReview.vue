<template>
  <div class="modal-backdrop" @click.self="close">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" @click="close">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitFeedback">
            <div class="form-group">
              <label for="feedbackText">Review</label>
              <textarea id="feedbackText" class="form-control" v-model="feedbackText" required></textarea>
            </div>
            <div class="form-group">
              <label for="feedbackRating">Rating</label>
              <select id="feedbackRating" class="form-control" v-model.number="feedbackRating" required>
                <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
              </select>
            </div>
            <button type="submit" class="btn btn-outline-primary me-md-2 btn-sm">Submit</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    feedback: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      feedbackText: this.feedback ? this.feedback.feedback_text : '',
      feedbackRating: this.feedback ? this.feedback.feedback_rating : 1
    };
  },
  methods: {
    close() {
      this.$emit('close');
    },
    submitFeedback() {
      const newFeedback = {
        book_id: this.$route.params.book_id,
        feedback_text: this.feedbackText,
        feedback_rating: this.feedbackRating
      };
      this.$emit('submit', newFeedback);
    }
  }
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-dialog {
  background: #fff;
  padding: 20px;
  border-radius: 5px;
  width: 100%;
  max-width: 500px;
}
</style>
