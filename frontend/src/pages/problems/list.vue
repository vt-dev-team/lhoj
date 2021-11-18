<template>
    <div>
        <div class="row">
            <div class="col-md-9 col-sm-12 order-md-1 order-2">
                <div class="card" v-if="isLoading">
                    <div class="card-body">
                        <div class="d-flex justify-content-center">
                            <div class="spinner-grow text-primary" role="status">
                                <span class="sr-only">Loading...</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card" v-else>
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th v-if="isSelecting" class="problem-select"></th>
                                <th v-if="$store.state.loginUser.uid !== -1" class="problem-status"></th>
                                <th class="problem-id">#</th>
                                <th class="problem-title">标题</th>
                                <th class="problem-tags">标签</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(p, i) in ProblemList" v-bind:key="i">
                                <td v-if="isSelecting">
                                    <input type="checkbox" v-model="selectedProblems" :value="p.id" />
                                </td>
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
                                <td>{{ p.id }}</td>
                                <td>
                                    <router-link
                                        :to="{ name: 'ProblemShow', params: { id: p.id } }"
                                    >{{ p.title }}</router-link>
                                </td>
                                <td>
                                    <span
                                        v-for="(t, i) in p.tags"
                                        v-bind:key="i"
                                        :class="`badge badge-${t.color} problem-tag`"
                                        @click="doSearch(t.label)"
                                    >{{ t.label }}</span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="card-body">
                        <ul class="pagination">
                            <li class="page-item">
                                <a class="page-link" @click="getProblem(1)" href="javascript:;">
                                    <i class="fas fa-chevron-left"></i>
                                </a>
                            </li>
                            <li class="page-item" v-if="currentPage > 1">
                                <a
                                    class="page-link"
                                    @click="getProblem(currentPage - 1)"
                                    href="javascript:;"
                                >{{ currentPage - 1 }}</a>
                            </li>
                            <li class="page-item active">
                                <a class="page-link">{{ currentPage }}</a>
                            </li>
                            <li class="page-item" v-if="currentPage < totalPage">
                                <a
                                    class="page-link"
                                    @click="getProblem(currentPage + 1)"
                                    href="javascript:;"
                                >{{ currentPage + 1 }}</a>
                            </li>
                            <li class="page-item">
                                <a
                                    class="page-link"
                                    @click="getProblem(totalPage)"
                                    href="javascript:;"
                                >
                                    <i class="fas fa-chevron-right"></i>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-md-3 col-sm-12 order-md-2 order-1">
                <div class="card">
                    <div class="card-body">
                        <h4>搜索</h4>
                        <form @submit="doSearchByForm">
                            <div class="form-group">
                                <div class="input-group input-group-alternative mb-4">
                                    <div class="input-group-prepend">
                                        <span class="input-group-text">
                                            <i class="fas fa-search"></i>
                                        </span>
                                    </div>
                                    <input
                                        class="form-control form-control-alternative"
                                        placeholder="Search"
                                        v-model="searchContent"
                                        type="text"
                                    />
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                <div class="card" v-if="($store.state.loginUser.privilege & 256) > 0">
                    <div class="card-body" style="padding-bottom: 0 !important;">
                        <h4>管理题目</h4>
                    </div>
                    <ul class="contest-menu" style="box-shadow: none;">
                        <li>
                            <a @click="isSelecting = !isSelecting" href="javascript:;">
                                <span class="btn-inner--icon">
                                    <i
                                        class="fas"
                                        :class="{ 'fa-th-list': !isSelecting, 'fa-times': isSelecting }"
                                    ></i>
                                </span>
                                <span class="btn-inner--text">
                                    <span v-show="isSelecting">取消</span>多选
                                </span>
                            </a>
                        </li>
                        <li>
                            <router-link :to="{ name: 'ProblemNew' }">
                                <span class="btn-inner--icon">
                                    <i class="fas fa-plus"></i>
                                </span>
                                <span class="btn-inner--text">新建题目</span>
                            </router-link>
                        </li>
                        <li v-show="isSelecting">
                            <a @click="deleteProblems" href="javascript:;">
                                <span class="btn-inner--icon">
                                    <i class="far fa-trash-alt"></i>
                                </span>
                                <span class="btn-inner--text">删除所选</span>
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>
<style>
.problem-select,
.problem-status,
.problem-id {
    width: 6.25%;
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
            isLoading: 1,
            ProblemList: [],
            currentPage: 1,
            totalPage: 1,
            searchContent: '',
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
            { id: '10', color: 'grey', val: 'System Error', icon: 'cog' }],
            isSelecting: false,
            selectedProblems: [],
        }
    },
    mounted() {
        const _t = this
        _t.$store.commit('changeTitle', '题库')
        if (_t.$route.query.search)
            _t.searchContent = _t.$route.query.search
        if (_t.$route.query.page)
            _t.currentPage = _t.$route.query.page
        _t.getProblem(_t.currentPage)
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
        getProblem(page) {
            let _t = this
            _t.isLoading = true
            let fixurl = `?page=${page}`
            if (_t.searchContent)
                fixurl += `&search=${_t.searchContent}`
            _t.$router.replace(fixurl)
            _t.$axios.get(`${_t.$store.state.backendURL}/api/problem/list/${fixurl}`).then((res) => {
                _t.isLoading = false
                _t.ProblemList = res.data.data
                for (let i in _t.ProblemList)
                    _t.ProblemList[i].tags = _t.labelFormat(_t.ProblemList[i].tags.split(","))
                _t.totalPage = res.data.totalPage
                _t.currentPage = res.data.currentPage
            }).catch((error) => {
                _t.isLoading = false
                Toast.fire(
                    'Oops',
                    error.message,
                    'error',
                )
            })
        },
        doSearch(q) {
            this.searchContent = q
            this.getProblem(this.currentPage)
        },
        doSearchByForm(e) {
            e.preventDefault()
            this.getProblem(this.currentPage)
        },
        deleteProblems(e) {
            console.log(this.selectedProblems)
        }
    }
}
</script>
