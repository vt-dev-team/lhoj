<template>
    <div>
        <div class="card">
            <div class="card-body">
                <form @submit="NewPost">
                    <div class="form-group">
                        <label>标题</label>
                        <input type="text" class="form-control" v-model="Title" />
                    </div>
                    <div class="form-group">
                        <label>开始时间</label>
                        <div class="input-group">
                            <div class="input-group-prepend">
                                <span class="input-group-text">
                                    <i class="far fa-clock"></i>
                                </span>
                            </div>
                            <input
                                class="flatpickr datetimepicker form-control"
                                type="text"
                                id="startTime"
                                v-model="start_time"
                                placeholder="开始时间"
                            />
                        </div>
                    </div>
                    <div class="form-group">
                        <label>结束时间</label>
                        <div class="input-group">
                            <div class="input-group-prepend">
                                <span class="input-group-text">
                                    <i class="far fa-clock"></i>
                                </span>
                            </div>
                            <input
                                class="flatpickr datetimepicker form-control"
                                type="text"
                                v-model="end_time"
                                id="endTime"
                                placeholder="结束时间"
                            />
                        </div>
                    </div>
                    <div class="form-group">
                        <label>比赛模式</label>
                        <select class="form-control" v-model="tp">
                            <option value="0">ACM</option>
                            <option value="1">OI</option>
                            <option value="2">自由训练</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>描述</label>
                        <textarea id="PostEditor"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="postTitle">题目(英文,隔开)</label>
                        <input type="text" class="form-control" v-model="problems" />
                    </div>
                    <button type="submit" class="btn btn-primary" :disabled="isSubmitting">Submit</button>
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
import flatpickr from "flatpickr"
import 'prismjs/components/prism-python.js'
import SimpleMDE from 'simplemde'
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
            Title: '',
            start_time: this.$moment().format("YYYY-MM-DD HH:mm"),
            end_time: this.$moment().format("YYYY-MM-DD HH:mm"),
            tp: 0,
            problems: '',
            isSubmitting: false,
        }
    },
    mounted() {
        const _t = this
        _t.$store.commit('changeTitle', '新建比赛')
        if ((_t.$store.state.loginUser.privilege & 512) === 0)
            _t.$router.replace('/error/404')
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
        flatpickr(document.getElementById("startTime"), {
            enableTime: true,
            dateFormat: "Y-m-d H:i",
        })
        flatpickr(document.getElementById("endTime"), {
            enableTime: true,
            dateFormat: "Y-m-d H:i",
        })
    },
    methods: {
        NewPost(e) {
            e.preventDefault()
            let _t = this
            let param = new URLSearchParams()
            param.append('title', _t.Title)
            param.append('content', _t.PostEditor.value())
            param.append('start_time', _t.start_time)
            param.append('tp', _t.tp)
            param.append('end_time', _t.end_time)
            param.append('problems', _t.problems)
            _t.isSubmitting = true
            _t.$axios.post(`${_t.$store.state.backendURL}/api/contest/new/`, param).then((res) => {
                _t.isSubmitting = false
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
                            name: "ContestShow",
                            params: {
                                id: res.data.id
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
