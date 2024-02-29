<template>
<div class="flex flex-row flex-auto space-x-3 justify-center">
  <router-link to="/">Search</router-link> 
  <div>|</div> 
  <router-link to="/upload">Upload</router-link>
  <div class="text-center flex-grow">No Copyright Movies</div>
  <router-link to="/personal">Personal</router-link>
  <div>|</div>
  <button @click="logout">Logout</button>
</div>
</template>

<script>
export default {
  name: 'Header',
  methods: {
    logout() {
        this.$store.dispatch("logout")
          .then(() => this.$router.push("/login"))
    }
  }
}
</script>
