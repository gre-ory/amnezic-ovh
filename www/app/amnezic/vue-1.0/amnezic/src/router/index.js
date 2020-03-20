import Vue from 'vue'
import Router from 'vue-router'
import MusicTable from '@/components/MusicTable'
import TagTable from '@/components/TagTable'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/musics',
      name: 'MusicTable',
      component: MusicTable
    },
    {
      path: '/tags',
      name: 'TagTable',
      component: TagTable
    }
  ]
})
