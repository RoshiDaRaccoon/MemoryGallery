<script>
import DoorEntrance from '../assets/icons/door-entrance.svg?component'
import VkIcon from '../assets/icons/vk.svg?component'
export default {
    data() {
        return {
            isAdmin: localStorage.getItem('access_token'),
        }
    },
    components: {
        DoorEntrance,
        VkIcon
    }
}
</script>

<template>
    <footer class="footer py-4 mb-xl-0 mb-5">
        <div class="container mt-4 mb-4">
            <div class="row align-items-center gy-3">
                <div class="col-12 col-md-4 text-center text-md-start mt-0">
                    <div class="d-flex flex-column gap-1">
                        <a href="tel:+7(385-32)42-8-45" class="text-decoration-none text-dark fw-bold w-100">
                            +7 (385-32) 42-8-45
                        </a>
                        <a href="mailto:school-30@mail.ru" class="text-decoration-none text-muted small w-100">
                            school-30@mail.ru
                        </a>
                    </div>
                </div>

                <div class="col-12 col-md-4 text-center mt-0">
                    <a href="https://vk.com/publicschoolnumber30" target="_blank" class="vk-link">
                        <vk-icon width="2em" height="autho" />
                    </a>
                </div>

                <div class="col-12 col-md-4 text-center d-flex justify-content-end mt-0">
                    <RouterLink to="/admin" class="text-decoration-none title-link">
                        <button class="title-button d-flex align-items-center"><door-entrance width="2.6em" height="autho" />{{isAdmin ? "Панель администратора" : "Войти в систему"}}</button>
                    </RouterLink>
                </div>

            </div>
        </div>
    </footer>
</template>

<style scoped>
.footer {
    background-color: #E0EDAB;
    border-top: #3F2B4C 2px solid;
    min-height: 120px;
}

.vk-link {
    color: #000;
    transition: opacity 0.2s;
}

.vk-link:hover {
    opacity: 0.7;
}

.title-button {
    gap: 1rem;
    padding: 0.5em 3em;
    background-color: #E0EDAB;
    border: #3F2B4C 2px solid;
    border-radius: 3em;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    transition: transform 0.3s ease;

    &:hover {
        transform: scale(1.1);
    }
}

@media (max-width: 1200px) {
    .title-link {
        display: none;
    }
}
</style>