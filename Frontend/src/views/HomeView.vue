<script setup>
import Homenav from '../components/Homenav.vue'
import content from '../components/HomeContent.vue'
</script>

<template>
  <main>
    <div class="home">
      <Homenav/>
      <content/>
  </div>
  </main>
</template>

<style scoped>
.home {
  width: 100%;
  position: relative;
  background: linear-gradient(90deg, #b2cbcf, #b5cacd 52%, #edb294);
  height: 1024px;
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