import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'

import './styles.scss'
import * as bootstrap from 'bootstrap'
import './assets/main.css' 

const app = createApp(App)


app.use(router)

app.mount('#app')
