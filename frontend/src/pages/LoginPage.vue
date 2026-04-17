<script>
import api from '@/api';
import EyeIcon from '../assets/icons/eye.svg?component'
import EyeClosed from '../assets/icons/eye-closed.svg?component'

export default {
    name: 'LoginPage',
    data() {
        return {
            isCheckingStatus: true,
            isInitialized: true,
            masterKey: '',
            firstName: '',
            lastName: '',
            email: '',
            password: '',
            error: '',
            loading: false,
            showPassword: false,
            showMasterKey: false
        };
    },
    computed: {
        passwordValidation() {
            if (this.isInitialized) return { valid: true };
            const p = this.password;
            const hasDigit = /\d/.test(p);
            const hasUpper = /[A-Z]/.test(p);
            const hasLower = /[a-z]/.test(p);
            const minLength = p.length >= 8;
            return {
                valid: hasDigit && hasUpper && hasLower && minLength
            };
        },
        isFormValid() {
            if (this.isInitialized) return this.email && this.password;
            return (
                this.firstName && 
                this.lastName && 
                this.email && 
                this.passwordValidation.valid && 
                this.masterKey
            );
        }
    },
    methods: {
        togglePassword() { this.showPassword = !this.showPassword; },
        toggleMasterKey() { this.showMasterKey = !this.showMasterKey; },
        
        async handleAuth() {
            this.loading = true;
            this.error = '';
            try {
                if (!this.isInitialized) {
                    // Регистрация
                    const res = await api.post(`/auth/register/first?key=${this.masterKey}`, {
                        first_name: this.firstName,
                        last_name: this.lastName,
                        email: this.email,
                        password: this.password
                    });
                    localStorage.setItem('access_token', res.data.access_token);
                    this.$router.push('/admin');
                } else {
                    // Логин
                    const formData = new FormData();
                    formData.append('username', this.email);
                    formData.append('password', this.password);
                    
                    const res = await api.post('/auth/login', formData);
                    localStorage.setItem('access_token', res.data.access_token);
                    this.$router.push('/admin');
                }
            } catch (err) {
                this.error = err.response?.data?.detail || 'Ошибка операции';
            } finally {
                this.loading = false;
            }
        }
    },
    async mounted() {
        if (localStorage.getItem('access_token')) {
            this.$router.push('/admin');
            return;
        }
        try {
            const res = await api.get('/auth/check-init');
            this.isInitialized = res.data.is_initialized;
        } catch (err) {
            console.error("Ошибка проверки системы");
        } finally {
            this.isCheckingStatus = false;
        }
    },
    components: {
        EyeIcon,
        EyeClosed
    }
};
</script>

<template>
    <div class="login-page d-flex align-items-center justify-content-center">
        <img class="login-page-image" src="/image.png" alt="">
        
        <div class="login-card p-5 shadow-lg text-center">
            <!-- Загрузка при первой проверке -->
            <div v-if="isCheckingStatus" class="py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Загрузка...</span>
                </div>
                <p class="mt-3 text-muted">Проверка состояния системы...</p>
            </div>

            <div v-else>
                <h2 class="mb-4 fw-bold">
                    {{ isInitialized ? 'Вход в систему' : 'Создание админа' }}
                </h2>

                <form @submit.prevent="handleAuth">
                    <!-- Поля регистрации -->
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

                    <!-- Пароль -->
                    <div class="mb-3 text-start">
                        <label class="form-label">Пароль</label>
                        <div class="input-group">
                            <input v-model="password" :type="showPassword ? 'text' : 'password'" 
                                   class="form-control custom-input" placeholder="••••••••" required>
                            <button class="btn eye-btn" type="button" @click="togglePassword">
                                <eye-icon width="1.5em" height="autho" v-if="showPassword" />
                                <eye-closed width="1.5em" height="autho" v-else />
                            </button>
                        </div>
                        <div v-if="!isInitialized && password.length > 0" class="mt-2 password-hints">
                            <small :class="passwordValidation.valid ? 'text-success' : 'text-muted'">
                                {{ passwordValidation.valid ? '✅ Пароль надежен' : '❌ Минимум 8 симв., цифра и заглавная' }}
                            </small>
                        </div>
                    </div>

                    <!-- Мастер-ключ -->
                    <div v-if="!isInitialized" class="mb-4 text-start">
                        <label class="form-label text-primary">Секретный ключ (Master Key)</label>
                        <div class="input-group">
                            <input v-model="masterKey" :type="showMasterKey ? 'text' : 'password'" 
                                   class="form-control custom-input border-primary" required>
                            <button class="btn btn-outline-primary eye-btn" type="button" @click="toggleMasterKey">
                                <eye-icon width="1.5em" height="autho" v-if="showMasterKey" />
                                <eye-closed width="1.5em" height="autho" v-else />
                            </button>
                        </div>
                    </div>

                    <button type="submit" class="btn-login w-100" :disabled="loading || !isFormValid">
                        {{ loading ? 'Обработка...' : (isInitialized ? 'Войти' : 'Создать и войти') }}
                    </button>

                    <p v-if="error" class="text-danger mt-3">{{ error }}</p>
                    <p v-if="!isInitialized" class="mt-3 small text-primary">
                        Система пуста. Зарегистрируйтесь как первый администратор.
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
        color: white;
        border-color: #3F2B4C;
    }
}

.btn-outline-primary.eye-btn {
    border-color: #0D6EFD;

    &:hover {
        background-color: #0D6EFD;
        border-color: #0D6EFD;
    }
}

.spinner-border {
    width: 3rem;
    height: 3rem;
    color: #3F2B4C !important;
}
</style>