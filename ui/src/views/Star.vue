<template>
    <div class="flex flex-col space-y-4">

    <div class="text-3xl">{{decodeURIComponent(this.$route.params.starname)}}</div>
    <!-- Studios -->
      <div>
        <span class="text-xl">Studios working with {{decodeURIComponent(this.$route.params.starname)}}:  &nbsp;</span>
        <span class="justify-right">({{studioList.length}})</span>
        <StudioList :studioList="studioList"/>
      </div>
    <!-- Tags -->
      <div>
        <span class="text-xl">Typical tags of {{decodeURIComponent(this.$route.params.starname)}}:  &nbsp;</span>
        <span class="justify-right">({{tagList.length}})</span>
        <TagList :tagList="tagList"/>
      </div>
    <!-- Videos -->
    <span class="text-xl">Videos with {{decodeURIComponent(this.$route.params.starname)}}:  &nbsp;</span>
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
import StudioList from "../components/StudioList";
import TagList from "../components/TagList";

export default {
    name: 'Star',
    components: {
      VideoDisplay,
      TagList,
      StudioList,
    },
    beforeMount() {
    postApi("/star", {name: this.$route.params.starname}, this.$store.state.jwt)
      .then(data => { this.videoList = data.videoList;
                      this.tagList = data.tagList.sort((first, second) => first.ranking > second.ranking).map(tag => tag["_id"]);
                      this.studioList = data.studioList;
                      console.log(data) })
    },
    data(){
        return {
            videoList: {},
            tagList: {},
            studioList: {}
    }
    }
}
</script>
