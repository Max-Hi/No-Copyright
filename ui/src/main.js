import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './main.css'

let app = createApp(App)
app.use(store)
app.use(router)
app.mount('#app')

const STATIC_FILES_HOSTNAME = "http://localhost:9000"
app.config.globalProperties.staticFilesHostname = STATIC_FILES_HOSTNAME 