import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import ContactsView from '@/views/ContactsView.vue'
import OfficialsView from '@/views/OfficialsView.vue'
import GalleryView from '@/views/GalleryView.vue'
import LoginView from '@/views/LoginView.vue'
import AdminView from '@/views/AdminView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        { path: '/', component: HomeView },
        { path: '/about', component: AboutView },
        { path: '/contacts', component: ContactsView },
        { path: '/gallery', component: GalleryView },
        { path: '/officials', component: OfficialsView },
        {
            path: '/login',
            component: LoginView,
            meta: { hideFooter: true }
        },
        {
            path: '/admin',
            component: AdminView,
            meta: {
                requiresAuth: true,
                hideFooter: true
            }
        },
    ],

    scrollBehavior(to, from, savedPosition) {
        return { top: 0 }
    }
})

router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('access_token');

    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login'); // Если нет токена — на логин
    } else {
        next(); // Иначе пропускаем
    }
})

export default router