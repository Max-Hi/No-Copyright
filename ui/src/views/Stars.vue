<template>
<div class="flex flex-col space-y-4">
  <div>
    <div class="flex flex-row w-full">
      <span class="text-xl flex-grow">Stars</span>
      <span class="">({{starList.length}})</span>
    </div>
    <StarList :starList="starList"/>
  </div>
</div>
</template>


<script>
import { getApi } from '@/api'
import StarList from "../components/StarList";

export default {
  name: 'Stars',
  components: {
    StarList,
  },
  beforeMount() {
    getApi("/stars", this.$store.state.jwt)
      .then(data => { this.starList = data; console.log(data) })
  },
  data(){
      return {
          starList: {},
  }
  },
}
</script>
