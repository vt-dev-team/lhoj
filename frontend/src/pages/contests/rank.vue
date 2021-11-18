<template>
    <div>
        <div class="row">
            <div class="col-md-8 col-sm-12">
                <div class="card">
                    <div class="card-body">
                        <h3>{{ ContestView.title }} 榜单</h3>
                    </div>
                    <div style="width: 100%; overflow-y: auto">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th class="contest-rank">#</th>
                                    <th>用户名</th>
                                    <th v-if="ContestView.tp == 1">得分</th>
                                    <th v-else>解决</th>
                                    <th
                                        v-for="(p,i) in ContestView.problems"
                                        v-bind:key="i"
                                    >#{{ problemId[i] }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(p, i) in RankList" v-bind:key="i">
                                    <td>{{ p.rank }}</td>
                                    <td>
                                        <router-link
                                            :to="{ name: 'UserInfo', params: { id: p.user_id } }"
                                        >{{ p.user_id }}</router-link>
                                    </td>
                                    <td v-if="ContestView.tp == 1">{{ p.score }}</td>
                                    <td v-else>{{ p.solved }}</td>
                                    <template v-if="ContestView.tp == 1">
                                        <td v-for="(c, i) in p.problems" v-bind:key="i">
                                            <span class="vtooltip" v-if="c.submission_id > 0">
                                                <router-link
                                                    :to="{ name: 'SubmissionShow', params: { id: c.submission_id } }"
                                                    :class="'score_' + Math.floor(c.score / 10)"
                                                >{{ c.score }}</router-link>
                                                <span class="tooltiptext">{{ getTime(c.time) }}</span>
                                            </span>
                                            <span style="color:#c1c3c5" v-else>-</span>
                                        </td>
                                    </template>
                                    <template v-else>
                                        <td v-for="(c, i) in p.problems" v-bind:key="i">
                                            <span class="vtooltip" v-if="c.submission_id > 0">
                                                <router-link
                                                    :to="{ name: 'SubmissionShow', params: { id: c.submission_id } }"
                                                    :class="[c.result == 3 ? 'score_10' : 'score_0']"
                                                >
                                                    <i
                                                        class="fas"
                                                        :class="[c.result == 3 ? 'fa-check' : 'fa-times']"
                                                    ></i>
                                                </router-link>
                                                <span class="tooltiptext">{{ getTime(c.time) }}</span>
                                            </span>
                                            <span style="color:#c1c3c5" v-else>-</span>
                                        </td>
                                    </template>
                                </tr>
                            </tbody>
                        </table>
                    </div>
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
                </ul>
            </div>
        </div>
    </div>
</template>

<style scoped>
.contest-rank,
.problem-id {
    width: 6.25%;
}
th {
    text-align: inherit;
    vertical-align: inherit;
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
            RankList: [],
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
            { id: '10', color: 'grey', val: 'System Error', icon: 'cog' }]
        }
    },
    mounted() {
        const _t = this
        _t.$store.commit('changeTitle', '加载中')
        _t.$axios.get(`${_t.$store.state.backendURL}/api/contest/${_t.$route.params.id}/rank/`).then((res) => {
            _t.ContestView = res.data.contest
            _t.ContestView.problems = _t.ContestView.problems.split(",")
            _t.RankList = res.data.data
            _t.$store.commit('changeTitle', `排名 #${_t.$route.params.id} ${_t.ContestView.title}`)
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
        getTime(e) {
            return this.$moment(e).format("YYYY-MM-DD HH:mm:ss")
        },
        getFormatDate(e) {
            return this.$moment(e).fromNow()
        },
        getDeltaDate(s, e) {
            let du = this.$moment.duration(this.$moment(e).diff(this.$moment(s)))
            let res = ""
            if (du.get('years'))
                res += `${du.get('years')}年`
            if (du.get('months'))
                res += `${du.get('months')}月`
            if (du.get('days'))
                res += `${du.get('days')}天`
            if (du.get('hours'))
                res += `${du.get('hours')}小时`
            if (du.get('minutes'))
                res += `${du.get('minutes')}分`
            if (du.get('seconds'))
                res += `${du.get('seconds')}秒`
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
    }
}
</script>
