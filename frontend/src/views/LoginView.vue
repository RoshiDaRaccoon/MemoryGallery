<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api'; // Настроенный axios

const isCheckingStatus = ref(true); // Флаг для самой первой проверки
const isInitialized = ref(true); // По умолчанию считаем, что админ есть

const masterKey = ref('');       // Для первого админа
const firstName = ref('');       // Для первого админа
const lastName = ref('');        // Для первого админа

const email = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);
const router = useRouter();

const showPassword = ref(false);
const showMasterKey = ref(false);

const togglePassword = () => showPassword.value = !showPassword.value;
const toggleMasterKey = () => showMasterKey.value = !showMasterKey.value;

const passwordValidation = computed(() => {
    if (isInitialized.value) return { valid: true }; // Для входа проверку не делаем

    const p = password.value;
    const hasDigit = /\d/.test(p);
    const hasUpper = /[A-Z]/.test(p);
    const hasLower = /[a-z]/.test(p);
    const minLength = p.length >= 8;

    return {
        hasDigit,
        hasUpper,
        hasLower,
        minLength,
        valid: hasDigit && hasUpper && hasLower && minLength
    };
});

const isFormValid = computed(() => {
    if (isInitialized.value) return email.value && password.value;

    return (
        firstName.value &&
        lastName.value &&
        email.value &&
        passwordValidation.value.valid &&
        masterKey.value
    );
});

onMounted(async () => {
    try {
        const res = await api.get('/auth/check-init');
        isInitialized.value = res.data.is_initialized;
    } catch (err) {
        console.error("Ошибка проверки системы");
    } finally {
        // Убираем загрузку в любом случае
        isCheckingStatus.value = false;

        // Фокусируемся с небольшой задержкой, когда DOM отрисовался
        setTimeout(() => {
            if (isInitialized.value) emailInput.value?.focus();
            else firstNameInput.value?.focus();
        }, 50);
    }
});

const handleAuth = async () => {
    loading.value = true;
    error.value = '';

    try {
        if (!isInitialized.value) {
            // РЕГИСТРАЦИЯ ПЕРВОГО АДМИНА
            const res = await api.post(`/auth/register/first?key=${masterKey.value}`, {
                first_name: firstName.value,
                last_name: lastName.value,
                email: email.value,
                password: password.value
            });
            localStorage.setItem('access_token', res.data.access_token);
            router.push('/admin');
        } else {
            // ОБЫЧНЫЙ ВХОД (твой старый код handleLogin)
            // OAuth2PasswordRequestForm на бэкенде ждет FormData (username/password)
            const formData = new FormData();
            formData.append('username', email.value);
            formData.append('password', password.value);
            const res = await api.post('/auth/login', formData);
            // Сохраняем access_token (refresh упадет в куки сам)
            localStorage.setItem('access_token', res.data.access_token);
            // Перенаправляем в админку
            router.push('/admin');
        }
    } catch (err) {
        error.value = err.response?.data?.detail || 'Ошибка операции';
    } finally {
        loading.value = false;
    }
};
</script>

