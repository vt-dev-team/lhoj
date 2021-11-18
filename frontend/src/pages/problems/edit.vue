<template>
    <div class="row">
        <div class="col-md-8 col-sm-12 order-md-1 order-2">
            <div class="card">
                <div class="card-body">
                    <form @submit="EditProblem">
                        <div class="form-group">
                            <label>标题</label>
                            <input type="text" class="form-control" v-model="ProblemView.title" />
                        </div>
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label>时间限制(ms)</label>
                                    <input
                                        type="text"
                                        class="form-control"
                                        v-model="ProblemView.time_limit"
                                    />
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label>空间限制(KiB)</label>
                                    <input
                                        type="text"
                                        class="form-control"
                                        v-model="ProblemView.memory_limit"
                                    />
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label class="vtooltip">
                                        测评方法
                                        <span class="tooltiptext">仅显示，具体配置在测试数据中</span>
                                    </label>
                                    <select v-model="ProblemView.judge_type" class="form-control">
                                        <option value="0">传统</option>
                                        <option value="1">Special Judge</option>
                                        <option value="2">提交答案</option>
                                        <option value="3">交互</option>
                                        <option value="4">程序填空</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>内容</label>
                            <textarea id="PostEditor"></textarea>
                        </div>
                        <div class="form-group">
                            <label for="postTitle">标签(英文,隔开)</label>
                            <input type="text" class="form-control" v-model="ProblemView.tags" />
                        </div>
                        <div class="form-group">
                            <label for="postTitle">算法(英文,隔开)</label>
                            <input
                                type="text"
                                class="form-control"
                                v-model="ProblemView.algorithms"
                            />
                        </div>
                        <button class="btn btn-primary" @click="submitCode" v-if="!isSubmit">提交</button>
                        <button class="btn btn-primary" type="button" disabled v-else>
                            <span
                                class="spinner-border spinner-border"
                                role="status"
                                aria-hidden="true"
                            ></span>
                            提交
                        </button>
                    </form>
                </div>
            </div>
        </div>
        <div class="col-md-4 col-sm-12 order-md-2 order-1">
            <template v-if="($store.state.loginUser.privilege & 2048) > 0">
                <ul class="contest-menu">
                    <li>
                        <router-link
                            :to="{ name: 'ProblemShow', params: { id: $route.params.id } }"
                        >
                            <i class="fas fa-eye"></i>题目查看
                        </router-link>
                    </li>
                    <li>
                        <router-link
                            :to="{ name: 'ProblemEdit', params: { id: $route.params.id } }"
                        >
                            <i class="fas fa-edit"></i>题目编辑
                        </router-link>
                    </li>
                    <li>
                        <router-link
                            :to="{ name: 'ProblemData', params: { id: $route.params.id } }"
                        >
                            <i class="fas fa-database"></i>数据配置
                        </router-link>
                    </li>
                </ul>
            </template>
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
            judge_type: ['传统', 'Special Judge', '提交答案', '交互', '程序填空'],
            ProblemView: {
                id: 0,
                time_limit: 0,
                memory_limit: 0,
                judge_type: 0,
                title: "加载中",
                content: "加载中",
                author: "加载中",
                pub_date: "加载中"
            },
            contest: 0,
            code_content: "",
        }
    },
    mounted() {
        const _t = this
        if ((_t.$store.state.loginUser.privilege & 2048) === 0)
            _t.$router.replace('/error/404')
        _t.$store.commit('changeTitle', '加载中')
        _t.contest = Number(_t.$route.query.contest) != NaN ? Number(_t.$route.query.contest) : 0
        _t.$axios.get(`${_t.$store.state.backendURL}/api/problem/${_t.$route.params.id}/`).then((res) => {
            _t.ProblemView = res.data
            _t.$store.commit('changeTitle', `题目编辑 #${_t.$route.params.id} ${_t.ProblemView.title}`)
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
            _t.PostEditor.value(_t.ProblemView.content)
        }).catch((error) => {
            Toast.fire(
                'Oops',
                error.message,
                'error',
            )
            _t.ProblemView = {
                id: 0,
                time_limit: 0,
                memory_limit: 0,
                judge_type: 0,
                title: "加载失败",
                content: `<h3>在请求后端时遇到错误</h3><p>${error.message}</p>`,
                author: "加载失败",
                pub_date: "加载失败"
            }
            _t.$store.commit('changeTitle', `#${_t.$route.params.id} ${_t.ProblemView.title}`)
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
        EditProblem(e) {
            e.preventDefault()
            let _t = this
            _t.isSubmit = true
            let param = new URLSearchParams()
            param.append('title', _t.ProblemView.title)
            param.append('content', _t.PostEditor.value())
            param.append('time_limit', _t.ProblemView.time_limit)
            param.append('memory_limit', _t.ProblemView.memory_limit)
            param.append('judge_type', _t.ProblemView.judge_type)
            param.append('tags', _t.ProblemView.tags)
            param.append('algorithm', _t.ProblemView.algorithms)
            _t.$axios.post(`${_t.$store.state.backendURL}/api/problem/${_t.ProblemView.id}/edit/`, param).then((res) => {
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
