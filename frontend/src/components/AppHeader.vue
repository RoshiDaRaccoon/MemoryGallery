<script>
import { RouterLink } from 'vue-router'
export default {
    data() {
        return {
            logo: "favicon2.ico"
        }
    }
}
</script>

<template>
    <header>
        <nav class="fixed-top navbar navbar-expand-md">
            <div class="container justify-content-end">
                <div class="d-flex w-100 align-items-center justify-content-between">

                    <div class="links d-flex gap-4 justify-content-around align-items-center">
                        <RouterLink to="/gallery" class="navlink" href="#">Галерея</RouterLink>
                        <RouterLink to="/officials" class="navlink" href="#">Лица школы</RouterLink>
                    </div>

                    <div class="logo-holder">
                        <RouterLink to="/" class="navbar-brand mx-0 order-first order-0" href="#">
                            <img class="logo" :src="logo" alt="Logo">
                        </RouterLink>
                    </div>

                    <div class="links d-flex gap-4 justify-content-around align-items-center">
                        <RouterLink to="/about" class="navlink" href="#">О нас</RouterLink>
                        <RouterLink to="/contacts" class="navlink" href="#">Контакты</RouterLink>
                    </div>
                </div>
            </div>
        </nav>
    </header>
</template>

<style scoped>
.navbar {
    background: linear-gradient(rgba(63, 43, 76, 0.8), rgba(63, 43, 76, 0));
}

.logo {
    user-select: none;
    -webkit-user-drag: none;
    height: 100px;
    width: 100px;
}

.links {
    width: 40%;
}

.logo-holder {
    width: 20%;
    text-align: center;
}

.navlink {
    background-color: #3F2B4C;
    padding: 0 1em 0 1em;
    border-radius: 0.5em;
    font-weight: 600;
    font-size: 1.4rem;
    color: #F2ECDF;
    text-align: center;
    text-decoration: none;
    transition: all 0.3s ease-out;

    &:hover {
        text-decoration: underline;
        transition: all 0.3s;
    }
}

@media (max-width: 1200px) {
    .navbar {
        background-color: #3F2B4C;
        top: auto;
        bottom: 0;
    }

    .navlink {
        font-size: 0.9rem;
        background: none;
        padding: 0;
        border-radius: 0;
    }

    .logo {
        width: 50px;
        height: 50px;
    }

    .sm-text {
        font-size: 0.85rem;
    }
}
</style>