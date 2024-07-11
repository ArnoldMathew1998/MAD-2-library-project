<script setup>
import LoginNav from "../components/LoginNav.vue";
import HomeContent from "../components/LoginHomeContent.vue";
import Footer from "../components/LoginFooter.vue";
</script>

<template>
  <div class="body">
    <LoginNav></LoginNav>
    <div class="wrapper">
      <div class="content">
        <HomeContent></HomeContent>
      </div>
      <Footer></Footer>
    </div>
</div>
</template>

<style scoped>

.body {
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
