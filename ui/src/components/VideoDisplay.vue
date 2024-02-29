<template>
<div class="w-96 max-w-md">
  <div class="group">
    <!-- title -->
    <div class="flex flex-row">
      <a :href="'/watch/'+video.id" class="hover:underline group-hover:underline flex-grow truncate mb-2">{{video.title}}</a>
      <template v-if="video.rating !== -1">
          <template v-for="star in Array(parseInt(video.rating))" v-bind:key="star">
            <!--div>{{video.rating}}</div-->
            <div class="material-icons w-5" :id="star">star_rate</div>
        </template>
        <template v-if="0 !== parseInt(video.rating)-video.rating">
          <div class="material-icons w-5">star_half</div>
        </template>
      </template>
      <template v-else>
          <div class="material-icons">star_outline</div>
      </template>
    </div>

    <!-- image -->
    <div class="relative">
      <a :href="'/watch/'+video.id">
        <img class="w-full rounded-2xl"
             :src="staticFilesHostname+'/pictures/thumbnails/'+video.id+'.jpg'" >
      </a>
      <div class="absolute bottom-0 right-0 px-2 py-1 bg-black bg-opacity-50 rounded-tl-md rounded-br-2xl">
        {{video.views}} views &middot;
        {{parseInt(video.length*video.playback_position/60)}} / {{ parseInt(video.length/60) }} min
      </div>
    </div>
  </div>

  <VideoInfo :video="video" class="mt-2"/>
</div>
</template>

<script>
import VideoInfo from "./VideoInfo";
export default {
    name: "VideoDisplay",
  components: {VideoInfo},
  props: {
        video: {
            type: Object,
            default() {
                return {};
            }
        }
    },
    data() {
        return {

        }
    },
}
</script>

<style>
</style>
