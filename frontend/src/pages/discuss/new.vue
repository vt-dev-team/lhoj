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
                        <input type="text" class="form-control" v-model="PostTitle" />
                    </div>
                    <div class="form-group line-numbers">
                        <label>内容</label>
                        <textarea id="PostEditor"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
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
            PostEditor: '',
            PostTitle: '',
            nowTime: moment().format("YYYY-MM-DD HH:mm:ss"),
            nowTimeSetter: '',
        }
    },
    mounted() {
        const _t = this
        _t.nowTimeSetter = setInterval(() => { _t.getNowTime() }, 1000)
        _t.$store.commit('changeTitle', '新建讨论')
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
            hideIcons: ["guide", "heading", "side-by-side", "fullscreen"],
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
            param.append('title', _t.PostTitle)
            param.append('content', _t.PostEditor.value())
            param.append('section', _t.$route.query.section)
            _t.$axios.post(`${_t.$store.state.backendURL}/api/discuss/post/new/`, param).then((res) => {
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
                        _t.$router.push({
                            name: "DiscussShow",
                            params: {
                                id: res.data.post
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
