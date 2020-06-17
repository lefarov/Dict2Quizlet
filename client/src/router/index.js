import Vue from 'vue';
import Router from 'vue-router';
import Ping from '../components/Ping.vue';
import Books from '../components/Books.vue';
import Dict from '../components/Dict.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Dict',
      component: Dict,
    },
    {
      path: '/books',
      name: 'Books',
      component: Books,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});
