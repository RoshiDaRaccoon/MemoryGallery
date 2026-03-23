<script>
import { MasonryWall } from '@yeger/vue-masonry-wall';
import axios from 'axios';
export default {
    components: {
        MasonryWall
    },
    data() {
        return {
            API_URL: 'http://localhost:8000/photos/',
            STATIC_FILES_BASE_URL: 'http://localhost:8000/public-photos/',
            photos: [],
            loading: true,
            error: null,
            image: "image.png",
            windowWidth: window.innerWidth,
            // Параметры пагинации
            limit: 12,
            offset: 0,
            hasMore: true,
            observer: null // Хранилище для наблюдателя
        }
    },
    computed: {
        columnWidth() {
            if (this.windowWidth < 482) {
                return 150;
            } else if (this.windowWidth < 648) {
                return 220;
            } else {
                return 300;
            }
        }
    },
    methods: {
        async fetchPhotos() {
            if (!this.hasMore || this.loadingMore) return;

            // Если это первая загрузка
            if (this.photos.length === 0) this.loading = true;
            else this.loadingMore = true;

            try {
                const response = await axios.get(this.API_URL, {
                    params: { limit: this.limit, offset: this.offset }
                });

                const newPhotos = response.data;
                this.photos = [...this.photos, ...newPhotos];

                // Проверяем, есть ли что грузить дальше
                this.hasMore = newPhotos.length === this.limit;
                this.offset += this.limit;

                this.loading = false;
                this.loadingMore = false;
            } catch (err) {
                this.error = err.message;
                this.loading = false;
                this.loadingMore = false;
            }
        },
        setupIntersectionObserver() {
            // Создаем наблюдателя
            this.observer = new IntersectionObserver((entries) => {
                // Если "маячок" появился внизу экрана и данные еще есть
                if (entries[0].isIntersecting && this.hasMore && !this.loading) {
                    this.fetchPhotos();
                }
            }, { threshold: 0.1 }); // Сработает, когда хотя бы 10% маячка видно

            // Прикрепляем к элементу с ref="loadMoreInterceptor"
            if (this.$refs.loadMoreInterceptor) {
                this.observer.observe(this.$refs.loadMoreInterceptor);
            }
        },
        getImage(photo) {
            const relativePath = photo.path.replace(/^photos[\\\/]/, '').replace(/\\/g, '/');
            const imageUrl = `${this.STATIC_FILES_BASE_URL}${relativePath}`;
            return imageUrl
        },
        getDate(photo) {
            if (!photo.date) return '';
            return photo.date.split('T')[0].split('-').reverse().join('.');
        },
        handleResize() {
            this.windowWidth = window.innerWidth;
        },
        async downloadImage(photo) {
            try {
                const url = this.getImage(photo);

                // 1. Скачиваем файл как набор байтов (blob)
                const response = await axios.get(url, {
                    responseType: 'blob'
                });

                // 2. Создаем временную ссылку в памяти браузера
                const blobUrl = window.URL.createObjectURL(new Blob([response.data]));

                // 3. Создаем невидимую ссылку и программно кликаем по ней
                const link = document.createElement('a');
                link.href = blobUrl;

                // Формируем имя файла (например, "123.jpg")
                const fileName = `${photo.id}.jpg`;
                link.setAttribute('download', fileName);

                document.body.appendChild(link);
                link.click();

                // 4. Удаляем ссылку и освобождаем память
                link.remove();
                window.URL.revokeObjectURL(blobUrl);

            } catch (err) {
                console.error('Ошибка при скачивании:', err);
                alert('Не удалось скачать фото. Проверьте консоль.');
            }
        }
    },
    mounted() {
        this.fetchPhotos().then(() => {
            // Запускаем слежку после первой загрузки
            this.setupIntersectionObserver();
        });
        window.addEventListener('resize', this.handleResize);
    },
    beforeUnmount() {
        if (this.observer) this.observer.disconnect();
        window.removeEventListener('resize', this.handleResize);
    }
}
</script>

