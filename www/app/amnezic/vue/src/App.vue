<template>
  <v-app>
    
    <!-- header -->
    
    <v-app-bar app color="blue-grey" class="white--text">
      <router-link to="/">
        <v-btn depressed small color="blue-grey" class="white--text">
          <v-icon>mdi-star</v-icon>
          Start
        </v-btn>
      </router-link> 
      <router-link to="/players">
        <v-btn depressed small color="blue-grey" class="white--text">
          <v-icon>mdi-account-group</v-icon>
          Players
        </v-btn>
      </router-link> 
      <router-link to="/set-up">
        <v-btn depressed small color="blue-grey" class="white--text">
          <v-icon>mdi-tune</v-icon>
          Set-up
        </v-btn>
      </router-link>
      <router-link to="/question/1">
        <v-btn depressed small color="blue-grey" class="white--text">
          <v-icon>mdi-music</v-icon>
          Quiz
        </v-btn>
      </router-link>
      <router-link to="/score">
        <v-btn depressed small color="blue-grey" class="white--text">
          <v-icon>mdi-podium</v-icon>
          Score
        </v-btn>
      </router-link>
    </v-app-bar>
    
    <!-- content -->
    
    <v-content>
      <router-view></router-view>
    </v-content>
    
    <!-- footer -->
    
    <v-footer app color="blue-grey" class="white--text">
      <span>AmneZic</span>
      <v-spacer></v-spacer>
      <span>&copy; 2020</span>
    </v-footer>
    
  </v-app>
  
</template>

<script>


export default {
  name: 'App',

  components: {
  },

  data: () => ({
    showScore: false,
    players: [{
      icon: 'mdi-account-box',
      name: 'Player 1',
      score: 0
    },{
      icon: 'mdi-star',
      name: 'Player 2',
      score: 0
    }]         
  }),
};
</script>
