<template>
    <div>
        <div class="card card-topic">
            <div class="card-header">
                <router-link
                    :to="{ name: 'UserInfo', params: { id: PostView.author } }"
                >{{ PostView.author }}</router-link>@
                <span class="vtooltip">
                    {{ getFormatDate(PostView.date) }}
                    <span
                        class="tooltiptext"
                    >{{ getFormatDate(PostView.date, 0) }}</span>
                </span>
                <span
                    class="float-right text-grey"
                    v-if="(PostView.author == $store.state.loginUser.uname) || (($store.state.loginUser.privilege & 8192) > 0)"
                >
                    <router-link :to="{ name: 'DiscussEdit', params: { id: $route.params.id } }">编辑</router-link>&nbsp;
                    <a @click="deletePost()" href="javascript:;">删除</a>
                </span>
            </div>
            <div class="card-body">
                <div class="card-text line-numbers" v-html="PostView.content"></div>
            </div>
        </div>
        <div class="divider"></div>
        <template v-for="(c,i) in CommentList" v-bind:key="i">
            <div class="card">
                <div class="card-header">
                    <router-link :to="{ name: 'UserInfo', params: { id: c.author } }">{{ c.author }}</router-link>@
                    <span class="vtooltip">
                        {{ getFormatDate(c.date) }}
                        <span
                            class="tooltiptext"
                        >{{ getFormatDate(c.date, 0) }}</span>
                    </span>
                    <span
                        class="float-right text-grey"
                        v-if="(c.author == $store.state.loginUser.uname) || (($store.state.loginUser.privilege & 8192) > 0)"
                    >
                        <router-link
                            :to="{ name: 'DiscussEdit', params: { id: $route.params.id } }"
                        >编辑</router-link>&nbsp;
                        <a @click="deleteComment(c.id)" href="javascript:;">删除</a>
                    </span>
                </div>
                <div class="card-body">
                    <div class="card-text line-numbers" v-html="c.content"></div>
                </div>
            </div>
        </template>
        <br />
        <ul class="pagination">
            <li class="page-item">
                <a class="page-link" @click="getComments(1)" href="javascript:;">
                    <i class="fas fa-chevron-left"></i>
                </a>
            </li>
            <li class="page-item" v-if="currentPage > 1">
                <a
                    class="page-link"
                    @click="getComments(currentPage - 1)"
                    href="javascript:;"
                >{{ currentPage - 1 }}</a>
            </li>
            <li class="page-item active">
                <a class="page-link">{{ currentPage }}</a>
            </li>
            <li class="page-item" v-if="currentPage < totalPage">
                <a
                    class="page-link"
                    @click="getComments(currentPage + 1)"
                    href="javascript:;"
                >{{ currentPage + 1 }}</a>
            </li>
            <li class="page-item">
                <a class="page-link" @click="getComments(totalPage)" href="javascript:;">
                    <i class="fas fa-chevron-right"></i>
                </a>
            </li>
        </ul>
        <div class="card" v-if="$store.state.loginUser.uid !== -1">
            <div class="card-header">
                {{ $store.state.loginUser.uname }}
                @ {{ nowTime }}
            </div>
            <div class="card-body no-padding">
                <textarea id="commentEditor"></textarea>
                <a
                    href="javascript:;"
                    class="btn btn-primary"
                    style="margin: 10px"
                    @click="sendComment"
                >发射</a>
            </div>
        </div>
    </div>
</template>

<style>
.CodeMirror {
    height: 150px;
}
</style>

