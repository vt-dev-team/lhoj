<template>
    <div>
        <div class="row">
            <div class="col-md-8 col-sm-12 order-md-1 order-2">
                <div class="nav-wrapper">
                    <ul class="nav nav-pills nav-fill flex-column flex-md-row">
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
                                :class="{ 'disabled': !($store.state.loginUser.privilege & 2) }"
                                data-toggle="tab"
                                role="tab"
                                aria-controls="problem-submit"
                                href="#problem-submit"
                            >提交代码</a>
                        </li>
                    </ul>
                </div>
                <div class="card">
                    <div class="card-body">
                        <div class="tab-content">
                            <div
                                class="tab-pane fade show active content line-numbers"
                                id="problem-show"
                                role="tabpanel"
                                v-html="ProblemView.content"
                            ></div>
                            <div class="tab-pane fade" id="problem-submit" role="tabpanel">
                                <code-editor v-model="code_content" style="height: 600px"></code-editor>
                                <div class="divider"></div>
                                <button
                                    class="btn btn-primary"
                                    @click="submitCode"
                                    v-if="!isSubmit"
                                >提交</button>
                                <button class="btn btn-primary" type="button" disabled v-else>
                                    <span
                                        class="spinner-border spinner-border"
                                        role="status"
                                        aria-hidden="true"
                                    ></span>
                                    提交中
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                <br />
            </div>
            <div class="col-md-4 col-sm-12 order-md-2 order-1">
                <template v-if="contest">
                    <ul class="contest-menu">
                        <li>
                            <router-link
                                :to="{ name: 'ContestShow', params: { id: contest } }"
                            >比赛#{{ contest }} 总览</router-link>
                        </li>
                        <li>
                            <router-link
                                :to="{ name: 'SubmissionSet', query: { contest: contest } }"
                            >评测记录</router-link>
                        </li>
                        <li>
                            <router-link :to="{ name: 'ContestRank', params: { id: contest } }">排名</router-link>
                        </li>
                    </ul>
                    <br />
                </template>
                <div class="card">
                    <div class="card-body">
                        <h5>题目附件</h5>
                        <a
                            @click="downloadAttachment"
                            href="javascript:;"
                        >点击下载(attachment{{ ProblemView.id }}.zip)</a>
                    </div>
                </div>
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
                <div class="card">
                    <div class="card-body">
                        <h5>标签</h5>
                        <router-link
                            v-for="(t, i) in ProblemView.algorithms"
                            v-bind:key="i"
                            v-show="showAlgorithms"
                            :class="`badge badge-primary problem-tag`"
                            :to="{ name: 'ProblemSet', query: { search: t } }"
                        >{{ t }}</router-link>
                        <router-link
                            v-for="(t, i) in ProblemView.tags"
                            v-bind:key="i"
                            :class="`badge badge-${t.color} problem-tag`"
                            :to="{ name: 'ProblemSet', query: { search: t.label } }"
                        >{{ t.label }}</router-link>
                        <span
                            class="toggleAlgorithm text-center"
                            @click="showAlgorithms = 1 - showAlgorithms"
                        >
                            <i
                                class="fas"
                                :class="{ 'fa-chevron-down': !showAlgorithms, 'fa-chevron-up': showAlgorithms }"
                            ></i>
                            <template v-if="showAlgorithms">隐藏</template>
                            <template v-else>显示</template>算法标签
                        </span>
                    </div>
                </div>
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
                            :to="{ name: 'SubmissionSet', query: { problem: $route.params.id, contest: contest } }"
                        >
                            <i class="fas fa-list-ol"></i>评测记录
                        </router-link>
                    </li>
                    <li>
                        <router-link
                            :to="{ name: 'DiscussList', query: { section: 'P' + $route.params.id } }"
                        >
                            <i class="fas fa-comments"></i>讨论
                        </router-link>
                    </li>
                    <template v-if="($store.state.loginUser.privilege & 2048) > 0">
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
                    </template>
                </ul>
            </div>
        </div>
    </div>
</template>

