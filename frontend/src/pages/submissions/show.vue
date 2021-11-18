<template>
    <div>
        <div class="row">
            <div class="col-md-8 col-sm-12">
                <div class="card">
                    <div class="card-body">
                        <h3>
                            <span
                                class="status-result"
                                :style="`color:${results[SubmissionView.result].color}`"
                            >
                                <i
                                    :class="`fas fa-${results[SubmissionView.result].icon} resultIcon`"
                                ></i>
                                {{ results[SubmissionView.result].val }}
                            </span>
                            得分:
                            <span
                                :class="`score_${Math.floor(SubmissionView.score / 10)}`"
                                style="font-weight: 500"
                            >{{ SubmissionView.score }}</span>pts
                        </h3>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body content">
                        <h3>
                            测试点信息
                            <div
                                class="spinner-grow"
                                :class="`score_${Math.floor(SubmissionView.score / 10)}`"
                                role="status"
                                v-if="SubmissionView.result <= 2"
                            >
                                <span class="sr-only">Loading...</span>
                            </div>
                        </h3>
                        <pre v-if="SubmissionView.mes"><code class="language-plain">{{ SubmissionView.mes }}</code></pre>
                        <div style="max-height: 300px; overflow:auto">
                            <table class="table">
                                <thead>
                                    <th></th>
                                    <th>状态</th>
                                    <th>时间</th>
                                    <th>空间</th>
                                </thead>
                                <tbody>
                                    <tr v-for="(k, i) in datas" v-bind:key="i">
                                        <td>#{{ i + 1 }}</td>
                                        <td>
                                            <span
                                                class="status-result vtooltip"
                                                :style="`color:${results[k.res].color}`"
                                            >
                                                <i
                                                    :class="`fas fa-${results[k.res].icon} resultIcon`"
                                                ></i>
                                                {{ results[k.res].val }}
                                                <span
                                                    class="tooltiptext"
                                                    v-if="k.mes"
                                                >{{ k.mes }}</span>
                                            </span>
                                        </td>
                                        <td>{{ k.time }}ms</td>
                                        <td>{{ k.memory }}KB</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <template v-if="SubmissionView.code">
                            <h3>代码</h3>
                            <pre class="line-numbers"><code class="language-python">{{ SubmissionView.code }}</code></pre>
                        </template>
                    </div>
                </div>
            </div>
            <div class="col-md-4 col-sm-12">
                <template v-if="SubmissionView.contest > 0">
                    <ul class="contest-menu">
                        <li>
                            <router-link
                                :to="{ name: 'ContestShow', params: { id: SubmissionView.contest } }"
                            >比赛#{{ SubmissionView.contest }} 总览</router-link>
                        </li>
                        <li>
                            <router-link
                                :to="{ name: 'SubmissionSet', query: { contest: SubmissionView.contest } }"
                            >评测记录</router-link>
                        </li>
                        <li>
                            <router-link
                                :to="{ name: 'ContestRank', params: { id: SubmissionView.contest } }"
                            >排名</router-link>
                        </li>
                    </ul>
                    <br />
                </template>
                <div class="card">
                    <div class="card-body">
                        <h5>评测信息</h5>
                        <table style="width: 100%">
                            <tr>
                                <th width="30%">状态</th>
                                <td width="70%">
                                    <span
                                        class="status-result"
                                        :style="`color:${results[SubmissionView.result].color}`"
                                    >
                                        <i
                                            :class="`fas fa-${results[SubmissionView.result].icon} resultIcon`"
                                        ></i>
                                        {{ results[SubmissionView.result].val }}
                                    </span>
                                </td>
                            </tr>
                            <tr>
                                <th width="30%">题目</th>
                                <td width="70%">
                                    <router-link
                                        :to="{ name: 'ProblemShow', params: { id: SubmissionView.problem } }"
                                    >#{{ SubmissionView.problem }}</router-link>
                                </td>
                            </tr>
                            <tr>
                                <th width="30%">提交者</th>
                                <td width="70%">
                                    <router-link
                                        :to="{ name: 'UserInfo', params: { id: SubmissionView.user_id } }"
                                    >{{ SubmissionView.user_id }}</router-link>
                                </td>
                            </tr>
                            <tr>
                                <th width="30%">评测机</th>
                                <td width="70%">{{ SubmissionView.judger }}</td>
                            </tr>
                            <tr>
                                <th width="30%">时间</th>
                                <td width="70%">{{ SubmissionView.time }}ms</td>
                            </tr>
                            <tr>
                                <th width="30%">内存</th>
                                <td width="70%">{{ SubmissionView.memory }}KB</td>
                            </tr>
                            <tr>
                                <th width="30%">提交时间</th>
                                <td width="70%">{{ SubmissionView.date }}</td>
                            </tr>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Swal from 'sweetalert2'
import Prism from 'prismjs'
import '../../statics/line-number.js'
import 'prismjs/components/prism-python.js'
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
            SubmissionView: {
                id: 0,
                user_id: '加载中',
                code: '',
                time: 0,
                memory: 0,
                score: 0,
                result: 0,
                problem: 1,
                cases: {},
                contest: 0,
                judger: '',
                date: '加载中',
                mes: '',
            },
            datas: [],
            info: "",
            results: [{ id: '0', color: '#6cf', val: 'Pending', icon: 'hourglass' },
            { id: '1', color: '#6cf', val: 'Pending Rejudge', icon: 'hourglass' },
            { id: '2', color: '#6cf', val: 'Judging', icon: 'hourglass' },
            { id: '3', color: '#25ad40', val: 'Accepted', icon: 'check' },
            { id: '4', color: '#ff4f4f', val: 'Wrong Answer', icon: 'times' },
            { id: '5', color: '#f4a460', val: 'Time Limit Exceeded', icon: 'clock' },
            { id: '6', color: '#f4a460', val: 'Memory Limit Exceeded', icon: 'database' },
            { id: '7', color: '#f4a460', val: 'Output Limit Exceeded', icon: 'print' },
            { id: '8', color: '#9932cc', val: 'Runtime Error', icon: 'bomb' },
            { id: '9', color: 'grey', val: 'Unknown Error', icon: 'cog' },
            { id: '10', color: 'grey', val: 'System Error', icon: 'cog' },
            { id: '11', color: '#ff4f4f', val: 'Unaccepted', icon: 'times' }]
        }
    },
    mounted() {
        const _t = this
        _t.$store.commit('changeTitle', `提交记录 #${_t.$route.params.id}`)
        _t.getSubmission()
        let p = setInterval(() => {
            if (_t.SubmissionView.result > 2 || _t.$route.params.id == undefined)
                clearInterval(p)
            _t.getSubmission()
        }, 3000)
    },
    methods: {
        getSubmission() {
            let _t = this
            if (_t.$route.params.id == undefined)
                return
            _t.$axios.get(`${_t.$store.state.backendURL}/api/submission/${_t.$route.params.id}/`).then((res) => {
                _t.SubmissionView = res.data
                try {
                    let parsedData = JSON.parse(_t.SubmissionView.cases)
                    _t.datas = parsedData["datas"]
                    if (parsedData["mes"])
                        _t.SubmissionView.mes = parsedData["mes"]
                }
                catch (e) {
                    console.log("Cannot parse cases")
                }
                setTimeout(() => { Prism.highlightAll() }, 100)
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
