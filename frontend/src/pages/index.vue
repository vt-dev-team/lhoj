<template>
    <div>
        <div class="row">
            <div class="col-md-8 col-sm-12">
                <div class="card">
                    <div class="card-body">
                        <h3 class="field-title">公告</h3>
                        <div class="d-flex justify-content-center" v-if="isLoadAnnoucement">
                            <div class="spinner-grow text-primary" role="status">
                                <span class="sr-only">Loading...</span>
                            </div>
                        </div>
                        <template v-else>
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>标题</th>
                                        <th>发布时间</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(a, i) in AnnoucementsList" v-bind:key="i">
                                        <td>
                                            <router-link
                                                :to="{ name: 'NewsPage', params: { id: a.id } }"
                                            >{{ a.title }}</router-link>
                                        </td>
                                        <td>{{ getFormatDate(a.pub_date, 0) }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </template>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h3 class="field-title">近期比赛</h3>
                        <div class="d-flex justify-content-center" v-if="isLoadContests">
                            <div class="spinner-grow text-primary" role="status">
                                <span class="sr-only">Loading...</span>
                            </div>
                        </div>
                        <template v-else>
                            <div class="row">
                                <div
                                    class="col-md-6 col-12"
                                    v-for="(c, i) in ContestList"
                                    v-bind:key="i"
                                >
                                    <div class="card">
                                        <div class="card-body">
                                            <h5>
                                                <router-link
                                                    :to="{ name: 'ContestShow', params: { id: c.id } }"
                                                >{{ c.title }}</router-link>
                                            </h5>
                                            <span
                                                class="badge badge-square badge-primary badge-pill"
                                            >{{ contestTypes[c.tp] }}</span>&nbsp;
                                            <span class="vtooltip">
                                                <span
                                                    class="badge badge-square badge-info"
                                                    v-if="!isStart(c.start_time)"
                                                >开始于{{ getFormatDate(c.start_time) }}</span>
                                                <span
                                                    class="badge badge-square badge-dark bg-grey"
                                                    v-else-if="isStart(c.end_time)"
                                                >结束于{{ getFormatDate(c.end_time) }}</span>
                                                <span
                                                    class="badge badge-square badge-danger"
                                                    v-else
                                                >进行中, 结束于{{ getFormatDate(c.end_time) }}</span>
                                                <span
                                                    class="tooltiptext"
                                                    v-if="!isStart(c.start_time)"
                                                >{{ getFormatDate(c.start_time, 0) }}</span>
                                                <span
                                                    class="tooltiptext"
                                                    v-else
                                                >{{ getFormatDate(c.end_time, 0) }}</span>
                                            </span>&nbsp;
                                            <span class="badge badge-square badge-warning">
                                                <i class="fas fa-clock"></i>
                                                {{ getDeltaDate(c.start_time, c.end_time) }}
                                            </span>
                                        </div>
                                        <div class="progress card-progress">
                                            <div
                                                class="progress-bar"
                                                :class="{ 'bg-grey': isStart(c.end_time) }"
                                                role="progressbar"
                                                :style="`width: ${calcWidth(c.start_time, c.end_time)}%;`"
                                                aria-valuenow="25"
                                                aria-valuemin="0"
                                                aria-valuemax="1000"
                                            ></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>
            </div>
            <div class="col-md-4 col-sm-12">
                <div class="card">
                    <div class="card-body">
                        <h3 class="field-title">最近更新</h3>
                        <div class="d-flex justify-content-center" v-if="isLoadProblems">
                            <div class="spinner-grow text-primary" role="status">
                                <span class="sr-only">Loading...</span>
                            </div>
                        </div>
                        <template v-else>
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>#</th>
                                        <th>题目标题</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(p,i) in LatestProblems" v-bind:key="i">
                                        <td>#{{ p.id }}</td>
                                        <td>
                                            <router-link
                                                :to="{ name: 'ProblemShow', params: { id: p.id } }"
                                            >{{ p.title }}</router-link>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </template>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h3 class="field-title">排行榜(Solve)</h3>
                        <div class="d-flex justify-content-center" v-if="isLoadUserRank">
                            <div class="spinner-grow text-primary" role="status">
                                <span class="sr-only">Loading...</span>
                            </div>
                        </div>
                        <template v-else>
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>#</th>
                                        <th>用户名</th>
                                        <th>解决</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(u,i) in UserRank" v-bind:key="i">
                                        <td>{{ i + 1 }}</td>
                                        <td>
                                            <router-link
                                                :to="{ name: 'UserInfo', params: { id: u.username } }"
                                            >{{ u.username }}</router-link>
                                        </td>
                                        <td>{{ u.solve }}题</td>
                                    </tr>
                                </tbody>
                            </table>
                        </template>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Swal from 'sweetalert2'
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
            isLoadAnnoucement: false,
            AnnoucementsList: [],
            isLoadUserRank: false,
            UserRank: [],
            isLoadProblems: false,
            LatestProblems: [],
            isLoadContests: false,
            ContestList: [],
            contestTypes: ["ACM", "OI", "自由训练"]
        }
    },
    mounted() {
        const _t = this
        _t.$store.commit('changeTitle', '首页')
        _t.isLoadAnnoucement = true
        _t.$axios.get(`${_t.$store.state.backendURL}/api/main/announcements/list`).then((res) => {
            _t.isLoadAnnoucement = false
            _t.AnnoucementsList = res.data.data
        }).catch((error) => {
            Toast.fire(
                'Oops',
                error.message,
                'error',
            )
        })
        _t.isLoadUserRank = true
        _t.$axios.get(`${_t.$store.state.backendURL}/api/user/rank/?size=10`).then((res) => {
            _t.isLoadUserRank = false
            _t.UserRank = res.data.data
        }).catch((error) => {
            Toast.fire(
                'Oops',
                error.message,
                'error',
            )
        })
        _t.isLoadProblems = true
        _t.$axios.get(`${_t.$store.state.backendURL}/api/problem/latest/`).then((res) => {
            _t.isLoadProblems = false
            _t.LatestProblems = res.data.data
        }).catch((error) => {
            Toast.fire(
                'Oops',
                error.message,
                'error',
            )
        })
        _t.isLoadContests = true
        _t.$axios.get(`${_t.$store.state.backendURL}/api/contest/latest/`).then((res) => {
            _t.isLoadContests = false
            _t.ContestList = res.data.data
        }).catch((error) => {
            Toast.fire(
                'Oops',
                error.message,
                'error',
            )
        })
    },
    methods: {

        getFormatDate(e, k = 1) {
            return k ? this.$moment(e).fromNow() : this.$moment(e).format("YYYY-MM-DD HH:mm:ss")
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
        calcWidth(e, f) {
            return this.$moment().diff(this.$moment(e)) / this.$moment(f).diff(this.$moment(e)) * 100
        }
    }
}
</script>
