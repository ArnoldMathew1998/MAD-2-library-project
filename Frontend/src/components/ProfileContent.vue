<template>
  <div class="container mt-4">
    <div class="profile-container">
      <h2>User Profile</h2>
      <div class="profile-header">
        <input
          type="file"
          @change="onPhotoChange"
          ref="photoInput"
          style="display: none"
        />
        <img
          :src="previewPhoto || resolvedImagePath(user.profile_photo)"
          alt="Avatar"
          class="profile-avatar clickable"
          @click="triggerPhotoUpload"
        />
        <div>
          <h4>{{ user.first_name }} {{ user.last_name }}</h4>
          <p>{{ user.mail_id }}</p>
        </div>
        <div class="profile-buttons">
          <button class="btn btn-outline-secondary" @click="deletePhoto">
            Delete Photo
          </button>
        </div>
      </div>
      <form @submit.prevent="saveChanges">
        <div class="row">
          <div class="col-md-6">
            <label for="firstName" class="form-label">First Name</label>
            <input
              type="text"
              class="form-control"
              id="firstName"
              v-model="user.first_name"
              placeholder="eg. Arnold"
            />
          </div>
          <div class="col-md-6">
            <label for="lastName" class="form-label">Last Name</label>
            <input
              type="text"
              class="form-control"
              id="lastName"
              v-model="user.last_name"
              placeholder="eg. Mathew"
            />
          </div>
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">Email Address</label>
          <input
            type="text"
            class="form-control"
            id="email"
            v-model="user.mail_id"
            placeholder="example@example.com"
          />
        </div>
        <div class="row">
          <div class="col-md-4">
            <label for="currentPassword" class="form-label"
              >Current Password</label
            >
            <input
              type="password"
              class="form-control"
              id="currentPassword"
              v-model="currentPassword"
              placeholder="Current Password"
            />
          </div>
          <div class="col-md-4">
            <label for="newPassword" class="form-label">New Password</label>
            <input
              type="password"
              class="form-control"
              id="newPassword"
              v-model="newPassword"
              placeholder="New Password"
            />
          </div>
          <div class="col-md-4">
            <label for="confirmPassword" class="form-label"
              >Confirm New Password</label
            >
            <input
              type="password"
              class="form-control"
              id="confirmPassword"
              v-model="confirmPassword"
              placeholder="Confirm New Password"
            />
          </div>
        </div>
        <div class="mt-4 d-flex justify-content-end">
          <button
            type="button"
            class="btn btn-outline-secondary me-2"
            @click="cancel"
          >
            Cancel
          </button>
          <button type="submit" class="btn btn-primary">Save Changes</button>
          <button class="btn btn-outline-danger ms-2" @click="deleteUser">
            Delete Account
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentPassword: "",
      newPassword: "",
      confirmPassword: "",
      selectedPhoto: null,
      previewPhoto: null,
    };
  },
  computed: {
    user() {
      return this.$store.getters["user/user"];
    },
  },
  methods: {
    resolvedImagePath(imagePath) {
      try {
        if (imagePath == null) {
          return require("@/assets/book_image/default.jpg");
        }
        return require(`@/assets/book_image/${imagePath}`);
      } catch (e) {
        // If the image cannot be resolved, return the default image
        return require("@/assets/book_image/default.jpg");
      }
    },
    async saveChanges() {
      if (this.newPassword !== this.confirmPassword) {
        alert("New password and confirm password do not match");
        return;
      }
      if (this.selectedPhoto) {
        this.user["profile_photo"] = await this.$store.dispatch(
          "books/uploadfile",
          { file: this.selectedPhoto }
        );
      }

      const updatedUser = {
        ...this.user,
        password: this.newPassword,
        currentPassword: this.currentPassword,
      };

      await this.$store.dispatch("user/updateUser", updatedUser);
    },
    cancel() {
      this.$router.push("/");
    },
    triggerPhotoUpload() {
      this.$refs.photoInput.click();
    },
    onPhotoChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedPhoto = file;
        this.previewPhoto = URL.createObjectURL(file);
      }
    },
    async deleteUser() {
      if (confirm("Are you sure you want to delete your profile?")) {
        if (this.currentPassword) {
          await this.$store.dispatch("user/deleteUser", this.currentPassword);
          this.$router.push("/SignIn");
        } else {
          alert("Please enter your current password to delete your profile.");
        }
      }
    },

    deletePhoto() {
      this.user["profile_photo"] = null;
      this.user["profile_photo_url"] = "delete";
      this.previewPhoto = null;
    },

    async fetchUser() {
      const user_id = localStorage.getItem("user_id");
      await this.$store.dispatch("user/getUser", user_id);
    },
  },
  created() {
    this.fetchUser();
  },
};
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  background-color: #fff;
}
.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}
.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-right: 20px;
}
.profile-buttons {
  margin-left: auto;
}
.form-control {
  margin-bottom: 15px;
}
.clickable {
  cursor: pointer;
}
</style>
