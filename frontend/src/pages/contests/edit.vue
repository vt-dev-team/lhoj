<template>
    <div class="row">
        <div class="col-md-8 col-sm-12 order-md-1 order-2">
            <div class="card">
                <div class="card-body">
                    <form @submit="EditContest">
                        <div class="form-group">
                            <label>标题</label>
                            <input type="text" class="form-control" v-model="ContestView.title" />
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
                                    v-model="ContestView.start_time"
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
                                    v-model="ContestView.end_time"
                                    id="endTime"
                                    placeholder="结束时间"
                                />
                            </div>
                        </div>
                        <div class="form-group">
                            <label>比赛模式</label>
                            <select class="form-control" v-model="ContestView.tp">
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
                            <input type="text" class="form-control" v-model="ContestView.problems" />
                        </div>
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </form>
                </div>
            </div>
        </div>
        <div class="col-md-4 col-sm-12 order-md-2 order-1">
            <ul class="contest-menu">
                <li>
                    <router-link
                        :to="{ name: 'ContestShow', params: { id: ContestView.id } }"
                    >比赛#{{ ContestView.id }} 总览</router-link>
                </li>
                <li>
                    <router-link
                        :to="{ name: 'SubmissionSet', query: { contest: ContestView.id } }"
                    >评测记录</router-link>
                </li>
                <li>
                    <router-link :to="{ name: 'ContestRank', params: { id: ContestView.id } }">排名</router-link>
                </li>
                <li v-if="($store.state.loginUser.privilege & 4096) > 0">
                    <router-link :to="{ name: 'ContestEdit', params: { id: ContestView.id } }">编辑比赛</router-link>
                </li>
            </ul>
            <br />
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
import flatpickr from "flatpickr"
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
            isSubmit: false,
            ContestView: {
                id: this.$route.params.id,
                description: '',
                title: '',
                start_time: '',
                end_time: '',
                tp: 0,
                problems: '',
                privilege: 0,
            },
            code_content: "",
        }
    },
    mounted() {
        const _t = this
        if ((_t.$store.state.loginUser.privilege & 4096) === 0)
            _t.$router.replace('/error/404')
        _t.$store.commit('changeTitle', '加载中')
        _t.$axios.get(`${_t.$store.state.backendURL}/api/contest/${_t.$route.params.id}/?notShowProblem=yes`).then((res) => {
            _t.ContestView = res.data.data
            _t.$store.commit('changeTitle', `编辑比赛 #${_t.$route.params.id} ${_t.ContestView.title}`)
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
            _t.PostEditor.value(_t.ContestView.description)
            _t.ContestView.start_time = _t.$moment(_t.ContestView.start_time).format("YYYY-MM-DD HH:mm")
            flatpickr(document.getElementById("startTime"), {
                enableTime: true,
                dateFormat: "Y-m-d H:i",
            })
            _t.ContestView.end_time = _t.$moment(_t.ContestView.end_time).format("YYYY-MM-DD HH:mm")
            flatpickr(document.getElementById("endTime"), {
                enableTime: true,
                dateFormat: "Y-m-d H:i",
            })
        }).catch((error) => {
            Toast.fire(
                'Oops',
                error.message,
                'error',
            )
            _t.ContestView = {
                id: _t.$route.params.id,
                title: '加载失败',
                start_time: '0',
                end_time: '0',
                tp: 0,
                problems: '',
                privilege: 0,
            }
            _t.$store.commit('changeTitle', `#${_t.$route.params.id} ${_t.ContestView.title}`)
        })
    },
    methods: {
        showError(t, m) {
            let _t = this
            Toast.fire(
                t,
                m,
                'error'
            )
        },
        EditContest(e) {
            e.preventDefault()
            let _t = this
            _t.isSubmit = true
            let param = new URLSearchParams()
            param.append('title', _t.ContestView.title)
            param.append('content', _t.PostEditor.value())
            param.append('start_time', _t.ContestView.start_time)
            param.append('tp', _t.ContestView.tp)
            param.append('end_time', _t.ContestView.end_time)
            param.append('problems', _t.ContestView.problems)
            _t.$axios.post(`${_t.$store.state.backendURL}/api/contest/${_t.ContestView.id}/edit/`, param).then((res) => {
                _t.isSubmit = false
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
                    )
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
