<template>
    <div>
        <div class="row">
            <div class="col-md-8 col-sm-12">
                <div class="card">
                    <div class="card-body">
                        <div class="tab-content">
                            <div
                                class="tab-pane fade show active content"
                                id="problem-show"
                                role="tabpanel"
                                v-html="ProblemView.content"
                            ></div>
                            <div class="tab-pane fade" id="problem-submit" role="tabpanel" style="height: 600px">
                                <code-editor></code-editor>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4 col-sm-12">
                <div class="card">
                    <div class="card-body" style="padding: 0;">
                        <ul class="nav nav-tabs d-flex flex-column">
                            <li class="nav-item">
                                <a
                                    class="nav-link active"
                                    data-toggle="tab"
                                    role="tab"
                                    aria-controls="problem-show"
                                    href="#problem-show"
                                >题面查看</a>
                            </li>
                            <li class="nav-item">
                                <a
                                    class="nav-link"
                                    data-toggle="tab"
                                    role="tab"
                                    aria-controls="problem-submit"
                                    href="#problem-submit"
                                >提交代码</a>
                            </li>
                        </ul>
                    </div>
                </div>
                <br />
                <div class="card">
                    <div class="card-body">
                        <h5>题目信息</h5>
                        <table style="width: 100%">
                            <tr>
                                <th width="30%">时间限制</th>
                                <td width="70%">{{ ProblemView.time_limit }}ms</td>
                            </tr>
                            <tr>
                                <th>空间限制</th>
                                <td>{{ ProblemView.memory_limit }}KB</td>
                            </tr>
                            <tr>
                                <th>评测方式</th>
                                <td>{{ judge_type[ProblemView.judge_type] }}</td>
                            </tr>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.content h1,
.content h2,
.content h3,
.content h4,
.content h5,
.content h6 {
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}
</style>

<style scoped>
.nav.nav-tabs {
    margin-bottom: 0;
}
.nav.nav-tabs .nav-item .nav-link {
    border-radius: 0;
}
.nav.nav-tabs .nav-item .nav-link:hover {
    border-bottom: 0;
    border-left: 1px solid #611f6a;
    color: #611f6a;
}
.nav.nav-tabs .nav-item .nav-link.active,
.nav.nav-tabs .nav-item .nav-link.active:hover {
    border-bottom: 0;
    border-left: 2px solid #611f6a;
    border-color: #611f6a;
    font-weight: bold;
    color: #611f6a;
}
</style>

<script>
import axios from 'axios'
import Swal from 'sweetalert2'
import showdown from 'showdown'
import showdownKatex from 'showdown-katex'
import Prism from 'prismjs'
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
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000
})
export default {
    data() {
        return {
            judge_type: ['传统', 'Special Judge', '提交答案', '交互'],
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
            code_content: "",
        }
    },
    mounted() {
        const _t = this
        _t.$store.commit('changeTitle', '加载中')
        axios.get(`${_t.$store.state.backendURL}/problem/${_t.$route.params.id}/`).then((res) => {
            _t.ProblemView = res.data
            _t.ProblemView.content = converter.makeHtml(_t.ProblemView.content)
            _t.$store.commit('changeTitle', _t.ProblemView.title)
            setTimeout(() => { Prism.highlightAll() }, 100)
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
            _t.$store.commit('changeTitle', _t.ProblemView.title)
        })
    },
    components: {
        CodeEditor
    }
}
</script>
