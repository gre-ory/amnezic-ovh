<template>
  <div id="tag-table">
    <table>
      <thead>
        <tr>
          <th>Id</th>
          <th>Name</th>
          <th>Number of musics</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="tag in tags" :key="tag.id">
          <td>{{ tag.id }}</td>
          <td>{{ tag.name }}</td>
          <td>{{ tab.nb }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'tag-table',
  props: {
    tags: Array
  }
}
</script>

<style scoped></style>
