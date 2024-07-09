<script setup>
import LoginNav from '../components/LoginNAV.vue'
import Profile from '../components/Profile.vue'
import Footer from '../components/Footer.vue'

</script>

<template>
    <body>
    <LoginNav/>
    <div class="wrapper">
        <div class="content">
            <Profile/>
        </div>
        <Footer/>
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