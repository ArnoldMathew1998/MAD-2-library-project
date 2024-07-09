<!-- <script setup>
import WelcomeItem from './WelcomeItem.vue'
import DocumentationIcon from './icons/IconDocumentation.vue'
import ToolingIcon from './icons/IconTooling.vue'
import EcosystemIcon from './icons/IconEcosystem.vue'
import CommunityIcon from './icons/IconCommunity.vue'
import SupportIcon from './icons/IconSupport.vue'
</script> -->

<template>
  <div class="content">
        <div class="content1">
          <div class="headline-and-subhead">
            <div class="books-are-a-container">
              <p class="books-are-a">Books are a uniquely</p>
              <p class="books-are-a">portable magic.</p>
              <p class="stephen-king">– Stephen King</p>
            </div>
          </div>
        </div>
          <div class="input-group input-group-lg">
            <input type="text" class="form-control" aria-label="Sizing example input" placeholder="Enter your book" aria-describedby="inputGroup-sizing-lg">
          <button type="button" class="btn btn-dark btn-lg">Search</button></div>
      </div>
</template>

<style scoped>

.books-are-a {
  margin: 0;
}
.stephen-king {
  margin: 0;
  white-space: pre-wrap;
}
.books-are-a-container {
  align-self: stretch;
  position: relative;
  line-height: 64px;
  font-weight: 500;
}
.headline-and-subhead {
  width: 633px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: flex-end;
}
.content1 {
  align-self: stretch;
  flex: 1;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
}

.content {
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.content {
  width: 749px;
  backdrop-filter: blur(24px);
  border-radius: 24px;
  background-color: rgba(255, 255, 255, 0.25);
  height: 617px;
  flex-shrink: 0;
  align-items: flex-start;
  justify-content: center;
  padding: 121px 64px;
  box-sizing: border-box;
  gap: 13px;
}

</style>