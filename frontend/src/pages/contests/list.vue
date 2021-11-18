<template>
    <div>
        <div class="row">
            <div class="col-md-9 col-sm-12">
                <div class="card" v-if="isLoading">
                    <div class="card-body">
                        <div class="d-flex justify-content-center">
                            <div class="spinner-grow text-primary" role="status">
                                <span class="sr-only">Loading...</span>
                            </div>
                        </div>
                    </div>
                </div>
                <template v-for="(c,i) in ContestList" v-bind:key="i">
                    <div class="card">
                        <div class="card-body">
                            <h4>
                                <router-link
                                    :to="{ name: 'ContestShow', params: { id: c.id } }"
                                >{{ c.title }}</router-link>
                            </h4>
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
                </template>
                <ul class="pagination">
                    <li class="page-item">
                        <a class="page-link" @click="getContest(1)" href="javascript:;">
                            <i class="fas fa-chevron-left"></i>
                        </a>
                    </li>
                    <li class="page-item" v-if="currentPage > 1">
                        <a
                            class="page-link"
                            @click="getContest(currentPage - 1)"
                            href="javascript:;"
                        >{{ currentPage - 1 }}</a>
                    </li>
                    <li class="page-item active">
                        <a class="page-link">{{ currentPage }}</a>
                    </li>
                    <li class="page-item" v-if="currentPage < totalPage">
                        <a
                            class="page-link"
                            @click="getContest(currentPage + 1)"
                            href="javascript:;"
                        >{{ currentPage + 1 }}</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" @click="getContest(totalPage)" href="javascript:;">
                            <i class="fas fa-chevron-right"></i>
                        </a>
                    </li>
                </ul>
            </div>
            <div class="col-md-3 col-sm-12">
                <div class="card">
                    <div class="card-body">
                        <h4>当前时间</h4>
                        {{ nowTime }}
                    </div>
                </div>
                <div class="card" v-if="($store.state.loginUser.privilege & 512) > 0">
                    <div class="card-body">
                        <h4>管理比赛</h4>
                        <router-link :to="{ name: 'ContestNew' }" class="btn btn-icon btn-primary">
                            <span class="btn-inner--icon">
                                <i class="fas fa-plus"></i>
                            </span>
                            <span class="btn-inner--text">新建比赛</span>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<style scoped>
.Contest-status,
.Contest-id {
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
            ContestList: [],
            currentPage: 1,
            totalPage: 1,
            nowTime: this.$moment().format("YYYY-MM-DD HH:mm:ss"),
            nowTimeSetter: '',
            contestTypes: ["ACM", "OI", "自由训练"]
        }
    },
    mounted() {
        const _t = this
        _t.nowTimeSetter = setInterval(() => { _t.getNowTime() }, 1000)
        _t.$store.commit('changeTitle', '比赛')
        if (_t.$route.query.search)
            _t.searchContent = _t.$route.query.search
        if (_t.$route.query.page)
            _t.currentPage = _t.$route.query.page
        _t.getContest(_t.currentPage)
    },
    beforeUnmount() {
        clearInterval(this.nowTimeSetter)
    },
    methods: {
        getNowTime() {
            this.nowTime = this.$moment().format("YYYY-MM-DD HH:mm:ss")
        },
        getContest(page) {
            let _t = this
            _t.isLoading = true
            let fixurl = `?page=${page}`
            _t.$router.replace(fixurl)
            _t.$axios.get(`${_t.$store.state.backendURL}/api/contest/list/${fixurl}`).then((res) => {
                _t.isLoading = false
                _t.ContestList = res.data.data
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
