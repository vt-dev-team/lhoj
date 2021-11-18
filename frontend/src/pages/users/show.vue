<template>
    <div class="row">
        <div class="col-md-9 col-sm-12 order-md-1 order-2">
            <div class="card">
                <div class="card-body user-info" style="padding-bottom: 0 !important;">
                    <h3>{{ UserView.username }} (UID: {{ UserView.id }})</h3>注册于
                    <span class="vtooltip">
                        {{ getFormatDate(UserView.reg_time) }}
                        <span
                            class="tooltiptext"
                        >{{ getFormatDate(UserView.reg_time, 0) }}</span>
                    </span>
                    ,
                    解决了{{ UserView.solved }}道题目，Rating: {{ UserView.rating }}
                    <div class="mt-5">
                        <ul class="nav nav-tabs nav-dark" id="userTab" role="tablist">
                            <li class="nav-item">
                                <a
                                    class="nav-link mb-sm-3 mb-md-0 active"
                                    id="description-tab"
                                    data-toggle="tab"
                                    href="#description"
                                    role="tab"
                                >个人介绍</a>
                            </li>
                            <li class="nav-item">
                                <a
                                    class="nav-link mb-sm-3 mb-md-0"
                                    id="posts-tab"
                                    data-toggle="tab"
                                    href="#posts"
                                    role="tab"
                                >帖子({{ UserView.posts }})</a>
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="user-content">
                    <div class="tab-content" id="userTabContent">
                        <div
                            class="tab-pane fade show active"
                            id="description"
                            role="tabpanel"
                            aria-labelledby="userTab"
                            v-html="UserView.motto"
                        ></div>
                        <div
                            class="tab-pane fade show"
                            id="posts"
                            role="tabpanel"
                            aria-labelledby="userTab"
                        >
                            <template v-for="(d, i) in posts.data" v-bind:key="i">
                                <div style="padding: 20px; border-bottom: 1px solid #c1c3c5">
                                    <h4>
                                        <router-link
                                            :to="{ name: 'DiscussShow', params: { id: d.id } }"
                                        >{{ d.title }}</router-link>
                                    </h4>
                                    <div class="card-description">
                                        <template v-if="d.toplevel > 1">
                                            <span
                                                class="badge badge-pill badge-square badge-danger"
                                                style="margin-right: 3px"
                                            >置顶</span>
                                        </template>
                                        {{ d.author }} @
                                        <span
                                            class="vtooltip"
                                        >
                                            {{ getFormatDate(d.date) }}
                                            <span
                                                class="tooltiptext"
                                            >{{ getFormatDate(d.date, 0) }}</span>
                                        </span>
                                    </div>
                                </div>
                            </template>
                            <ul class="pagination">
                                <li class="page-item">
                                    <a class="page-link" @click="getPosts(1)" href="javascript:;">
                                        <i class="fas fa-chevron-left"></i>
                                    </a>
                                </li>
                                <li class="page-item" v-if="posts.currentPage > 1">
                                    <a
                                        class="page-link"
                                        @click="getPosts(posts.currentPage - 1)"
                                        href="javascript:;"
                                    >{{ posts.currentPage - 1 }}</a>
                                </li>
                                <li class="page-item active">
                                    <a class="page-link" href="javascript:;">{{ posts.currentPage }}</a>
                                </li>
                                <li class="page-item" v-if="posts.currentPage < posts.totalPage">
                                    <a
                                        class="page-link"
                                        @click="getPosts(posts.currentPage + 1)"
                                        href="javascript:;"
                                    >{{ posts.currentPage + 1 }}</a>
                                </li>
                                <li class="page-item">
                                    <a
                                        class="page-link"
                                        @click="getPosts(posts.totalPage)"
                                        href="javascript:;"
                                    >
                                        <i class="fas fa-chevron-right"></i>
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3 col-sm-12 order-md-2 order-1">
            <template v-if="$store.state.loginUser.uname == $route.params.id">
                <ul class="contest-menu">
                    <li>
                        <router-link :to="{ name: 'UserInfo', params: { id: $route.params.id } }">
                            <i class="far fa-user"></i>个人信息
                        </router-link>
                    </li>
                    <li>
                        <router-link :to="{ name: 'UserModify', params: { id: $route.params.id } }">
                            <i class="fas fa-cog"></i>信息修改
                        </router-link>
                    </li>
                    <li>
                        <router-link :to="{ name: 'UserMessage' }">
                            <i class="far fa-envelope"></i>站内私信
                        </router-link>
                    </li>
                </ul>
            </template>
        </div>
    </div>
</template>

<style scoped>
.profile .stats .posts {
    margin: 1rem;
}
.profile .lead {
    font-size: 1.1rem;
}
.user-info {
    background-image: url(../../assets/bg5.jpg);
    background-position: center center;
    background-size: cover;
    color: #fff !important;
}
.user-info h3 {
    color: #fff !important;
}
.user-content {
    padding: 0.7em 0.9375rem;
    background-color: #fff;
}
</style>

<script>
import Swal from 'sweetalert2'
import showdown from 'showdown'
import showdownKatex from 'showdown-katex'
import Prism from 'prismjs'
import '../../statics/line-number.js'
import 'prismjs/components/prism-python.js'
import CodeEditor from '../../components/codeEditor.vue';
const converter = new showdown.Converter({
    extensions: [
        showdownKatex({
            throwOnError: true,
            displayMode: true,
            errorColor: '#1500ff',
            delimiters: [
                { left: "$", right: "$", display: false },
                { left: "$$", right: "$$", display: true },
            ]
        }),
    ],
})
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
            UserView: {
                id: 0,
                username: "加载中",
                email: "加载中",
                motto: "加载中",
                rating: "加载中",
                privilege: "加载中",
                reg_time: "加载中",
                posts: 0,
                solved: 0,
            },
            posts: {
                data: [],
                totalPage: 1,
                currentPage: 1,
            },
        }
    },
    mounted() {
        const _t = this
        _t.$store.commit('changeTitle', '加载中')
        _t.$axios.get(`${_t.$store.state.backendURL}/api/user/${_t.$route.params.id}/`).then((res) => {
            _t.UserView = res.data
            _t.$store.commit('changeTitle', `用户${_t.UserView.username}`)
            setTimeout(() => { Prism.highlightAll() }, 100)
            _t.getPosts(1)
        }).catch((error) => {
            Toast.fire(
                'Oops',
                error.message,
                'error',
            )
        })
    },
    methods: {
        getPosts(page) {
            let _t = this
            let pathfix = `?page=${page}&user=${this.UserView.username}`
            _t.$axios.get(`${_t.$store.state.backendURL}/api/discuss/list/${pathfix}`).then((res) => {
                _t.posts = res.data
            }).catch((error) => {
                Toast.fire(
                    'Oops',
                    error.message,
                    'error',
                )
            })
        },
        getFormatDate(e, k = 1) {
            return k ? this.$moment(e).fromNow() : this.$moment(e).format("YYYY-MM-DD HH:mm:ss")
        }
    },
    components: {
        CodeEditor
    }
}
</script>
