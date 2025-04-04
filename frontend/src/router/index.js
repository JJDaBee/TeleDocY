import { createRouter, createWebHistory } from 'vue-router';
import Homepage from '../components/Homepage.vue';
import Consult from '../components/Consult.vue';
import payment from '../components/payment.vue';
import doctorOrder from '../components/doctorOrder.vue';
import SymptomChecker from '../components/SymptomChecker.vue'; 

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
    {
        path: '/payment',
        name: 'Payment',
        component: payment,
    },
    {
        path: '/doctorOrder',
        name: 'DoctorOrder',
        component: doctorOrder,
    },
    {
        path: '/symptom-checker',
        name: 'SymptomChecker',
        component: SymptomChecker,
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
