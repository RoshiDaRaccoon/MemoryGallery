<template>
    <div class="page-container d-flex justify-content-center align-items-center">
        <img class="page-bg" src="/image.png" alt="">
        <div class="info-card p-5 text-center">
            <h1 class="mb-4">Контакты</h1>
            <div class="d-flex flex-column gap-3 fs-5">
                <p><strong>Адрес:</strong> г. Новоалтайск, ул. Примерная, д. 30</p>
                <p><strong>Телефон:</strong> <a href="tel:+73853242845" class="text-white">+7 (385-32) 42-8-45</a></p>
                <p><strong>E-mail:</strong> school-30@mail.ru</p>
                <p><strong>Мы в ВК:</strong> <a href="https://vk.com" class="text-white" target="_blank">://vk.com</a>
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.page-container {
    height: 100vh;
    color: #F2ECDF;
}

.page-bg {
    position: fixed;
    width: 100vw;
    height: 100vh;
    object-fit: cover;
    filter: brightness(40%);
    z-index: -1;
}

.info-card {
    background: rgba(63, 43, 76, 0.85);
    border: 2px solid #E0EDAB;
    border-radius: 30px;
    max-width: 40vw;
    backdrop-filter: blur(5px);
}
</style>