import Vue from "vue";
import Vuex from "vuex";
 
Vue.use(Vuex);
 
export default new Vuex.Store({
 state: {
    players: [ 
        {
            id: 1,
            name: 'Player 1',
            active: true,
            score: 0
        },
        {
            id: 2,
            name: 'Player 2',
            active: false,
            score: 0
        }
    ],
    setUp: {
        nbQuestion: 10,
        nbAnswer: 6,
        tags: []
    },
    game: null
 },
 getters: {     
    firstPlayer: state => {
        return state.players.length > 0 ? state.players[0] : null;
    },    
    secondPlayer: state => {
        return state.players.length > 1 ? state.players[1] : null;
    },    
    thirdPlayer: state => {
        return state.players.length > 2 ? state.players[2] : null;
    },    
    otherPlayers: state => {
        return state.players.length > 3 ? state.players.slice(3) : [];
    }
 },
 mutations: {
    addPlayer(state) {
        state.players.push({
            id: (state.players.length + 1),
            name: 'Player ' + (state.players.length + 1),
            active: true,
            score: 0
        });
    },
    updateName(state, data) {
        console.log(`[store] update name to ${data.name} for player ${data.playerId}`);
        var player = state.players.find( p => p.id == data.playerId );
        player.name = data.name;
    },
    updateScore(state, data) {
        console.log(`[store] update score to ${data.score} for player ${data.playerId}`);
        var player = state.players.find( p => p.id == data.playerId );
        player.score = data.score;
        this.sortPlayers(state);
    },
    updateStatus(state, data) {
        console.log(`[store] update status to ${data.active} for player ${data.playerId}`);
        var player = state.players.find( p => p.id == data.playerId );
        player.active = data.active;
    },
    sortPlayers (state) {
        state.players.sort(function(a, b){return a.score-b.score})
    }
 },
 actions: {}
});
