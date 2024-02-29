<template>
<div class="flex flex-col space-y-1">
  <!-- studios -->
  <div v-if="video.studios.length !== 0"
       class="flex flex-wrap gap-x-1 w-full max-h-7 truncate" >
    <span>Produced by</span>
    <template v-for="studio in video.studios" v-bind:key="studio" >
      <a :href = "'/studio/'+encodeURIComponent(studio)" class="bg-red-800 border border-black rounded-lg px-1">{{studio}}</a>
    </template>
  </div>

  <!-- stars -->
  <div v-if="video.stars.length !== 0"
       class="flex flex-wrap gap-x-1 w-full max-h-7 truncate" >
    <span>Starring</span>
    <template v-for="star in video.stars" v-bind:key="star">
      <a :href = "'/star/'+encodeURIComponent(star)" class="bg-red-800 border border-black rounded-lg px-1">{{star}}</a>
    </template>
  </div>

  <!-- tags -->
<div v-if="video.tags.length !== 0" class="flex flex-wrap gap-x-1 gap-y-1 w-full max-h-14 truncate">
    <span>Including</span>
    <template v-for="tag in sort_tags(video.tags)" v-bind:key="tag">
      <a :href = "'/tag/'+encodeURIComponent(tag)" class="bg-red-800 border border-black rounded-lg px-1">{{tag.name}}</a>
    </template>
  </div>
</div>
</template>

<script>
export default {
  name: "VideoInfo",
  props: {
        video: {
            type: Object,
            default() {
                return {studios: [], stars: [], tags: []};
            }
        }
    },
    methods: {
      sort_tags(tags){
        return tags
      }
    },
}
</script>

<style scoped>

</style>
