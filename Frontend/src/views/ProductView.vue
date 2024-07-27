<script setup>
import LoginNav from "../components/LoginNav.vue";
import Product from "../components/ProductContent.vue";
import Footer from "../components/LoginFooter.vue";
import Review from "../components/ReviewContent.vue";
</script>

<template>
  <body>
    <LoginNav></LoginNav>
    <div class="wrapper">
      <div class="content">
        <Product></Product>
        <Review></Review>
      </div>
      <Footer></Footer>
    </div>
  </body>
</template>


<style scoped>
html,
body {
  height: 100%;
}
.wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.content {
  flex: 1;
}
</style>
