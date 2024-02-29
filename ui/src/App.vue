<template>
<div class="bg-dark-red text-white">
  <div class="bg-dark-red sticky top-0 py-4 px-16">
      <Header v-if="loggedin"/>
  </div>
  <div class="px-16 min-h-screen flex flex-col flex-auto space-y-5">
      <router-view />
  </div>
  <div class="py-4 px-16">
  <Footer v-if="loggedin"/>
  </div>
</div>
</template>

<script>
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import store from "@/store"

export default {
  name: 'App',
  components: {
    Header,
    Footer
  },
  computed: {
    loggedin() {
        return store.getters["isAuthenticated"]
    }
  },
  mounted() {
    this.$store.dispatch("tryRecoverJwt")
  },
}
</script>
