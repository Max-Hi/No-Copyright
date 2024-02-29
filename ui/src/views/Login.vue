<template>
<div class="flex flex-col items-center">
  <form v-on:submit.prevent="authenticate">
    <div class="text-left w-64 mb-8 space-y-2 text-center text-2xl">Login page</div>
    <div class="flex flex-col space-y-2">
      <input
        class="text-black w-64 p-1 rounded border-2"
        type="text" id="username" name="username" v-model="username"
        placeholder="username">
      <input
        class="text-black w-64 p-1 rounded border-2"
        type="password" id="password" name="password" v-model="password"
        placeholder="password">
    </div>
    <div>
      <button @click="authenticate" class="btn-primary">
        Login
      </button>
    </div>
  </form>
</div>
</template>

<script>
export default {
  data () {
    return {
      username: '',
      password: '',
    }
  },
  components: {
  },
  methods: {
    authenticate() {
      console.log("authenticating")
      this.$store.dispatch('login', { username: this.username, password: this.password })
        .then(() => this.$router.push('/'))
    },
  },
  mounted () {
  },
  beforeUnmount () {
  }
}
</script>
