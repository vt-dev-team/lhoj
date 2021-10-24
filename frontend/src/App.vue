<script setup>
import NavBar from "./components/NavBar.vue"
import Footer from "./components/Footer.vue"
</script>

<template>
  <div>
    <NavBar></NavBar>
    <div class="container main">
      <router-view v-slot="{ Component }">
        <transition name="fade">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
    <Footer></Footer>
  </div>
</template>

<style scoped>
.main {
  margin-top: 30px;
}
</style>