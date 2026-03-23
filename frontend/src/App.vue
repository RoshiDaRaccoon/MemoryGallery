<script>
import { RouterView } from 'vue-router'
import AppHeader from './components/AppHeader.vue';
import HomePage from './components/HomePage.vue';
import AppFooter from './components/AppFooter.vue';

export default {
    components: {
        AppHeader,
        HomePage,
        AppFooter
    }
}
</script>

<template>
    <app-header />
    <RouterView />
    <app-footer v-if="!$route.meta.hideFooter" />
</template>

<style scoped>
* {
    font-family: 'Rubik', sans-serif;
}
</style>