<template>
    <div class="photo-gallery-container d-flex flex-column align-items-center gap-5">
        <img class="gallery-page-image" :src="image" alt="">
        <h1 class="gallery-title">Галерея фотографий</h1>
        <div v-if="!loading && !error">
            <MasonryWall :items="photos" :column-width="columnWidth" :gap="16">
                <template #default="{ item, index }">
                    <div class="photo-card d-flex flex-column align-items-center" data-bs-toggle="modal"
                        :data-bs-target="'#modal-' + index">
                        <img :src="getImage(item)" :alt="item.description || `Фото ${item.id}`" class="photo-image" />
                        <p class="photo-date">{{ getDate(item) }}</p>
                        <p v-if="item.grade" class="photo-class">
                            {{ item.grade }} <span v-if="item.parallel">«{{ item.parallel }}»</span> класс
                        </p>
                    </div>

                    <div class="modal fade" :id="'modal-' + index" tabindex="-1" aria-labelledby="exampleModalLabel"
                        aria-hidden="true">
                        <div class="modal-dialog modal-xl">
                            <div class="modal-content">
                                <div class="modal-header border-0 custom-modal">
                                    <button @click="downloadImage(item)" class="btn btn-primary"
                                        style="background-color: #3F2B4C; border: none; color: #F2ECDF;">Скачать
                                        фото</button>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                                        aria-label="Close"></button>
                                </div>
                                <div class="modal-body text-center custom-modal">
                                    <img :src="getImage(item)" :alt="item.description || `Фото ${item.id}`"
                                        width="100%" />
                                </div>
                                <div class="modal-footer d-flex flex-column border-2 custom-modal">
                                    <h5 v-if="item.description">{{ item.description }}</h5>
                                    <p class="mb-0">{{ getDate(item) }} <span v-if="item.grade">
                                            | {{ item.grade }} <span v-if="item.parallel">«{{ item.parallel }}»</span>
                                            класс
                                        </span>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </MasonryWall>
            <div ref="loadMoreInterceptor" class="scroll-trigger" />

            <div class="d-flex justify-content-center">
                <div v-if="loadingMore" class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Загрузка...</span>
                </div>
                <p v-if="!hasMore && photos.length > 0" class="end-msg m-5">
                    Пока что всё!
                </p>
            </div>
        </div>
        <div v-if="loading" class="d-flex flex-column align-items-center justify-content-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Загрузка...</span>
            </div>
            <p class="status-msg">Загрузка фотографий...</p>
        </div>
        <div v-if="error" class="w-100">
            <p class="status-msg">Ошибка при загрузке: {{ error }}</p>
        </div>
    </div>
</template>

<style>
.gallery-page-image {
    position: fixed;
    width: 100vw;
    height: 100vh;
    user-select: none;
    -webkit-user-drag: none;
    object-fit: cover;
    filter: contrast(105%) brightness(40%);
    z-index: -1;
}

.photo-gallery-container {
    min-height: 100vh;
    color: #F2ECDF;
}

.gallery-title {
    padding-top: 2em;
    font-weight: 700;
    font-size: 4rem;
    margin-bottom: 1.5em;
    color: #F2ECDF;
    text-align: center;
}

/* Стили карточки */
.photo-card {
    background-color: rgb(242, 236, 223);
    border: 2px solid #3F2B4C;
    border-radius: 15px;
    overflow: hidden;
    transition: all 0.3s ease-out;
    cursor: pointer;

    &:hover {
        transform: translateY(-10px);
        box-shadow: 0 10px 20px rgb(224, 237, 171);
        border-color: #E0EDAB;
    }

    &:hover img {
        border-color: #E0EDAB;
    }
}

.photo-image {
    border-bottom: 2px solid #3F2B4C;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: all 0.3s ease-out;
}

.photo-date {
    color: #3F2B4C;
    font-weight: 600;
    margin-bottom: 0.1rem;
}

.photo-class {
    color: #3F2B4C;
    font-weight: 600;
    font-size: 1rem;
    opacity: 0.8;
    margin: 0;
}

.custom-modal {
    color: #3F2B4C;
}

.status-msg {
    text-align: center;
    font-size: 2rem;
    color: #F2ECDF;
}

.scroll-trigger {
    position: relative;
    bottom: 25em;
}

.spinner-border {
    width: 3rem;
    height: 3rem;
    color: #F2ECDF !important;
}

@media (max-width: 1200px) {
    .gallery-title {
        font-size: 2rem;
    }

    .photo-card * {
        font-size: 0.8rem;
    }
}
</style>