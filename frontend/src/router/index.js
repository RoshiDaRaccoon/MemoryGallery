import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import AboutPage from '@/pages/AboutPage.vue'
import ContactsPage from '@/pages/ContactsPage.vue'
import OfficialsPage from '@/pages/OfficialsPage.vue'
import GalleryPage from '@/pages/GalleryPage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import AdminPage from '@/pages/AdminPanel.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        { path: '/', component: HomePage },
        { path: '/about', component: AboutPage },
        { path: '/contacts', component: ContactsPage },
        { path: '/gallery', component: GalleryPage },
        { path: '/officials', component: OfficialsPage },
        {
            path: '/login',
            component: LoginPage,
            meta: { hideFooter: true }
        },
        {
            path: '/admin',
            component: AdminPage,
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