<script>
import Swal from 'sweetalert2'
import showdown from 'showdown'
import showdownKatex from 'showdown-katex'
import Prism from 'prismjs'
import 'prismjs/components/prism-python.js'
import '../../statics/line-number.js'
import SimpleMDE from 'simplemde'
import moment from 'moment'
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
            PostView: {
                id: 0,
                title: "加载中",
                content: "加载中",
                author: "加载中",
                pub_date: "加载中"
            },
            CommentList: [],
            commentEditor: '',
            currentPage: 1,
            nowTime: moment().format("YYYY-MM-DD HH:mm:ss"),
            nowTimeSetter: '',
            totalPage: 1
        }
    },
    mounted() {
        const _t = this
        _t.nowTimeSetter = setInterval(() => { _t.getNowTime() }, 1000)
        _t.$store.commit('changeTitle', '加载中')
        _t.$axios.get(`${_t.$store.state.backendURL}/api/discuss/post/${_t.$route.params.id}/?mode=post`).then((res) => {
            _t.PostView = res.data.post
            _t.PostView.content = converter.makeHtml(_t.PostView.content)
            _t.$store.commit('changeTitle', _t.PostView.title)
            setTimeout(() => { Prism.highlightAll() }, 100)
        }).catch((error) => {
            Toast.fire(
                'Oops',
                error.message,
                'error',
            )
            _t.PostView = {
                id: 0,
                title: "加载失败",
                content: `<h3>在请求后端时遇到错误</h3><p>${error.message}</p>`,
                author: "加载失败",
                pub_date: "加载失败"
            }
            _t.$store.commit('changeTitle', _t.PostView.title)
        })
        if (_t.$route.query.page)
            _t.currentPage = _t.$route.query.page
        _t.getComments(_t.currentPage)
        _t.loadEditor()
    },
    beforeUnmount() {
        clearInterval(this.nowTimeSetter)
    },
    methods: {
        loadEditor() {
            let _t = this
            _t.commentEditor = new SimpleMDE({
                element: document.getElementById("commentEditor"),
                previewRender: function (plainText, preview) { // Async method
                    setTimeout(() => {
                        preview.innerHTML = converter.makeHtml(plainText)
                        Prism.highlightAll()
                    }, 100)
                    return "Loading..."
                },
                spellChecker: false,
                hideIcons: ["guide", "heading", "side-by-side", "fullscreen"],
            })
        },
        getNowTime() {
            this.nowTime = moment().format("YYYY-MM-DD HH:mm:ss")
        },
        getFormatDate(e, k = 1) {
            return k ? this.$moment(e).fromNow() : this.$moment(e).format("YYYY-MM-DD HH:mm:ss")
        },
        getComments(page) {
            let _t = this
            _t.$router.replace(`?page=${page}`)
            _t.$axios.get(`${_t.$store.state.backendURL}/api/discuss/post/${_t.$route.params.id}/?mode=comment&page=${page}`).then((res) => {
                _t.CommentList = res.data.comments
                for (let i in _t.CommentList) {
                    _t.CommentList[i].content = converter.makeHtml(_t.CommentList[i].content)
                }
                _t.totalPage = res.data.totalPage
                _t.currentPage = res.data.currentPage
            }).catch((error) => {
                Toast.fire(
                    'Oops',
                    error.message,
                    'error',
                )
            })
        },
        deleteComment(e) {
            let _t = this
            Swal.fire({
                title: '真的要删除这个评论吗?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#db2828',
                confirmButtonText: '给老子删了!',
                cancelButtonColor: '#eee',
                cancelButtonText: '不敢!'
            }).then((result) => {
                if (result.value) {
                    _t.$axios.get(`${_t.$store.state.backendURL}/api/discuss/comment/${e}/delete/`).then((res) => {
                        if (res.data.code != 0) {
                            Toast.fire(
                                'Oops',
                                res.data.mes,
                                'error',
                            )
                        }
                        else {
                            Toast.fire(
                                '成功',
                                "删除成功",
                                'success',
                            ).then(() => {
                                _t.getComments(1)
                            })
                        }
                    }).catch((err) => {
                        Toast.fire(
                            'Oops',
                            "出现错误",
                            'error',
                        )
                    })
                }
            })
        },
        deletePost() {
            let _t = this
            Swal.fire({
                title: '真的要删除这篇讨论吗?',
                text: "连评论会被一起删除，不可恢复！",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#db2828',
                confirmButtonText: '给老子删了!',
                cancelButtonColor: '#eee',
                cancelButtonText: '不敢!'
            }).then((result) => {
                if (result.value) {
                    _t.$axios.get(`${_t.$store.state.backendURL}/api/discuss/post/${_t.$route.params.id}/delete/`).then((res) => {
                        if (res.data.code != 0) {
                            Toast.fire(
                                'Oops',
                                res.data.mes,
                                'error',
                            )
                        }
                        else {
                            Toast.fire(
                                '成功',
                                "删除成功",
                                'success',
                            ).then(() => {
                                _t.$router.push({
                                    name: "DiscussList"
                                })
                            })
                        }
                    }).catch((err) => {
                        Toast.fire(
                            'Oops',
                            "出现错误",
                            'error',
                        )
                    })
                }
            })
        },
        sendComment() {
            let _t = this
            let param = new URLSearchParams()
            param.append('post_id', _t.$route.params.id)
            param.append('content', _t.commentEditor.value())
            _t.$axios.post(`${_t.$store.state.backendURL}/api/discuss/comment/new/`, param).then((res) => {
                if (res.data.code != 0) {
                    Toast.fire(
                        'Oops',
                        res.data.mes,
                        'error',
                    )
                }
                else {
                    Toast.fire(
                        '成功',
                        "添加成功",
                        'success',
                    ).then(() => {
                        _t.commentEditor.value("")
                        _t.getComments(_t.totalPage)
                    })
                }
            }).catch((error) => {
                Toast.fire(
                    'Oops',
                    error.message,
                    'error',
                )
            })
        }
    }
}
</script>
