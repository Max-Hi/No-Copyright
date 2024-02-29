<!-- https://github.com/horans/vue-nouislider.git -->

<template>
</template>

<script>
import noUiSlider from 'nouislider'
// import 'nouislider/dist/nouislider.css'

export default {
  name: "Slider",
  props: {
    'config': Object,
  },
  computed: {
    slider: function () {
      return document.getElementById('range')
    }
  },
  mounted() {
    noUiSlider.create(this.slider, this.config)
    this.slider.noUiSlider.on('update', function (values, handle) {
      // vnus.$emit('update', values)
      // if (vnus.log) window.console.log('[vnus]<' + handle + '>' + values)
      console.log(values[handle])
    })
  },
  // watch: {
  //   'value': function (nv) {
  //     if (this.init) {
  //       var nus = this.slider.noUiSlider.get()
  //       if (!Array.isArray(nus)) nus = [nus]
  //       if (JSON.stringify(nus) !== JSON.stringify(nv)) this.slider.noUiSlider.set(nv)
  //     } else {
  //       this.init = true
  //     }
  //   }
  // }
}
</script>