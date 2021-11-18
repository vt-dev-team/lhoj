import { createApp } from "vue"
import { createStore } from 'vuex'
import App from "./App.vue"
import router from "./router/router"

import "bootstrap/dist/css/bootstrap.min.css"
import "./statics/argon/css/argon-design-system.min.css"
import $ from "jquery"
import "bootstrap"

import "./statics/fontawesome/css/all.css"
import "./statics/main.css"
import 'sweetalert2/dist/sweetalert2.min.css'
import 'simplemde/dist/simplemde.min.css'

import './statics/tomorrow.css'
import 'katex/dist/katex.min.css'
import 'flatpickr/dist/flatpickr.min.css'
import 'nprogress/nprogress.css'

import moment from 'moment'
import 'moment/dist/locale/zh-cn.js'
moment.locale('zh-cn')
moment().utcOffset(8)

import axios from 'axios'
axios.defaults.withCredentials = true

const store = createStore({
    state() {
        return {
            //backendURL: "",
            backendURL: "http://192.68.4.215",
            ojName: "LHOJ",
            pageTitle: "LHOJ",
            loginUser: {
                uid: "-1",
                privilege: 5,
                uname: "未登录"
            }
        }
    },
    mutations: {
        changeTitle(state, t) {
            state.pageTitle = t
            document.title = t + ' - LHOJ'
        },
        updateUser(state, u) {
            state.loginUser = u
        }
    }
})

const app = createApp(App)
app.config.globalProperties.$axios = axios
app.config.globalProperties.$moment = moment
app.use(router).use(store).mount("#app")