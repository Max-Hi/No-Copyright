<template>
<div class="flex flex-col space-y-4">
  <div>
    <div class="flex flex-row w-full">
      <span class="text-xl flex-grow">Tags</span>
      <span class="">({{tagList.length}})</span>
    </div>
    <TagList :tagList="tagList"/>
  </div>
</div>
</template>


<script>
import { getApi } from '@/api'
import TagList from "../components/TagList";

export default {
  name: 'Tags',
  components: {
    TagList,
  },
  beforeMount() {
    getApi("/tags", this.$store.state.jwt)
      .then(data => { this.tagList = data; console.log(data) })
  },
  data(){
      return {
          tagList: {},
  }
  },
}
</script>