<style scoped>
.toggleAlgorithm {
    display: block;
    width: 100%;
    margin-top: 10px;
    color: #aaabac;
    transition: all 0.2s;
}
.toggleAlgorithm:hover {
    cursor: pointer;
    color: #686868;
}
.toggleAlgorithm i {
    margin-right: 5px;
}
</style>

<script>
import Swal from 'sweetalert2'
import showdown from 'showdown'
import showdownKatex from 'showdown-katex'
import Prism from 'prismjs'
import 'prismjs/components/prism-python.js'
import '../../statics/line-number.js'
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
        }), ,
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
                pub_date: "加载中",
                tags: "",
                algorithms: "",
            },
            contest: 0,
            code_content: "",
            showAlgorithms: false,
        }
    },
    mounted() {
        const _t = this
        _t.$store.commit('changeTitle', '加载中')
        _t.contest = Number(_t.$route.query.contest) != NaN ? Number(_t.$route.query.contest) : 0
        _t.$axios.get(`${_t.$store.state.backendURL}/api/problem/${_t.$route.params.id}/`).then((res) => {
            _t.ProblemView = res.data
            _t.ProblemView.content = converter.makeHtml(_t.ProblemView.content)
            _t.ProblemView.tags = _t.labelFormat(_t.ProblemView.tags.split(","))
            _t.ProblemView.algorithms = _t.ProblemView.algorithms.split(",")
            _t.$store.commit('changeTitle', `#${_t.$route.params.id} ${_t.ProblemView.title}`)
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
            _t.$store.commit('changeTitle', `#${_t.$route.params.id} ${_t.ProblemView.title}`)
        })
    },
    methods: {
        hashCode(str) {
            var hash = 0
            for (var i = 0; i < str.length; i++) {
                hash = ~~(((hash << 5) - hash) + str.charCodeAt(i))
            }
            return hash
        },
        labelFormat(labels) {
            let res = []
            let colors = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']
            for (var i = 0; i < labels.length; ++i) {
                let labelsi = labels[i]
                let color = colors[this.hashCode(labelsi) % colors.length]
                res.push({
                    color: color,
                    label: labelsi
                })
            }
            return res
        },
        showError(t, m) {
            let _t = this
            Toast.fire(
                t,
                m,
                'error'
            )
        },
        submitCode() {
            let _t = this
            let param = new URLSearchParams()
            _t.isSubmit = true
            param.append('problem', _t.ProblemView.id)
            param.append('code', _t.code_content)
            param.append('contest', _t.contest)
            _t.$axios.post(`${_t.$store.state.backendURL}/api/submission/submit/`, param).then((res) => {
                _t.isSubmit = false
                if (res.data.code != 0)
                    _t.showError("Oops", res.data.mes)
                else {
                    Swal.fire(
                        "提交成功",
                        res.data.mes,
                        'success'
                    ).then(() => {
                        _t.$router.push({
                            name: 'SubmissionShow',
                            params: {
                                id: res.data.submission.id
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
        },
        downloadAttachment() {
            let _t = this
            _t.$axios({
                url: `${_t.$store.state.backendURL}/api/problem/${_t.ProblemView.id}/attachments/`,
                method: 'post',
                headers: {
                    responseType: "blob"
                }
            }).then((res) => {
                if (res.headers["content-type"] == "application/zip") {
                    let fileName = `attachments${_t.ProblemView.id}.zip`
                    if (window.navigator && window.navigator.msSaveOrOpenBlob) {
                        const blob = new Blob([res.data], { type: 'application/zip' })
                        window.navigator.msSaveOrOpenBlob(blob, fileName)
                    } else {
                        /* 火狐谷歌的文件下载方式 */
                        const blob = new Blob([res.data], { type: 'application/zip' })
                        const url = window.URL.createObjectURL(blob)
                        const link = document.createElement('a') // 创建a标签
                        link.href = url
                        link.download = fileName // 文件重命名，若无需重命名，将该行删去
                        link.click()
                        URL.revokeObjectURL(url) // 释放内存
                    }
                }
                else {
                    Toast.fire(
                        'Oops',
                        "出错了",
                        'error',
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
    },
    components: {
        CodeEditor
    }
}
</script>
