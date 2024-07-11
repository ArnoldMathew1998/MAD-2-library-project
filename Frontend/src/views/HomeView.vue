<script setup>
import Content from '../components/HomeContent.vue';
import Nav from '../components/HomeNav.vue';
</script>

<template>
<div class="home">
   <Nav></Nav>
    <Content/>
</div>
  
</template>

<style scoped>
.home {
  width: 100%;
  position: relative;
  background: linear-gradient(90deg, #b2cbcf, #b5cacd 52%, #edb294);
  height: 100vh;
  align-items: center;
  justify-content: flex-start;
  gap: 128px;
  text-align: left;
  font-size: 32px;
  color: var(--color-gray-100);
  font-family: var(--font-poppins);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
</style>