<template>
<div class="flex flex-col space-y-4">
  <div>
    <div class="flex flex-row w-full">
      <span class="text-xl flex-grow">Studios</span>
      <span class="">({{studioList.length}})</span>
    </div>
    <StudioList :studioList="studioList"/>
  </div>
</div>
</template>


<script>
import { getApi } from '@/api'
import StudioList from "../components/StudioList";

export default {
  name: 'Studios',
  components: {
    StudioList,
  },
  beforeMount() {
    getApi("/studios", this.$store.state.jwt)
      .then(data => { this.studioList = data; console.log(data) })
  },
  data(){
      return {
          studioList: {},
  }
  },
}
</script>
