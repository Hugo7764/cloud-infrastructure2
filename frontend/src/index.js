import { createRouter, createWebHistory } from 'vue-router';
import { getToken } from './auth';
import Accueil from './views/Accueil.vue';
import Classement from './views/Classement.vue';
import Calendrier from './views/Calendrier.vue';
import Login from './views/Login.vue';
import AdminDashboard from './views/AdminDashboard.vue';
import AjouterMatch from './views/AjouterMatch.vue';
import EditMatch from './views/EditMatch.vue';
import ListeEquipe from './views/ListeEquipe.vue';
import AjouterEquipe from './views/AjouterEquipe.vue';

const routes = [
    { path: '/', component: Accueil },
    { path: '/classement', component: Classement },
    { path: '/calendrier', component: Calendrier },
    { path: '/login', component: Login },
    { path: '/admin', component: AdminDashboard, meta: { requiresAuth: true } },
    { path: '/ajouter-match', component: AjouterMatch, meta: { requiresAuth: true } },
    { path: '/edit-match/:id', component: EditMatch, meta: { requiresAuth: true } },
    { path: '/liste-equipes', component: ListeEquipe, meta: { requiresAuth: true } },
    { path: '/ajouter-equipe', component: AjouterEquipe, meta: { requiresAuth: true } },
    { path: '/:pathMatch(.*)*', redirect: '/' }
];


const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth && !getToken()) {
        next('/login');
    } else {
        next();
    }
});

export default router;
