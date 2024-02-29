<template>
  <div>
    <div>Videos from your Favourites</div>
    <div class="justify-center">
      <div class="flex flex-wrap gap-x-6 gap-y-10 justify-center items-start">
      <template v-for="video in videos" v-bind:key="video.id">
        <VideoDisplay :video = "video"/>
      </template>
      </div>
    </div>
    <div>Your Playlists</div>
    <div>Continue Watching</div>
    <div class="justify-center">
      <div class="flex flex-wrap gap-x-6 gap-y-10 justify-center items-start">
      <template v-for="video in videos_continue" v-bind:key="video.id">
        <VideoDisplay :video = "video"/>
      </template>
      </div>
    </div>
    <div>Your Favourites:</div> <!--tags, stars, studios-->
  </div>
</template>


<script>
import VideoDisplay from '@/components/VideoDisplay'
import { postSearch } from "@/api"

export default {
    name: 'Personal',
    components: {
      VideoDisplay
    },
    /*beforeMount() {
    postPersonalInfo(username, this.$store.state.jwt)
      .then(data => { this.userinfo = data;
                      console.log(data) })
    },*/
    data(){
        return {
          videos: [],
          videos_continue: [],
          // userinfo,
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
    }
    },
    mounted() {
        postSearch({
                   title:         "",
                   tags:          [], 
                   stars:         [], 
                   studios:       [], 
                   length:        [200,3000],
                   watched:       [0.95,1],
                   minResolution: 0, 
                   minRating:     4, 
                   sorting:       "none",
                   reversed:      false,
                   junktoren:     {tags: "and", studios: "and", stars: "and"},
                 },
                 this.$store.state.jwt)
        .then(response => response.json())
        .then(data => {console.log(data); this.videos = data.slice(0,8)})
        postSearch({
                   title:         "",
                   tags:          [], 
                   stars:         [], 
                   studios:       [], 
                   length:        [200,3000],
                   watched:       [0.1,0.95],
                   minResolution: 0, 
                   minRating:     0, 
                   sorting:       "none",
                   reversed:      false,
                   junktoren:     {tags: "and", studios: "and", stars: "and"},
                 },
                 this.$store.state.jwt)
        .then(response => response.json())
        .then(data => {console.log(data); this.videos_continue = data.slice(0,8)})          
    },
}
</script>
