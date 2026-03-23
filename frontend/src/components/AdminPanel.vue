<script>
import api from '@/api';

export default {
    data() {
        return {
            currentAction: null,
            loading: false,
            isDragging: false,
            uploadForm: {
                file: null,
                date: new Date().toISOString().split('T')[0],
                grade: null,
                parallel: '',
                description: ''
            },
            updateForm: {
                id: null,
                date: null,
                grade: null,
                parallel: '',
                description: ''
            },
            registerForm: {
                first_name: '',
                last_name: '',
                email: '',
                password: ''
            },
            deleteId: null,
            profileForm: {
                first_name: '',
                last_name: '',
                email: '',
                password: ''
            },
            originalProfile: null,
        }
    },
    methods: {
        handleFileSelect(e) {
            this.uploadForm.file = e.target.files[0];
        },
        handleDrop(e) {
            this.isDragging = false;
            this.uploadForm.file = e.dataTransfer.files[0];
        },
        resetForm(form) {
            if (form == 'upload') {
                this.uploadForm = {
                    file: null,
                    // Сбрасываем дату на текущую, чтобы админу не вводить её каждый раз
                    date: new Date().toISOString().split('T')[0],
                    grade: null,
                    parallel: '',
                    description: ''
                };
                // Если ты используешь ref="fileInput" для инпута, очисти и его значение
                if (this.$refs.fileInput) {
                    this.$refs.fileInput.value = '';
                };
            } else if (form == 'update') {
                this.updateForm = {
                    id: null,
                    date: null,
                    grade: null,
                    parallel: '',
                    description: ''
                }
            } else if (form == 'register') {
                this.registerForm = {
                    first_name: '',
                    last_name: '',
                    email: '',
                    password: ''
                };
            }
        },
        async submitUpload() {
            this.loading = true;
            const formData = new FormData();

            // 1. Добавляем файл (важно: берем первый элемент, если это FileList из инпута)
            // Если у тебя Drag-and-Drop возвращает сразу File, оставь просто this.uploadForm.file
            const fileToUpload = this.uploadForm.file instanceof FileList
                ? this.uploadForm.file[0]
                : this.uploadForm.file;

            if (!fileToUpload) {
                alert("Пожалуйста, выберите файл");
                this.loading = false;
                return;
            }

            formData.append('file', fileToUpload);

            // 2. Собираем объект данных для Pydantic
            const photoData = {
                date: this.uploadForm.date,
                description: this.uploadForm.description || null,
                grade: this.uploadForm.grade ? parseInt(this.uploadForm.grade) : null,
                parallel: this.uploadForm.parallel || null
            };

            // 3. Превращаем объект в JSON-строку и добавляем в поле, которое ждет бэкенд
            formData.append('photo_data_json', JSON.stringify(photoData));

            try {
                // Отправляем через наш настроенный api (с токенами)
                await api.post('/photos/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });

                alert('Фото успешно загружено!');
                this.resetForm('upload');
            } catch (err) {
                console.error(err);
                const errorMsg = err.response?.data?.detail || err.message;
                alert('Ошибка при загрузке: ' + JSON.stringify(errorMsg));
            } finally {
                this.loading = false;
            }
        },
        async submitUpdate() {
            this.loading = true;
            const updatePayload = {
                date: this.updateForm.date || null,
                description: this.updateForm.description || null,
                grade: this.updateForm.grade ? parseInt(this.updateForm.grade) : null,
                parallel: this.updateForm.parallel || null
            };

            try {
                await api.put(`/photos/${this.updateForm.id}`, updatePayload);

                alert('Фото успешно изменено!');
                this.resetForm('update');
            } catch (err) {
                console.error(err);
                const errorMsg = err.response?.data?.detail || err.message;
                alert('Ошибка: ' + JSON.stringify(errorMsg));
            } finally {
                this.loading = false;
            }
        },
        async submitDelete() {
            this.loading = true;
            const formData = new FormData();
            formData.append('id', this.deleteId);
            try {
                await api.delete(`/photos/${this.deleteId}`, formData);
                alert('Успешно!');
            } catch (err) {
                alert('Ошибка: ' + err.response?.data?.detail || err.message);
            } finally {
                this.loading = false;
            }
        },
        async submitRegister() {
            this.loading = true;
            try {
                const response = await api.post('/auth/register', this.registerForm);
                alert(response.data.message || 'Администратор создан');
                this.resetForm('register')
                this.currentAction = null; // Возврат в меню
            } catch (err) {
                console.error(err);
                const errorMsg = err.response?.data?.detail || err.message;
                // Если ошибка валидации (Pydantic), она может быть массивом
                alert('Ошибка регистрации: ' + (typeof errorMsg === 'object' ? JSON.stringify(errorMsg) : errorMsg));
            } finally {
                this.loading = false;
            }
        },
        async handleLogout() {
            try {
                this.loading = true;
                // Отправляем запрос на бэкенд для зануления refresh_token и удаления куки
                await api.post('/auth/logout');
            } catch (err) {
                console.error("Ошибка при выходе:", err);
            } finally {
                // В любом случае очищаем локальные данные
                localStorage.removeItem('access_token');
                this.loading = false;
                // Перенаправляем на страницу логина
                this.$router.push('/login');
            }
        },
        async loadProfile() {
            try {
                const response = await api.get('/users/me');
                this.profileForm = { ...response.data, password: '' };
                this.originalProfile = JSON.stringify({ ...response.data, password: '' });
            } catch (error) {
                alert("Ошибка загрузки профиля");
            }
        },
        async submitUpdateProfile() {
            this.loading = true;
            // Создаем копию данных для отправки
            const payload = { ...this.profileForm };

            // Если пароль пустой, отправляем null, чтобы не триггерить валидатор
            if (!payload.password || payload.password.trim() === "") {
                payload.password = null;
            }
            try {
                // Используем твой существующий PUT /users/{id}
                await api.put(`/users/${this.profileForm.id}`, payload);
                this.originalProfile = JSON.stringify(this.profileForm);
                alert("Профиль обновлен!");
            } catch (error) {
                alert("Ошибка обновления");
            } finally { this.loading = false; }
        },
        async submitDeleteAccount() {
            if (confirm("Вы уверены? Это действие необратимо!")) {
                try {
                    await api.delete(`/users/${this.profileForm.id}`);
                    // Тут логика выхода: удаление токена и редирект
                    localStorage.removeItem('access_token');
                    delete api.defaults.headers.common['Authorization'];
                    this.$router.push('/login');
                } catch (error) {
                    alert("Ошибка при удалении");
                } finally {
                    this.loading = false;
                }
            }
        }
    },
    computed: {
        displayInfo() {
            return this.originalProfile ? JSON.parse(this.originalProfile) : { first_name: '', last_name: '' };
        },
        isProfileChanged() {
            // Сравниваем текущую форму с сохраненным оригиналом
            return JSON.stringify(this.profileForm) !== this.originalProfile;
        },
        isRegisterFormValid() {
            const f = this.registerForm;
            // Регулярки как в твоем schemas.py
            const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            const hasDigit = /\d/.test(f.password);
            const hasUpper = /[A-Z]/.test(f.password);
            const hasLower = /[a-z]/.test(f.password);

            return (
                f.first_name.length > 0 &&
                f.last_name.length > 0 &&
                emailRegex.test(f.email) &&
                f.password.length >= 6 &&
                hasDigit && hasUpper && hasLower
            );
        }
    }
}
</script>

<template>
    <div class="admin-container d-flex flex-column align-items-center gap-4">
        <img class="gallery-page-image" src="/image.png" alt="">
        <h1 class="gallery-title">Панель управления</h1>

        <!-- Главное меню выбора -->
        <div v-if="!currentAction" class="d-flex flex-wrap justify-content-center gap-4">
            <button @click="currentAction = 'add'" class="admin-main-btn">➕ Добавить фото</button>
            <button @click="currentAction = 'update'" class="admin-main-btn">📝 Изменить данные</button>
            <button @click="currentAction = 'delete'" class="admin-main-btn">🗑️ Удалить фото</button>
            <button @click="currentAction = 'register'" class="admin-main-btn secondary">👤 Новый админ</button>

            <button @click="currentAction = 'profile'; loadProfile()" class="admin-main-btn profile-btn">👤 Мой
                профиль</button>

            <!-- Кнопка Выхода -->
            <button @click="handleLogout" class="admin-main-btn logout-btn" :disabled="loading">
                🚪 {{ loading ? 'Выход...' : 'Выйти' }}
            </button>
        </div>

        <!-- Форма возврата -->
        <button v-if="currentAction" @click="currentAction = null" class="btn btn-outline-light mb-4">⬅ Назад</button>

        <!-- Форма ДОБАВЛЕНИЯ -->
        <div v-if="currentAction === 'add'" class="admin-card p-4 col-12 col-md-6">
            <h3>Загрузка нового фото</h3>
            <div class="drop-zone mb-3" @dragover.prevent @drop.prevent="handleDrop" :class="{ 'dragging': isDragging }"
                @dragenter="isDragging = true" @dragleave="isDragging = false">
                <input type="file" @change="handleFileSelect" hidden ref="fileInput">
                <p v-if="!uploadForm.file" @click="$refs.fileInput.click()">Перетащите фото сюда или нажмите для выбора
                </p>
                <p v-else class="text-success">✅ {{ uploadForm.file.name }}</p>
            </div>

            <div class="mb-3">
                <label class="form-label">Дата</label>
                <input type="date" v-model="uploadForm.date" class="form-control custom-input">
            </div>

            <div class="row">
                <div class="col-6 mb-3">
                    <label class="form-label">Класс (1-11)</label>
                    <select v-model="uploadForm.grade" class="form-select custom-input">
                        <option :value="null">Нет</option>
                        <option v-for="n in 11" :key="n" :value="n">{{ n }}</option>
                    </select>
                </div>
                <div class="col-6 mb-3">
                    <label class="form-label">Параллель</label>
                    <input type="text" v-model="uploadForm.parallel" placeholder="Буква"
                        class="form-control custom-input" maxlength="1">
                </div>
            </div>

            <div class="mb-3">
                <label class="form-label">Описание</label>
                <textarea v-model="uploadForm.description" class="form-control custom-input" rows="3"></textarea>
            </div>

            <button @click="submitUpload" class="btn-action w-100" :disabled="loading">
                {{ loading ? 'Загрузка...' : 'Загрузить в галерею' }}
            </button>
        </div>

        <!-- Форма ИЗМЕНЕНИЯ -->
        <div v-if="currentAction === 'update'" class="admin-card p-4 col-12 col-md-6">
            <h3>Изменение информации существующего фото</h3>
            <input type="number" v-model="updateForm.id" class="form-control custom-input mb-3"
                placeholder="Введите ID фото">

            <div class="mb-3">
                <label class="form-label">Дата</label>
                <input type="date" v-model="updateForm.date" class="form-control custom-input">
            </div>

            <div class="row">
                <div class="col-6 mb-3">
                    <label class="form-label">Класс (1-11)</label>
                    <select v-model="updateForm.grade" class="form-select custom-input">
                        <option :value="null">Нет</option>
                        <option v-for="n in 11" :key="n" :value="n">{{ n }}</option>
                    </select>
                </div>
                <div class="col-6 mb-3">
                    <label class="form-label">Параллель</label>
                    <input type="text" v-model="updateForm.parallel" placeholder="Буква"
                        class="form-control custom-input" maxlength="1">
                </div>
            </div>

            <div class="mb-3">
                <label class="form-label">Описание</label>
                <textarea v-model="updateForm.description" class="form-control custom-input" rows="3"></textarea>
            </div>

            <button @click="submitUpdate" class="btn-action w-100" :disabled="loading">
                {{ loading ? 'Загрузка...' : 'Сохранить изменения' }}
            </button>
        </div>

        <!-- Форма УДАЛЕНИЯ (по ID) -->
        <div v-if="currentAction === 'delete'" class="admin-card p-4 col-12 col-md-4">
            <h3>Удаление по ID</h3>
            <input type="number" v-model="deleteId" class="form-control custom-input mb-3"
                placeholder="Введите ID фото">
            <button @click="submitDelete" class="btn-action w-100 delete">Удалить навсегда</button>
        </div>

        <!-- Форма РЕГИСТРАЦИИ -->
        <div v-if="currentAction === 'register'" class="admin-card p-4 col-12 col-md-6">
            <h3>Регистрация нового администратора</h3>

            <div class="row">
                <div class="col-6 mb-3">
                    <label class="form-label">Имя</label>
                    <input type="text" v-model="registerForm.first_name" class="form-control custom-input"
                        placeholder="Иван" required>
                </div>
                <div class="col-6 mb-3">
                    <label class="form-label">Фамилия</label>
                    <input type="text" v-model="registerForm.last_name" class="form-control custom-input"
                        placeholder="Иванов" required>
                </div>
            </div>

            <div class="mb-3">
                <label class="form-label">Email (будет логином)</label>
                <input type="email" v-model="registerForm.email" class="form-control custom-input"
                    placeholder="example@mail.com" required>
            </div>

            <div class="mb-3">
                <label class="form-label">Пароль</label>
                <input type="password" v-model="registerForm.password" class="form-control custom-input"
                    placeholder="Минимум 1 цифра и заглавная буква" required>
                <small class="text-white-50">Пароль должен содержать цифры, большие и маленькие буквы.</small>
            </div>

            <button @click="submitRegister" class="btn-action w-100" :disabled="loading || !isRegisterFormValid"
                :style="{ opacity: isRegisterFormValid ? 1 : 0.5 }">
                {{ loading ? 'Создание...' : 'Зарегистрировать' }}
            </button>

            <!-- Подсказка под кнопкой -->
            <p v-if="!isRegisterFormValid && registerForm.password" class="text-warning mt-2 small">
                Проверьте: имя/фамилия заполнена, корректный Email и сложный пароль.
            </p>
        </div>

        <!-- Форма ПРОФИЛЯ -->
        <div v-if="currentAction === 'profile'" class="admin-card p-4 col-12 col-md-6">
            <!-- Приветственный блок -->
            <div class="profile-header text-center mb-4">
                <h2 class="mb-1">Приветствуем, {{ displayInfo.first_name }} {{ displayInfo.last_name }}! 👋</h2>
                <p class="text-white-50 small">Здесь вы можете обновить свои данные или сменить пароль</p>
            </div>

            <!-- Основная форма -->
            <form @submit.prevent="submitUpdateProfile">
                <div class="row">
                    <div class="col-6 mb-3">
                        <label class="form-label">Имя</label>
                        <input type="text" v-model="profileForm.first_name" class="form-control custom-input" required>
                    </div>
                    <div class="col-6 mb-3">
                        <label class="form-label">Фамилия</label>
                        <input type="text" v-model="profileForm.last_name" class="form-control custom-input" required>
                    </div>
                </div>

                <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input type="email" v-model="profileForm.email" class="form-control custom-input" required>
                </div>

                <div class="mb-4">
                    <label class="form-label">Новый пароль</label>
                    <input type="password" v-model="profileForm.password" class="form-control custom-input"
                        placeholder="Оставьте пустым, чтобы не менять">
                    <small class="text-white-50 d-block mt-1">Пароль должен быть надежным (цифры + заглавные
                        буквы).</small>
                </div>

                <button type="submit" class="btn-action w-100 mb-4" :disabled="loading || !isProfileChanged"
                    :style="{ opacity: isProfileChanged ? 1 : 0.5 }">
                    {{ loading ? 'Сохранение...' : 'Сохранить изменения' }}
                </button>
            </form>

            <!-- Отдельная зона удаления -->
            <div class="danger-zone pt-3 border-top border-secondary mt-2">
                <p class="text-danger small mb-2">Опасная зона</p>
                <button @click="submitDeleteAccount" class="btn-delete-outline w-100" :disabled="loading">
                    🗑️ Удалить мой аккаунт
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.admin-container {
    min-height: 100vh;
}

.admin-main-btn {
    width: 250px;
    height: 150px;
    background-color: #F2ECDF;
    color: #3F2B4C;
    border: 2px solid #3F2B4C;
    border-radius: 20px;
    font-size: 1.5rem;
    font-weight: 700;
    transition: 0.3s;
}

.admin-main-btn:hover {
    transform: scale(1.05);
    background-color: #E0EDAB;
}

.admin-main-btn.secondary {
    background-color: #3F2B4C;
    color: #F2ECDF;

    &:hover {
        border: 2px solid #F2ECDF;
    }
}

.admin-card {
    background-color: rgba(63, 43, 76, 0.9);
    border: 2px solid #F2ECDF;
    border-radius: 20px;
    color: #F2ECDF;
}

.drop-zone {
    border: 2px dashed #E0EDAB;
    padding: 40px;
    text-align: center;
    cursor: pointer;
    border-radius: 15px;
}

.drop-zone.dragging {
    background-color: rgba(224, 237, 171, 0.2);
}

.custom-input {
    background-color: #F2ECDF;
    border: none;
    color: #3F2B4C;
}

.btn-action {
    background-color: #E0EDAB;
    color: #3F2B4C;
    border: none;
    padding: 12px;
    border-radius: 10px;
    font-weight: 700;
}

.btn-action.delete {
    background-color: #ff6b6b;
    color: white;
}

.admin-main-btn.logout-btn {
    background-color: transparent;
    border: 2px solid #ff6b6b;
    color: #ff6b6b;
}

.admin-main-btn.logout-btn:hover {
    background-color: #ff6b6b;
    color: white;
    transform: translateY(-5px);
}

.profile-btn {
    background-color: #4a90e2;
    /* Синий оттенок для отличия */
    border-color: #357abd;
}

.btn-action.delete {
    background-color: #dc3545;
    /* Красный для удаления */
}

.profile-header h2 {
    font-weight: 700;
    color: #E0EDAB;
    /* Твой фирменный цвет */
}

/* Стиль для кнопки удаления, чтобы она не выглядела как основная */
.btn-delete-outline {
    background: transparent;
    color: #ff6b6b;
    border: 1px solid #ff6b6b;
    padding: 0.5rem;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.btn-delete-outline:hover {
    background: #ff6b6b;
    color: white;
}

.border-top {
    border-color: rgba(255, 255, 255, 0.1) !important;
}
</style>