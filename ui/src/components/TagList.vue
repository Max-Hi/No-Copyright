<template>
  <div class="flex flex-wrap gap-x-5 gap-y-1 justify-center items-start">
    <template v-for="tag in tagList" v-bind:key="tag">
      <div>
        <a :href="'/studio/'+encodeURIComponent(tag._id)" class="bg-red-800 border border-black rounded-lg px-1">{{tag._id}}</a>
      </div>
    </template>
  </div>
</template>


<script>


export default {
    name: "TagList",
    props: {
        tagList: {
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
    beforeMount() {
       console.log(this.tagList)
    }
}
</script>

<style>
</style>