import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
    withCredentials: true // ОБЯЗАТЕЛЬНО для работы с HttpOnly Cookies
});

// 1. Перед каждым запросом добавляем Access Token из localStorage
api.interceptors.request.use(config => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// 2. Если сервер ответил 401 (токен протух), пытаемся обновиться
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // Если ошибка 401 и мы еще не пробовали обновлять токен в этом запросе
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                // Запрашиваем новый Access Token. 
                // Refresh Token из HttpOnly куки прикрепится автоматически браузером.
                const res = await axios.post('http://localhost:8000/auth/refresh', {}, { withCredentials: true });
                const newToken = res.data.access_token;

                localStorage.setItem('access_token', newToken);

                // Повторяем изначальный запрос с новым токеном
                originalRequest.headers.Authorization = `Bearer ${newToken}`;
                return axios(originalRequest);
            } catch (refreshError) {
                // Если и Refresh Token невалиден — выкидываем на логин
                localStorage.removeItem('access_token');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    }
);

export default api;