<script setup>
import { ref, computed } from "vue";
import HomeNav from "../components/HomeNav.vue";
import LoginNav from "../components/LoginNav.vue";
import Footer from "../components/LoginFooter.vue";
import Search from "../components/SearchBooks.vue";

const isLoggedIn = ref(localStorage.getItem('accessToken') !== null);

const NavComponent = computed(() => (isLoggedIn.value ? LoginNav : HomeNav));
</script>

<template>
  <div :class="isLoggedIn ? 'body-logged-in' : 'body'">
    <component :is="NavComponent"></component>
    <div class="wrapper">
      <div class="content">
        <Search></Search>
      </div>
      <Footer></Footer>
    </div>
  </div>
</template>

<style scoped>
.body {
  height: 100%;
  width: 100%;
  background: linear-gradient(90deg, #b2cbcf, #b5cacd 52%, #edb294);
  height: 100vh;
  gap: 40px;
  text-align: left;
  font-size: 20px;
  overflow: auto;
  display: flex;
  flex-direction: column;
}

.body-logged-in {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
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
