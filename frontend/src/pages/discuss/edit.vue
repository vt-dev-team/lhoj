<template>
    <div>
        <div class="card card-topic">
            <div class="card-header">
                {{ $store.state.loginUser.uname }}
                @ {{ nowTime }}
            </div>
            <div class="card-body">
                <form @submit="NewPost">
                    <div class="form-group">
                        <label for="postTitle">标题</label>
                        <input type="text" class="form-control" v-model="PostView.title" />
                    </div>
                    <div class="form-group">
                        <label for="postSection">版块</label>
                        <input type="text" class="form-control" v-model="PostView.section" disabled />
                    </div>
                    <div class="form-group" v-if="$store.state.loginUser.privilege & 8192 > 0">
                        <label for="postSection">置顶等级</label>
                        <input type="text" class="form-control" v-model="PostView.toplevel" />
                    </div>
                    <div class="form-group line-numbers">
                        <label>内容</label>
                        <textarea id="PostEditor"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary" :disabled="isLoading">Submit</button>
                </form>
            </div>
        </div>
    </div>
</template>

<style>
.CodeMirror {
    height: 300px;
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
            isLoading: true,
            PostView: {
                id: 0,
                title: "加载中",
                content: "加载中",
                author: "加载中",
                section: 0,
                pub_date: "加载中",
                toplevel: 0,
            },
            PostView: '',
            nowTime: moment().format("YYYY-MM-DD HH:mm:ss"),
            nowTimeSetter: '',
        }
    },
    mounted() {
        const _t = this
        _t.nowTimeSetter = setInterval(() => { _t.getNowTime() }, 1000)
        _t.$store.commit('changeTitle', '加载中')
        _t.$axios.get(`${_t.$store.state.backendURL}/api/discuss/post/${_t.$route.params.id}/?mode=post`).then((res) => {
            _t.isLoading = false
            _t.PostView = res.data.post
            _t.$store.commit('changeTitle', `编辑讨论 ${_t.PostView.title}`)
            _t.PostEditor = new SimpleMDE({
                element: document.getElementById("PostEditor"),
                previewRender: function (plainText, preview) { // Async method
                    setTimeout(() => {
                        preview.innerHTML = converter.makeHtml(plainText)
                        Prism.highlightAll()
                    }, 100)
                    return "Loading..."
                },
                spellChecker: false,
                hideIcons: ["guide", "side-by-side", "fullscreen"],
            })
            _t.PostEditor.value(_t.PostView.content)
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
    },
    beforeUnmount() {
        clearInterval(this.nowTimeSetter)
    },
    methods: {
        getNowTime() {
            this.nowTime = moment().format("YYYY-MM-DD HH:mm:ss")
        },
        NewPost(e) {
            e.preventDefault()
            let _t = this
            let param = new URLSearchParams()
            param.append('title', _t.PostView.title)
            param.append('content', _t.PostEditor.value())
            if (_t.$store.state.loginUser.privilege & 8192 > 0)
                param.append('toplevel', _t.PostView.toplevel)
            _t.$axios.post(`${_t.$store.state.backendURL}/api/discuss/post/${_t.$route.params.id}/edit/`, param).then((res) => {
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
                        "修改成功",
                        'success',
                    ).then(() => {
                        _t.$router.push({
                            name: "DiscussShow",
                            params: {
                                id: _t.$route.params.id
                            }
                        })
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
