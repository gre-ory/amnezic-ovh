import Vue from 'vue'
import VueRouter from 'vue-router'
import vuetify from './plugins/vuetify'
import 'vuetify/dist/vuetify.min.css'
import store from "./plugins/store";

import App from './App.vue'
import Start from './components/Start'
import Players from './components/Players'
import SetUp from './components/SetUp'
import Question from './components/Question'
import Score from './components/Score'

Vue.config.productionTip = false

//
// vue-router
//

Vue.use(VueRouter)
const routes = [
  { path: '/', component: Start },
  { path: '/players', component: Players },
  { path: '/set-up', component: SetUp },
  { path: '/question/:id', component: Question },
  { path: '/score', component: Score }
]
const router = new VueRouter({
  routes: routes
})

//
// vue
//

new Vue({
  vuetify,
  router,
  store,
  render: h => h(App)
}).$mount('#app')
