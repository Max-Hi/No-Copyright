<template>
<div>
<p class="my-4">
  <!-- Search -->
  <span class="underline cursor-pointer" @click="search">Search</span>
  for videos by 
  <!-- title -->
  <input class="text-black p-1 rounded border-2 ml-2" placeholder="Title" v-model="titleSearch">
</p>
<div class="flex flex-col space-y-3 items-start">

  <!-- tags -->
  <div class="flex flex-row space-x-2 w-full">
    <button class="flex-grow w-8" @click="toggleJunktor('tags')">{{ junktoren["tags"] }}</button>
    <input class="text-black w-full p-1 rounded border-2" placeholder="tags" v-model="tagSearch">
  </div>

  <!-- studios -->
  <div class="flex flex-row space-x-2 w-full">
    <button class="flex-grow w-8" @click="toggleJunktor('studios')">{{ junktoren["studios"] }}</button>
    <input class="text-black w-full p-1 rounded border-2" placeholder="studios" v-model="studioSearch">
  </div>

  <!-- stars -->
  <div class="flex flex-row space-x-2 w-full">
    <button class="flex-grow w-8" @click="toggleJunktor('stars')">{{ junktoren["stars"] }}</button>
    <input class="text-black w-full p-1 rounded border-2" placeholder="stars" v-model="starSearch">
  </div>

  <div class="flex flex-wrap justify-center gap-2 w-full items-center">
    <div class="w-32">
      <label>Length</label>
      <div class="m-2">
      <Slider v-model="length"
      :min="0"
      :max="70"/>
      </div>
    </div>
    <div class="w-32">
      <span>Resolution</span>
      <div class="m-2">
      <Slider v-model="minResolution" 
      :min="0"
      :max="3840"/>
      </div>
    </div>
    <div class="w-32">
      <span>Watched</span>
      <div class="m-2">
      <Slider v-model="watched" />
      </div>
    </div>
    <div class="w-32">
      <span>Rating</span>
      <div class="m-2">
      <Slider v-model="minRating" 
      :min="0"
      :max="5"/>
      </div>
    </div>
    <div class="w-32">
      <!-- possible values: "length", "rating", "relevant", "none"-->
      <label for="sorting">Sort by</label>
      <select class="text-black w-full p-1 rounded border-2" v-model="sorting" id="sorting">
        <option>length</option>
        <option>rating</option>
        <option>relevant</option>
        <option>none</option>
      </select>
    </div>
    <div>
      <label for="reversed" class="mr-1">reversed</label>
      <input type="checkbox" name="reversed" id="reversed" v-model="reversed">
    </div>
  </div>

</div>
</div>

<!--Search results-->
<div class="justify-center">
  <div v-if="videos.length===0">
    <span>No search results</span>
  </div>
  <div v-else>
    <span>{{videos.length}} results</span>
  </div>
  <div class="flex flex-wrap gap-x-6 gap-y-10 justify-center items-start">
  <template v-for="video in videos" v-bind:key="video.id">
    <VideoDisplay :video = "video"/>
  </template>
  </div>
</div>

</template>

<script>
import Slider from '@vueform/slider'
import { postSearch } from "@/api"
import VideoDisplay from '@/components/VideoDisplay'

export default {
  name: 'LandingPage',
  components: {
    Slider,
    VideoDisplay,
  },
  data() {
    return {
      tagSearch: "",
      studioSearch: "", 
      starSearch: "",
      titleSearch: "",
      junktoren: { tags: "and", studios: "and", stars: "and", title: "and"},
      length: [0,70],        // in minutes
      minResolution: 0, // in pixels (width)
      minRating: 0,
      watched: [0,100],       // in percentage
      sorting: "none",
      reversed: "reversed",
      videos: [],
      ratingConfig: {
        step: 1,
        range: {
          'min': 1,
          'max': 10,
        }
      },
      //barMaxValue: 0,
      //barMinValue: 0,
    }
  },
  methods: {
    search() {
      const tags    = (this.tagSearch !== "" ? this.tagSearch.split("; ") : [])
      const stars   = (this.starSearch !== "" ? this.starSearch.split("; ") : [])
      const studios = (this.studioSearch !== "" ? this.studioSearch.split("; ") : [])
      const lengthmin = this.length[0]*60
      var lengthmax = this.length[1]*60
      if(lengthmax==4200){
        lengthmax = 30000
      }
      console.log({
                   title:         this.titleSearch,
                   tags:          tags, 
                   stars:         stars, 
                   studios:       studios, 
                   length:        [lengthmin,lengthmax],
                   watched:       this.watched.map((x)=>x/100),
                   minResolution: Number(this.minResolution), 
                   minRating:     Number(this.minRating), 
                   sorting:       this.sorting,
                   reversed:      Boolean(this.reversed),
                   junktoren:     this.junktoren,
                 })
      postSearch({
                   title:         this.titleSearch,
                   tags:          tags, 
                   stars:         stars, 
                   studios:       studios, 
                   length:        [lengthmin,lengthmax],
                   watched:       this.watched.map((x)=>x/100),
                   minResolution: Number(this.minResolution), 
                   minRating:     Number(this.minRating), 
                   sorting:       this.sorting,
                   reversed:      Boolean(this.reversed),
                   junktoren:     this.junktoren,
                 },
                 this.$store.state.jwt)
        .then(response => response.json())
        .then(data => {console.log(data); this.videos = data})        
    },
    toggleJunktor(field) {
       this.junktoren[field] = (this.junktoren[field] === "and" ? "or" : "and")
    },
  },
  mounted() {
    postSearch({
                   title:         "",
                   tags:          [], 
                   stars:         [], 
                   studios:       [], 
                   length:        [200,3000],
                   watched:       [0,0],
                   minResolution: 0, 
                   minRating:     0, 
                   sorting:       "none",
                   reversed:      false,
                   junktoren:     {tags: "and", studios: "and", stars: "and"},
                 },
                 this.$store.state.jwt)
        .then(response => response.json())
        .then(data => {console.log(data); this.videos = data.slice(0,8)})       
    },
  async created() {}
}
</script>

<style src="@vueform/slider/themes/default.css"></style>
