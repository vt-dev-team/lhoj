<template>
    <div class="row">
        <div class="col-md-9 col-sm-12 order-md-1 order-2">
            <div class="messageBox">
                <div class="message-mask" v-if="isLoading">
                    <div class="d-flex justify-content-center" style="height: 100%">
                        <div class="spinner-grow" style="margin:auto" role="status">
                            <span class="sr-only">Loading...</span>
                        </div>
                    </div>
                </div>
                <div class="messageBox-main">
                    <div class="messageBox-sidebar">
                        <div class="messageSidebar-header">
                            <input
                                class="form-control"
                                v-model="searchContent"
                                @change="doSearch"
                                placeholder="查找用户"
                            />
                        </div>
                        <div class="messageSidebar-list">
                            <ul class="contest-menu" v-if="contactList.length > 0">
                                <li v-for="(ci, i) in contactList" v-bind:key="i">
                                    <a
                                        href="javascript:;"
                                        :class="{ active: contactor == ci }"
                                        @click="chooseContact(ci)"
                                    >
                                        {{ ci.u }}
                                        <span
                                            class="badge badge-danger float-right"
                                            v-if="ci.n > 0"
                                        >{{ ci.n }}</span>
                                    </a>
                                </li>
                            </ul>
                            <ul class="contest-menu" v-else>
                                <li>
                                    <a>这里空空如也</a>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="messageBox-area" id="messageBox-area">
                        <div class="text-center" v-if="contactor">
                            <div class="moreMessage" v-if="currentPage < totalPage">
                                <a @click="chooseContact(contactor, 0)">加载更多消息</a>
                            </div>
                        </div>
                        <div
                            class="line-message"
                            v-for="(m, i) in revarr(messageList)"
                            v-bind:key="i"
                        >
                            <div
                                :class="m.from_user == $store.state.loginUser.uname ? 'me-message' : 'you-message'"
                            >
                                <div class="message-avatar">
                                    <img src="/no-avatar.svg" />
                                </div>
                                <div class="message-content">
                                    {{ m.content }}
                                    <br />
                                    <div class="message-date vtooltip">
                                        {{ getFormatDate(m.date) }}
                                        <template
                                            v-if="(m.from_user == $store.state.loginUser.uname) && (!m.isRead)"
                                        >未读</template>
                                        <span class="tooltiptext">{{ getFormatDate(m.date, 0) }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="messageBox-input" v-show="contactor">
                        <div class="messageBox-input-area">
                            <textarea v-model="mes"></textarea>
                        </div>
                        <button @click="sendMessage" :disabled="isSubmit">
                            <i class="far fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3 col-sm-12 order-md-2 order-1">
            <ul class="contest-menu">
                <li>
                    <router-link
                        :to="{ name: 'UserInfo', params: { id: $store.state.loginUser.uname } }"
                    >
                        <i class="far fa-user"></i>个人信息
                    </router-link>
                </li>
                <li>
                    <router-link
                        :to="{ name: 'UserModify', params: { id: $store.state.loginUser.uname } }"
                    >
                        <i class="fas fa-cog"></i>信息修改
                    </router-link>
                </li>
                <li>
                    <router-link :to="{ name: 'UserMessage' }">
                        <i class="far fa-envelope"></i>站内私信
                    </router-link>
                </li>
            </ul>
        </div>
    </div>
</template>

<style scoped>
.message-mask {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(255, 255, 255, 0.8);
    z-index: 2;
}

.messageBox {
    height: 31.25rem;
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
    box-sizing: inherit;
    position: relative;
}
.messageBox-sidebar {
    border-right: 1px solid #eee;
    float: left;
    width: 15.625rem;
}
.messageSidebar-header {
    padding: 1.5625rem 0.9375rem;
    height: 5rem;
    position: relative;
    border-bottom: 1px solid #eee;
}
.messageSidebar-list {
    overflow: auto;
    height: 26.25rem;
}
.messageBox-area {
    position: absolute;
    height: 26.25rem;
    left: 15.625rem;
    right: 0;
    top: 0;
    bottom: 5rem;
    overflow: auto;
    padding: 1.875rem;
}
.line-message {
    display: inline-block;
    width: 100%;
    margin-bottom: 1.875rem;
    word-wrap: break-word;
}
.me-message div {
    float: right;
}
.you-message div {
    float: left;
}
.message-avatar img {
    width: 48px;
    height: 48px;
    border-radius: 50%;
}
.you-message .message-content {
    position: relative;
    margin-left: 0.625rem;
    background-color: #ededed;
    padding: 0.6375rem;
    max-width: calc(100% - 48px - 1.89rem);
}
.you-message .message-content:before {
    content: "";
    position: absolute;
    left: -5px;
    top: 12px;
    width: 10px;
    height: 10px;
    background-color: #ededed;
    transform: rotate(45deg);
}
.me-message .message-content {
    position: relative;
    margin-right: 0.625rem;
    background-color: #5e72e4;
    color: #fff;
    padding: 0.6375rem;
    max-width: calc(100% - 48px - 1.89rem);
}
.message-date {
    color: rgba(233, 233, 233, 0.5);
    font-size: 12px;
}
.you-message .message-date {
    color: rgba(88, 88, 88, 0.5);
}
.me-message .message-content:before {
    content: "";
    position: absolute;
    right: -5px;
    top: 12px;
    width: 10px;
    height: 10px;
    background-color: #5e72e4;
    transform: rotate(45deg);
}
.line-message:after {
    content: "";
    clear: both;
}
.messageBox-input {
    position: absolute;
    left: 15.625rem;
    right: 0;
    bottom: 0;
    height: 80px;
    border-top: 1px solid #eee;
}
.messageBox-input-area {
    position: absolute;
    left: 0.625rem;
    right: 3.75rem;
    top: 0.625rem;
    bottom: 0.625rem;
}
.messageBox-input-area textarea {
    display: block;
    border: 0;
    background: none;
    padding: 0;
    width: 100%;
    height: 100%;
    font-size: 0.875rem;
    resize: none;
    outline: 0;
}
.moreMessage {
    color: #ddd;
    margin-bottom: 10px;
}
.moreMessage:hover {
    color: #aaa;
}
.messageBox-input button {
    display: block;
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    position: absolute;
    right: 0;
    width: 3.125rem;
    top: 0;
    height: 100%;
    border: 0;
    background: none;
    text-align: center;
    line-height: 5rem;
    font-size: 1rem;
    transition: background-color 0.1s, color 0.1s, opacity 0.1s;
    transition-timing-function: linear;
    outline: 0;
    background-color: #5e72e4;
    color: #fff;
}
.messageBox-input button:disabled {
    background-color: #fff;
    color: #ddd;
}
</style>

<script>
import Swal from 'sweetalert2'
const Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 1000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.addEventListener("mouseenter", Swal.stopTimer);
        toast.addEventListener("mouseleave", Swal.resumeTimer);
    },
})
export default {
    data() {
        return {
            contactList: [],
            contactor: {},
            messageList: [],
            mes: "",
            isSubmit: false,
            isLoading: true,
            currentPage: 1,
            totalPage: 1,
            searchContent: ''
        }
    },
    mounted() {
        let _t = this
        _t.$store.commit('changeTitle', `私信`)
        _t.getContactList()
    },
    methods: {
        doSearch() {
            const _t = this
            if (_t.searchContent.length == 0)
                _t.getContactList()
            else {
                _t.isLoading = true
                _t.$axios.get(`${_t.$store.state.backendURL}/api/user/find/?find=${_t.searchContent}`).then((res) => {
                    _t.isLoading = false
                    _t.contactList = res.data.data
                }).catch((err) => {
                    Toast.fire(
                        'Oops',
                        err.message,
                        'error',
                    )
                })
            }
        },
        getContactList() {
            let _t = this
            _t.isLoading = true
            _t.$axios.get(`${_t.$store.state.backendURL}/api/user/contacts/`).then((res) => {
                _t.contactList = res.data.data
                _t.isLoading = false
            })
        },
        chooseContact(e, a = 1) {
            let _t = this
            _t.isLoading = true
            if (a) {
                _t.messageList = []
                _t.currentPage = 1
            }
            else
                _t.currentPage++
            _t.$axios.get(`${_t.$store.state.backendURL}/api/user/message/?to_user=${e.u}&page=${_t.currentPage}`).then((res) => {
                _t.contactor = e
                e.n = 0
                if (res.data.code && res.data.code != 0) {
                    if (!a)
                        _t.currentPage--
                    Toast.fire(
                        'Oops',
                        res.data.mes,
                        'error',
                    )
                }
                else {
                    _t.currentPage = res.data.currentPage
                    _t.totalPage = res.data.totalPage
                    for (let k in res.data.data)
                        _t.messageList.push(res.data.data[k])
                    if (a)
                        setTimeout(() => { document.getElementById("messageBox-area").scrollTop = document.getElementById("messageBox-area").scrollHeight }, 50)
                }
                _t.isLoading = false
            }).catch((err) => {
                Toast.fire(
                    'Oops',
                    err.message,
                    'error',
                )
            })
        },
        sendMessage() {
            let _t = this
            let param = new URLSearchParams()
            param.append('content', _t.mes)
            param.append('to_user', _t.contactor.u)
            _t.isSubmit = true
            _t.$axios.post(`${_t.$store.state.backendURL}/api/user/send_message/`, param).then((res) => {
                _t.isSubmit = false
                if (res.data.code != 0) {
                    Toast.fire(
                        'Oops',
                        res.data.mes,
                        'error',
                    )
                }
                else {
                    _t.chooseContact(_t.contactor)
                    _t.mes = ""
                }
            }).catch((err) => {
                _t.isSubmit = false
                Toast.fire(
                    'Oops',
                    err.message,
                    'error',
                )
            })
        },
        revarr(q) {
            return [...q].reverse()
        },
        getFormatDate(e, k = 1) {
            return k ? this.$moment(e).fromNow() : this.$moment(e).format("YYYY-MM-DD HH:mm:ss")
        }
    }
}
</script>
