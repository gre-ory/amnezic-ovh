<template>
  <div id="app" class="small-container">
    <h1>Musics</h1>

    <music-table :musics="musics"/>
  </div>
</template>

<script>
import MusicTable from '@/components/MusicTable.vue'
import TagTable from '@/components/TagTable.vue'

export default {
  name: 'app',
  components: {
    MusicTable,
    TagTable
  },
  data () {
    return {
      musics: [],
      tags: [],
      game: null
    }
  },

  mounted () {
    this.getMusics(),
    this.getTags()
  },

  methods: {

    async getMusics () {
      try {
        const response = await fetch('http://server.amnezic.com/amnezic/music')
        const json = await response.json()
        this.musics = json.data.musics
      } catch (error) {
        console.error(error)
      }
    },
    
    async getTags () {
      try {
        const response = await fetch('http://server.amnezic.com/amnezic/tag')
        const json = await response.json()
        this.tags = json.data.tags
      } catch (error) {
        console.error(error)
      }
    },
    
    async getGame () {
      try {
        const response = await fetch('http://server.amnezic.com/amnezic/game')
        const json = await response.json()
        this.game = json.data.game
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