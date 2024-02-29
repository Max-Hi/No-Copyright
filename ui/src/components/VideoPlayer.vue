<template>
<div>
    <video ref="videoPlayer" class="video-js vjs-big-play-centered"></video>
</div>
</template>

<script>
import videojs from 'video.js';

export default {
    name: "VideoPlayer",
    props: {
        url: {
            type: String,
            default() {
                return "";
            }
        }
    },
    data() {
        return {
            player: null
        }
    },
    mounted() {
        const options = {
            autoplay: false, controls: true,
            sources: [ { src: this.url, type: "video/mp4" } ],
            preload: "auto",
            fluid: true,
        } 
        console.log("url", this.url)
            
        this.player = videojs(this.$refs.videoPlayer, options, function onPlayerReady() {
            console.log('onPlayerReady', this);
        })
    },
    beforeUnmount() {
        if (this.player) {
            this.player.dispose()
        }
    }
}
</script>

<style>
</style>
