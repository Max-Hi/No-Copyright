<template>
  <div class="flex flex-wrap gap-x-5 gap-y-1 justify-center items-start">
    <template v-for="star in starList" v-bind:key="star">
      <div>
        <a :href="'/star/'+encodeURIComponent(star._id)" class="bg-red-800 border border-black rounded-lg px-1">{{star._id}}</a>
      </div>
    </template>
  </div>
</template>


<script>


export default {
    name: "StarList",
    props: {
        starList: {
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