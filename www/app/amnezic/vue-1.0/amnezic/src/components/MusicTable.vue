<template>
  <div id="music-table">
    <table>
      <thead>
        <tr>
          <th>Id</th>
          <th>Title</th>
          <th>Artist</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="music in musics" :key="music.id">
          <td>{{ music.id }}</td>
          <td>{{ music.title }}</td>
          <td>{{ music.artist }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'music-table',
  props: {
    musics: Array
  }
}
</script>

<style scoped></style>
