<template>
<div>
  <div class="flex flex-row mt-6">
      <div class="flex-grow mb-4 text-lg">{{videoInfo.title}}</div>
      <template v-if="videoInfo.rating !== -1">
          <template v-for="star in Array(parseInt(videoInfo.rating))" v-bind:key="star">
            <!--div>{{video.rating}}</div-->
            <div class="material-icons w-5" :id="star">star_rate</div>
        </template>
        <template v-if="0 !== parseInt(videoInfo.rating)-videoInfo.rating">
          <div class="material-icons w-5">star_half</div>
        </template>
      </template>
      <template v-else>
          <div class="material-icons">star_outline</div>
      </template>
    </div>
  <VideoPlayer :url="staticFilesHostname+'/videos/'+id+'.mp4'" class="mb-5"/>
  <VideoInfo :video="videoInfo" />
  <div class="flex flex-row place-content-between mt-2">
    <div>Resolution {{videoInfo.resolution[0]}}x{{videoInfo.resolution[1]}}</div>
    <div> {{videoInfo.views}} views &middot;
        {{parseInt(videoInfo.length*videoInfo.playback_position/60)}} / {{ parseInt(videoInfo.length/60) }} min</div>
  </div>
</div>

<div>
  <p class="my-4">
  <!-- Edit Metadata -->
  <span class="underline cursor-pointer" @click="submitMetadata">Edit</span>
  Metadata for video titled: </p><p class="m-2">
  <!-- title -->
  <input class="text-black p-1 w-full rounded border-2" placeholder="New Title" v-model="newTitle">
</p>
<p class="m-2">
  <!-- tags -->
  <input class="text-black p-1 w-full rounded border-2" placeholder="New Tags" v-model="newTags">
</p>
<p class="m-2">
  <!-- studios -->
  <input class="text-black p-1 w-9/12 rounded border-2" placeholder="New Studios" v-model="newStudios">
  <!-- playbackpostion -->
  <input class="text-black p-1 w-3/12 rounded border-2 ml-auto" placeholder="New Playback Position" v-model="newPlaybackPosition">
</p>
<p class="m-2">
  <!-- stars -->
  <input class="text-black p-1 w-9/12 rounded border-2" placeholder="New Stars" v-model="newStars">
  <!-- rating -->
  <input class="text-black p-1 w-3/12 rounded border-2 ml-auto" placeholder="New Rating" v-model="newRating">
</p>
</div>

<!-- deletion -->
<div>
<span class="underline cursor-pointer" @click="deletevid">Delete</span>
</div>

</template>


<script>
import VideoPlayer from '@/components/VideoPlayer'
import VideoInfo from "../components/VideoInfo"
import { postApi } from "@/api";

export default {
  name: 'WatchVideo',
  components: {
    VideoInfo,
    VideoPlayer,
  },
  data() {
    return {
      videoInfo: {
        rating: 0,
        title: "",
        resolution: [0,0],
        views: 0,
        length: 0,
        playback_position: 0,
      },
      newTitle: "",
      newStars: "",
      newStudios: "", 
      newTags: "",
      newPlaybackPosition: "",
      newRating: ""
    }
  },
  computed: {
    id: function() {
      return this.$route.params.id
    }
  },
  beforeMount() {
    postApi("/video", {id: this.$route.params.id}, this.$store.state.jwt)
      .then(data => { this.videoInfo = data; console.log(data) })
  },
  methods: {
    submitMetadata(){
      let globalTagShare = true
      let newTags    = (this.newTags !== "" ? this.newTags.split("; ") : [])
      if (this.newTags.charAt(0) === "/") {
        globalTagShare = false
        newTags    = (this.newTags.substring(1) !== "" ? this.newTags.substring(1).split("; ") : [])
      }
      const newStars   = (this.newStars !== "" ? this.newStars.split("; ") : [])
      const newStudios = (this.newStudios !== "" ? this.newStudios.split("; ") : [])

      postApi("/metadata", {
                    id:                   this.$route.params.id,
                    newTitle:             this.newTitle, 
                    newStars:             newStars, 
                    newStudios:           newStudios, 
                    newTags:              newTags, 
                    newPlaybackPosition:  this.newPlaybackPosition, 
                    newRating:            this.newRating, 
                    globalTagShare:       globalTagShare},
                  this.$store.state.jwt)
        .then(data => {this.$router.go(); console.log(data)})
    },
    deletevid(){
      if(confirm("Confirmation: ")){
        postApi("/delete", {id: this.$route.params.id}, this.$store.state.jwt)
        .then(() => this.$router.push('/'))
      }
    },
    // URLencode: function(){
    //   this.result = encodeURIComponent('string');
    // }
  }
}
</script>
