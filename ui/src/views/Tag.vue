<template>
<div class="flex flex-col space-y-4">
  <div class="text-3xl">{{tagname}}</div>
  <!-- Studios -->
  <div>
    <div class="flex flex-row w-full">
      <span class="text-xl flex-grow">Studios with {{tagname}}:</span>
      <span class="">({{studioList.length}})</span>
    </div>
    <StudioList :studioList="studioList"/>
  </div>
  <!-- Stars -->
  <div>
    <div class="flex flex-row w-full">
      <span class="text-xl flex-grow">Stars with {{tagname}}:</span>
      <span class="">({{starList.length}})</span>
    </div>
    <StarList :starList="starList"/>
  </div>
  <!-- Videos -->
  <div>
    <div class="flex flex-row w-full mb-2">
      <span class="text-xl flex-grow">Videos with {{tagname}}:</span>
      <span class="">({{videoList.length}})</span>
    </div>
    <div class="flex flex-wrap gap-x-6 gap-y-10 justify-center items-start">
        <template v-for="video in videoList" v-bind:key="video.id">
            <VideoDisplay :video="video"/>
        </template>
    </div>
  </div>
</div>
</template>


<script>
import { postApi } from '@/api'
import VideoDisplay from '@/components/VideoDisplay'
import StudioList from "../components/StudioList";
import StarList from "../components/StarList";

export default {
  name: 'Tag',
  components: {
    StarList,
    StudioList,
      VideoDisplay,
  },
  computed: {
    tagname: function() {
      return decodeURIComponent(this.$route.params.tagname)
    }
  },
  beforeMount() {
    postApi("/tag", {name: this.$route.params.tagname}, this.$store.state.jwt)
      .then(data => { this.videoList = data.videoList;
                      this.starList = data.starList;
                      this.studioList = data.studioList;
                    console.log(data) })
  },
  data(){
      return {
          videoList: {},
          starList: {},
          studioList: {},
          searchWithDescriptor: "without",
  }
  },
  methods: {
      toggleJunktor() {
       this.searchWithDescriptor = (this.searchWithDescriptor === "without" ? "with" : "without")
    },
  }
}
</script>

