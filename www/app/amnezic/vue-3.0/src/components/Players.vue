<template>
  <div id="player-table">
    <table>
      <tbody>
        <tr v-for="player in players" :key="player.id">
          <td>
            <v-switch :value="true" :input-value="player.active" @change="updateStatus(player.id,$event)"></v-switch>
          </td>
          <td>
            <v-text-field id="playerName" label="Name" :value="player.name" @change="updateName(player.id,$event)" :rules="nameRules"></v-text-field>
          </td>
          <td>
            <v-icon>mdi-podium</v-icon> - {{ player.score }}
          </td>
        </tr>
        <tr>
          <v-btn v-on:click="addPlayer" depressed small color="blue-grey" class="white--text">
            <v-icon>mdi-account-plus</v-icon>
            Add
          </v-btn>
        </tr>
      </tbody>
    </table>
  </div>

</template>

<script>
export default {
  name: 'player-table',
  data() {
      return {
          players: null,
          nameRules: [
            value => !!value || 'Required.',
            value => (value || '').length <= 20 || 'Max 20 characters',
            value => {
              const pattern = /^[a-zA-Z0-9_ -]+$/
              return pattern.test(value) || 'Only alpha-numeric values.'
            },
          ]
      };
  },
  mounted () {
    this.players = this.$store.state.players;
  },
  methods: {
    updateStatus: function (playerId,event) {
      console.log(`updateStatus - ${playerId} - ${event}`);
      this.$store.commit("updateStatus",{playerId:playerId,active:(event!==null)});
    },
    updateName: function(playerId,event) {
      console.log(`updateName - ${playerId} - ${event}`);
      this.$store.commit("updateName",{playerId:playerId,name:event});
    },
    addPlayer: function () {
      this.$store.commit("addPlayer");
    }
  }
}
</script>

<style scoped></style>
