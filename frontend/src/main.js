import { createApp } from "vue"
import { createStore } from 'vuex'
import App from "./App.vue"
import router from "./router/router"

import "bootstrap/dist/css/bootstrap.min.css"
import "./statics/lazykit/css/lazy.css"
import "jquery"
import "bootstrap"

import "./statics/fontawesome/css/all.css"
import "./statics/main.css"
import 'sweetalert2/dist/sweetalert2.min.css'

import 'prismjs/themes/prism.css'
import 'katex/dist/katex.min.css'

const store = createStore({
    state() {
        return {
            backendURL: "http://127.0.0.1:8000",
            pageTitle: "LHOJ",
            loginUser: {
                uid: "-1",
            }
        }
    },
    mutations: {
        changeTitle(state, t) {
            state.pageTitle = t
        }
    }
})

const app = createApp(App)
app.config.globalProperties.$pageTitle = "LHOJ"
app.use(router).use(store).mount("#app")