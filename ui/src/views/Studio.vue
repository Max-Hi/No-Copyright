<template>
<div class="flex flex-col space-y-4">
  <div class="text-3xl">{{decodeURIComponent(this.$route.params.studioname)}}</div>
  <!-- Tags -->
  <div>
    <span class="text-xl">Tags often contained in Videos by {{decodeURIComponent(this.$route.params.studioname)}}:</span>
    <span class="justify-right">({{tagList.length}})</span>
    <TagList :tagList="tagList"/>
  </div>
  <!-- Stars -->
  <div>
    <span class="text-xl">Stars in Videos by {{decodeURIComponent(this.$route.params.studioname)}}:</span>
    <span class="justify-right">({{starList.length}})</span>
    <StarList :starList="starList"/>
  </div>
  <!-- Videos -->
  <span class="text-xl">Videos by {{decodeURIComponent(this.$route.params.studioname)}}:  &nbsp;</span>
  <span class="justify-right">({{videoList.length}})</span>
  <div class="flex flex-wrap gap-x-6 gap-y-10 justify-center items-start">
      <template v-for="video in videoList" v-bind:key="video.id">
          <VideoDisplay :video="video"/>
      </template>
  </div>
</div>
</template>

<script>
import { postApi } from '@/api'
import VideoDisplay from '@/components/VideoDisplay'
import TagList from "../components/TagList";
import StarList from "../components/StarList";

export default {
    name: 'Studio',
    components: {
      VideoDisplay,
      TagList,
      StarList,
    },
    beforeMount() {
    postApi("/studio", {name: this.$route.params.studioname}, this.$store.state.jwt)
      .then(data => { this.videoList = data.videoList;
                      this.starList = data.starList;
                      this.tagList = data.tagList.sort((first, second) => first.ranking > second.ranking).map(tag => tag["_id"]);
                      console.log(data);})
    },
    data(){
        return {
            videoList: {},
            starList: {},
            tagList: {}
    }
    }
}
</script>
