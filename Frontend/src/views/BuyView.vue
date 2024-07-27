<script setup>
import LoginNav from "../components/LoginNav.vue";
import Buy from '../components/BuyOrders.vue'
import Footer from "../components/LoginFooter.vue";
</script>

<template>
<body>
<LoginNav></LoginNav>
<div class="wrapper">
    <div class="content">
        <Buy></Buy>
    </div>
    <Footer></Footer>
</div>
</body> 
</template>

<style  scoped>
        html, body {
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