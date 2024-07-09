<template>
    <!-- Your template structure -->
    <button @click="signOut">Sign Out</button>
  </template>
  
  <script>
  import { mapActions } from 'vuex';
  
  export default {
    methods: {
      ...mapActions(['signOut']),
      signOut() {
        this.signOut();
        this.$router.push('/');  // Redirect to home or login page after sign out
      },
    },
  };
  </script>
  