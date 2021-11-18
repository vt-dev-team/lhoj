<template>
    <div>
        <div class="row">
            <div class="col-md-8 col-sm-12">
                <div class="card">
                    <div class="card-body">
                        <h3>{{ ContestView.title }}</h3>
                        <span
                            class="badge badge-square badge-primary badge-pill"
                        >{{ contestTypes[ContestView.tp] }}</span>&nbsp;
                        <span class="vtooltip">
                            <span
                                class="badge badge-square badge-info"
                                v-if="!isStart(ContestView.start_time)"
                            >开始于{{ getFormatDate(ContestView.start_time) }}</span>
                            <span
                                class="badge badge-square badge-dark"
                                v-else-if="isStart(ContestView.end_time)"
                            >结束于{{ getFormatDate(ContestView.end_time) }}</span>
                            <span
                                class="badge badge-square badge-danger"
                                v-else
                            >进行中, 结束于{{ getFormatDate(ContestView.end_time) }}</span>
                            <span
                                class="tooltiptext"
                                v-if="!isStart(ContestView.start_time)"
                            >{{ getFormatDate(ContestView.start_time, 0) }}</span>
                            <span
                                class="tooltiptext"
                                v-else
                            >{{ getFormatDate(ContestView.end_time, 0) }}</span>
                        </span>&nbsp;
                        <span class="badge badge-square badge-warning">
                            <i class="fas fa-clock"></i>
                            {{ getDeltaDate(ContestView.start_time, ContestView.end_time) }}
                        </span>
                        <div class="divider"></div>
                        <div class="content line-numbers" v-html="ContestView.description"></div>
                    </div>
                </div>
                <div class="card" v-if="isStart(ContestView.start_time)">
                    <div class="card-body">
                        <h3>题目列表</h3>
                    </div>
                    <table class="table">
                        <thead>
                            <tr>
                                <th class="problem-status" v-if="$store.state.loginUser.uid !== -1"></th>
                                <th>标题</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(p, i) in ContestView.problems" v-bind:key="i">
                                <td v-if="$store.state.loginUser.uid !== -1">
                                    <router-link
                                        class="status-result"
                                        v-if="p.result.res != 0"
                                        :style="`color:${results[p.result.res].color};`"
                                        :to="{ name: 'SubmissionShow', params: { id: p.result.sid } }"
                                    >
                                        <i
                                            :class="`fas fa-${results[p.result.res].icon} resultIcon`"
                                        ></i>
                                    </router-link>
                                </td>
                                <td>
                                    <router-link
                                        :to="{ name: 'ProblemShow', params: { id: p.id }, query: { contest: ContestView.id } }"
                                    >#{{ problemId[i] }}. {{ p.title }}</router-link>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="col-md-4 col-sm-12">
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
                        <router-link
                            :to="{ name: 'ContestRank', params: { id: ContestView.id } }"
                        >排名</router-link>
                    </li>
                    <li v-if="($store.state.loginUser.privilege & 4096) > 0">
                        <router-link
                            :to="{ name: 'ContestEdit', params: { id: ContestView.id } }"
                        >编辑比赛</router-link>
                    </li>
                    <li v-if="($store.state.loginUser.privilege & 4096) > 0">
                        <a @click="deleteContest()" href="javascript:;">删除比赛</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<style scoped>
.problem-status,
.problem-id {
    width: 6.25%;
}
</style>

<script>
import Swal from 'sweetalert2'
import showdown from 'showdown'
import showdownKatex from 'showdown-katex'
import Prism from 'prismjs'
import 'prismjs/components/prism-python.js'
import '../../statics/line-number.js'
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
            contestTypes: ["ACM", "OI", "自由训练"],
            problemId: "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            ContestView: {
                id: this.$route.params.id,
                title: '',
                start_time: '',
                end_time: '',
                tp: 0,
                problems: [],
                privilege: 0,
            },
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
        _t.$store.commit('changeTitle', '加载中')
        _t.$axios.get(`${_t.$store.state.backendURL}/api/contest/${_t.$route.params.id}/`).then((res) => {
            _t.ContestView = res.data.data
            _t.ContestView.description = converter.makeHtml(_t.ContestView.description)
            _t.$store.commit('changeTitle', `比赛 #${_t.$route.params.id} ${_t.ContestView.title}`)
            setTimeout(() => { Prism.highlightAll() }, 100)
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
            Toast.fire(
                t,
                m,
                'error'
            )
        },
        getFormatDate(e, k = 1) {
            return k ? this.$moment(e).fromNow() : this.$moment(e).format("YYYY-MM-DD HH:mm:ss")
        },
        getDeltaDate(s, e) {
            let dux = this.$moment.duration(this.$moment(e).diff(this.$moment(s)))
            let res = ""
            if (dux.get('years'))
                res += `${dux.get('years')}年`
            if (dux.get('months'))
                res += `${dux.get('months')}月`
            if (dux.get('days'))
                res += `${dux.get('days')}天`
            if (dux.get('hours'))
                res += `${dux.get('hours')}小时`
            if (dux.get('minutes'))
                res += `${dux.get('minutes')}分`
            if (dux.get('seconds'))
                res += `${dux.get('seconds')}秒`
            if (res == "")
                res = "0秒"
            return res
        },
        isStart(e) {
            if (this.$moment(e).diff(this.$moment()) <= 0)
                return true
            else
                return false
        },
        deleteContest() {
            let _t = this
            Swal.fire({
                title: '真的要删除这场比赛吗?',
                text: "连提交记录会被一起删除，不可恢复！",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#db2828',
                confirmButtonText: '给老子删了!',
                cancelButtonColor: '#eee',
                cancelButtonText: '不敢!'
            }).then((result) => {
                if (result.value) {
                    _t.$axios.get(`${_t.$store.state.backendURL}/api/contest/${_t.$route.params.id}/delete/`).then((res) => {
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
                                    name: "ContestSet"
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
    }
}
</script>
