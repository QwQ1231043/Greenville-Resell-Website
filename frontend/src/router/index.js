// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue';
import Setting from '../components/Setting.vue';
import MerchandiseList from '../components/post-merchandise.vue';
import register from '../components/register.vue'
import login from '../components/login.vue'
import post_merchandise from '../components/post-merchandise.vue'
import Like from '../components/Like.vue'
import merchandise_detail from '../components/merchandise_detail.vue'
import my_merchandise from '../components/my_merchandise.vue'
import edit_merchandise from '../components/edit_merchandise.vue'
import message from '../components/message.vue'
import message_detail from '../components/message_detail.vue'
import donation from '../components/donation.vue'
import reset_password from '../components/reset_password.vue'
const routes = [
  { path: '/', component: Home },
  { path: '/home', component: Home },
  { path: '/setting', component: Setting },
  { path: '/merchandise', component: MerchandiseList },
      { path: '/register', component: register },
      { path: '/login', component: login },
    {path:'/post-merchandise',component:post_merchandise},
    {path:'/Like',component: Like},
    {path:'/merchandise_detail/:id',component: merchandise_detail,name:"MerchandiseDetail"},
    {path:'/my_merchandise',component:my_merchandise},
  {path:'/edit-merchandise/:id',component: edit_merchandise},
  {path:'/message',component: message},
  {path:"/message/:id/:username",component: message_detail,name:"MessageDetail"},
  {path:'/donation',component: donation},
  {path:'/reset_password',component: reset_password}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
