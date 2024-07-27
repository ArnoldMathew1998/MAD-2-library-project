<script setup>
import LoginNav from "../components/LoginNav.vue";
import Dashboard from "../components/AdminDashboard.vue";
import Footer from "../components/LoginFooter.vue";
</script>

<template>
<body>
<LoginNav></LoginNav>
<div class="wrapper">
    <div class="content">
        <Dashboard></Dashboard>
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