<template>
    <div class="login-page d-flex align-items-center justify-content-center">
        <img class="login-page-image" src="/image.png" alt="">

        <div class="login-card p-5 shadow-lg text-center">
            <div v-if="isCheckingStatus" class="py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Загрузка...</span>
                </div>
                <p class="mt-3 text-muted">Проверка состояния системы...</p>
            </div>

            <div v-else>
                <!-- Динамический заголовок -->
                <h2 class="mb-4 fw-bold">
                    {{ isInitialized ? 'Вход в систему' : 'Создание админа' }}
                </h2>

                <form @submit.prevent="handleAuth">
                    <!-- Поля только для регистрации -->
                    <div v-if="!isInitialized" class="row mb-3">
                        <div class="col-6 text-start">
                            <label class="form-label">Имя</label>
                            <input v-model="firstName" type="text" class="form-control custom-input" required>
                        </div>
                        <div class="col-6 text-start">
                            <label class="form-label">Фамилия</label>
                            <input v-model="lastName" type="text" class="form-control custom-input" required>
                        </div>
                    </div>

                    <div class="mb-3 text-start">
                        <label class="form-label">Email</label>
                        <input v-model="email" type="email" class="form-control custom-input"
                            placeholder="admin@school.ru" required>
                    </div>

                    <!-- Поле Пароля -->
                    <div class="mb-3 text-start">
                        <label class="form-label">Пароль</label>
                        <div class="input-group">
                            <input v-model="password" :type="showPassword ? 'text' : 'password'"
                                class="form-control custom-input" placeholder="••••••••" required>
                            <button class="btn eye-btn" type="button" @click="togglePassword">
                                {{ showPassword ? '👁️‍🗨️' : '👁️' }}
                            </button>
                            <label v-if="!isInitialized" class="text-muted small">(более 8 символов, 1 заглавная и
                                цифра)</label>
                        </div>

                        <!-- Твои подсказки (Hints) из прошлого шага -->
                        <div v-if="!isInitialized && password.length > 0" class="mt-2 password-hints">
                            <small :class="passwordValidation.valid ? 'text-success' : 'text-muted'">
                                {{ passwordValidation.valid ? '✅ Пароль надежен' : '❌ Проверьте сложность' }}
                            </small>
                        </div>
                    </div>

                    <!-- Ключ только для регистрации -->
                    <div v-if="!isInitialized" class="mb-4 text-start">
                        <label class="form-label text-primary">Секретный ключ (Master Key)</label>
                        <div class="input-group">
                            <input v-model="masterKey" :type="showMasterKey ? 'text' : 'password'"
                                class="form-control custom-input border-primary" required>
                            <button class="btn btn-outline-primary eye-btn" type="button" @click="toggleMasterKey">
                                {{ showMasterKey ? '👁️‍🗨️' : '👁️' }}
                            </button>
                        </div>
                    </div>

                    <button type="submit" class="btn-login w-100" :disabled="loading || !isFormValid">
                        {{ loading ? 'Обработка...' : (isInitialized ? 'Войти' : 'Создать и войти') }}
                    </button>

                    <p v-if="error" class="text-danger mt-3">{{ error }}</p>
                    <p v-if="!isInitialized" class="mt-3 small text-primary">
                        Система пуста. Зарегистрируйтесь как первый администратор, используя мастер-ключ.
                    </p>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.login-page {
    height: 100vh;
}

.login-card {
    background-color: #F2ECDF;
    border: 2px solid #3F2B4C;
    border-radius: 25px;
    width: 100%;
    max-width: 400px;
    z-index: 1;
}

.login-card h2 {
    color: #3F2B4C;
}

.custom-input {
    border: 2px solid #3F2B4C;
    background-color: transparent;
    border-radius: 10px;
    padding: 12px;
}

.custom-input:focus {
    border-color: #E0EDAB;
    box-shadow: none;
}

.btn-login {
    background-color: #3F2B4C;
    color: #F2ECDF;
    border: none;
    padding: 12px;
    border-radius: 10px;
    font-weight: 700;
    transition: 0.3s;

    &:hover {
        background-color: #E0EDAB;
        color: #3F2B4C;
        transform: translateY(-2px);
    }

    &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none !important;
        background-color: #3F2B4C;
        color: #F2ECDF;
    }
}

.login-page-image {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    object-fit: cover;
    filter: brightness(50%);
    z-index: 0;
    user-select: none;
    -webkit-user-drag: none;
}

.input-group {
    position: relative;
}

.eye-btn {
    border: 2px solid #3F2B4C;
    border-left: none;
    background: transparent;
    border-top-right-radius: 10px !important;
    border-bottom-right-radius: 10px !important;
    transition: all 0.3s;
}

.btn.eye-btn {
    border-color: #3F2B4C;

    &:hover {
        background-color: #3F2B4C;
    }
}

.btn-outline-primary.eye-btn {
    border-color: #0D6EFD;

    &:hover {
        background-color: #0D6EFD;
    }
}

.spinner-border {
    width: 3rem;
    height: 3rem;
    color: #3F2B4C !important;
}
</style>