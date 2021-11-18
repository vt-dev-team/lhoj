<template>
    <div>
        <div class="mb-5">
            <div class="row">
                <div class="col">
                    <input class="form-control" placeholder="题目编号" v-model="searchFilter.problem" />
                </div>
                <div class="col">
                    <input class="form-control" placeholder="用户名" v-model="searchFilter.user_id" />
                </div>
                <div class="col">
                    <select class="form-control" v-model="searchFilter.result">
                        <option value="all">全部结果</option>
                        <option v-for="(r, i) in results" v-bind:key="i" :value="r.id">{{ r.val }}</option>
                    </select>
                </div>
                <div class="col">
                    <button
                        class="btn btn-primary"
                        @click="getSubmission(currentPage)"
                        :disabled="isSubmit"
                    >查询</button>
                </div>
            </div>
        </div>
        <div class="card" v-if="isSubmit">
            <div class="card-body">
                <div class="d-flex justify-content-center">
                    <div class="spinner-grow text-primary" role="status">
                        <span class="sr-only">Loading...</span>
                    </div>
                </div>
            </div>
        </div>
        <table class="table table-hover" v-else>
            <thead>
                <tr>
                    <th>状态</th>
                    <th>分数</th>
                    <th>题目</th>
                    <th>用户</th>
                    <th>用时</th>
                    <th>内存</th>
                    <th>提交时间</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(s, i) in SubmissionList" v-bind:key="i">
                    <td :style="`border-left: 2px solid ${results[s.result].color}`">
                        <router-link
                            class="status-result"
                            :style="`color:${results[s.result].color};`"
                            :to="{ name: 'SubmissionShow', params: { id: s.id } }"
                        >
                            <i :class="`fas fa-${results[s.result].icon} resultIcon`"></i>
                            {{ results[s.result].val }}
                        </router-link>
                    </td>
                    <td>
                        <router-link
                            :class="`score_${Math.floor(s.score / 10)}`"
                            :to="{ name: 'SubmissionShow', params: { id: s.id } }"
                        >{{ s.score }}</router-link>
                    </td>
                    <td>
                        <router-link
                            :to="{ name: 'ProblemShow', params: { id: s.problem } }"
                        >#{{ s.problem }}</router-link>
                    </td>
                    <td>
                        <router-link
                            :to="{ name: 'UserInfo', params: { id: s.user_id } }"
                        >{{ s.user_id }}</router-link>
                    </td>
                    <td>
                        <span>{{ s.time }}ms</span>
                    </td>
                    <td>
                        <span>{{ s.memory }}KB</span>
                    </td>
                    <td>
                        <span class="vtooltip">
                            {{ getFormatDate(s.date) }}
                            <span
                                class="tooltiptext"
                            >{{ getFormatDate(s.date, 0) }}</span>
                        </span>
                    </td>
                </tr>
            </tbody>
        </table>
        <ul class="pagination">
            <li class="page-item">
                <a class="page-link" @click="getSubmission(1)" href="javascript:;">
                    <i class="fas fa-chevron-left"></i>
                </a>
            </li>
            <li class="page-item" v-if="currentPage > 1">
                <a
                    class="page-link"
                    @click="getSubmission(currentPage - 1)"
                    href="javascript:;"
                >{{ currentPage - 1 }}</a>
            </li>
            <li class="page-item active">
                <a class="page-link" href="javascript:;">{{ currentPage }}</a>
            </li>
            <li class="page-item" v-if="currentPage < totalPage">
                <a
                    class="page-link"
                    @click="getSubmission(currentPage + 1)"
                    href="javascript:;"
                >{{ currentPage + 1 }}</a>
            </li>
            <li class="page-item">
                <a class="page-link" @click="getSubmission(totalPage)" href="javascript:;">
                    <i class="fas fa-chevron-right"></i>
                </a>
            </li>
        </ul>
    </div>
</template>
<style>
.status-result {
    text-decoration: none !important;
    border: none !important;
}
.resultIcon {
    margin: 0 0.25rem 0 0 !important;
}
</style>
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
            isSubmit: true,
            SubmissionList: [],
            currentPage: 1,
            totalPage: 1,
            contest: 0,
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
            { id: '11', color: '#ff4f4f', val: 'Unaccepted', icon: 'times' }],
            searchFilter: {
                problem: '',
                user_id: '',
                result: 'all',
            }
        }
    },
    mounted() {
        const _t = this
        if (_t.$route.query.problem)
            _t.searchFilter.problem = _t.$route.query.problem
        if (_t.$route.query.user_id)
            _t.searchFilter.user_id = _t.$route.query.user_id
        if (_t.$route.query.result)
            _t.searchFilter.result = _t.$route.query.result
        else
            _t.searchFilter.result = 'all'
        _t.$store.commit('changeTitle', '评测')
        if (_t.$route.query.page)
            _t.currentPage = _t.$route.query.page
        _t.getSubmission(_t.currentPage)
    },
    methods: {
        getSubmission(page) {
            let _t = this
            _t.contest = Number(_t.$route.query.contest) != NaN ? Number(_t.$route.query.contest) : 0
            let pathfix = `?page=${page}`
            if (_t.contest > 0)
                pathfix += `&contest=${_t.contest}`
            if (_t.searchFilter.problem)
                pathfix += `&problem=${_t.searchFilter.problem}`
            if (_t.searchFilter.user_id)
                pathfix += `&user_id=${_t.searchFilter.user_id}`
            if (_t.searchFilter.result && _t.searchFilter.result != 'all')
                pathfix += `&result=${_t.searchFilter.result}`
            console.log(_t.searchFilter.result)
            _t.$router.replace(pathfix)
            _t.isSubmit = true
            _t.$axios.get(`${_t.$store.state.backendURL}/api/submission/list/${pathfix}`).then((res) => {
                _t.isSubmit = false
                _t.SubmissionList = res.data.data
                _t.totalPage = res.data.totalPage
                _t.currentPage = res.data.currentPage
            }).catch((error) => {
                Toast.fire(
                    'Oops',
                    error.message,
                    'error',
                )
            })
        },
        getFormatDate(e, k = 1) {
            return k ? this.$moment(e).fromNow() : this.$moment(e).format("YYYY-MM-DD HH:mm:ss")
        }
    }
}
</script>
