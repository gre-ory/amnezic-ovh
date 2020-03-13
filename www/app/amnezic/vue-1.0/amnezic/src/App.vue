<template>
  <div id="app" class="small-container">
    <h1>Musics</h1>

    <music-table :musics="musics"/>
  </div>
</template>

<script>
import MusicTable from '@/components/MusicTable.vue'

export default {
  name: 'app',
  components: {
    MusicTable
  },
  data () {
    return {
      musics: []
    }
  },

  mounted () {
    this.getMusics()
  },

  methods: {

    async getMusics () {
      try {
        const response = await fetch('http://server.amnezic.com/amnezic/music')
        const json = await response.json()
        console.log(json)
        console.log(json.data.musics)
        this.musics = json.data.musics
      } catch (error) {
        console.error(error)
      }
    }
  }

}
</script>

<style>
  button {
    background: #009435;
    border: 1px solid #009435;
  }

  .small-container {
    max-width: 680px;
  }
</style>
