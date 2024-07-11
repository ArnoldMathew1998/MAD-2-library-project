<script setup>
import SignInLeft from '../components/SignInLeft.vue'
import SignInRight from '../components/SignInRight.vue' 
</script>

<template>
    <main>
        <div class="sign-in">
          <SignInLeft/>
          <SignInRight/>
        </div>
    </main>
  </template>

  <style scoped>
.sign-in {
  width: 100%;
  position: relative;
  background-color: var(--color-white);
  flex-direction: row;
  align-items: flex-start;
  text-align: center;
  font-size: 56px;
  color: var(--color-black);
  font-family: var(--font-poppins);
  display: flex;
  justify-content: flex-start;
  height: 100vh;
  overflow: hidden;
}
  </style>