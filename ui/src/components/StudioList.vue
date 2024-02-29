<template>
  <div class="flex flex-wrap gap-x-5 gap-y-1 justify-center items-start">
    <template v-for="studio in studioList" v-bind:key="studio">
      <div>
        <a :href="'/studio/'+encodeURIComponent(studio._id)" class="bg-red-800 border border-black rounded-lg px-1">{{studio._id}}</a>
      </div>
    </template>
  </div>
</template>


<script>


export default {
    name: "StudioList",
    props: {
        studioList: {
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