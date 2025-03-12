// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Homepage from '../components/Homepage.vue';
import Consult from '../components/Consult.vue';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Homepage,
    },
    {
        path: '/consult',
        name: 'Consultation',
        component: Consult,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
