<template>
    <div>
        <ul class="nav nav-tabs">
            <li class="nav-item">
                <a class="nav-link active" data-toggle="tab" href="#solve">Solve</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" data-toggle="tab" href="#rating">Rating</a>
            </li>
        </ul>
        <div
            id="myTabContent2"
            class="tab-content"
            style="background-color: #fff; z-index: 3; padding-top: 20px; border-top: 1px solid #c1c3c5"
        >
            <div class="tab-pane fade active show" id="solve">
                <div class="card" v-if="isSolveLoading">
                    <div class="card-body">
                        <div class="d-flex justify-content-center">
                            <div class="spinner-grow text-primary" role="status">
                                <span class="sr-only">Loading...</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div
                        class="col-md-4 col-sm-6 col-12"
                        v-for="(u,i) in UserListSolve"
                        v-bind:key="i"
                    >
                        <div class="card card-rank">
                            <div class="card-body">
                                <h3>
                                    <router-link
                                        :to="{ name: 'UserInfo', params: { id: u.username } }"
                                    >{{ u.username }}</router-link>
                                </h3>
                                <span class="badge badge-square badge-primary">Solve: {{ u.solve }}</span>&nbsp;
                                <span
                                    class="badge badge-square badge-warning"
                                >Rating: {{ u.rating }}</span>
                            </div>
                            <span class="rank">#{{ u.rank }}</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="tab-pane fade" id="rating">
                <div class="card" v-if="isRatingLoading">
                    <div class="card-body">
                        <div class="d-flex justify-content-center">
                            <div class="spinner-grow text-primary" role="status">
                                <span class="sr-only">Loading...</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div
                        class="col-md-4 col-sm-6 col-12"
                        v-for="(u,i) in UserListRating"
                        v-bind:key="i"
                    >
                        <div class="card card-rank">
                            <div class="card-body">
                                <h3>
                                    <router-link
                                        :to="{ name: 'UserInfo', params: { id: u.username } }"
                                    >{{ u.username }}</router-link>
                                </h3>
                                <span class="badge badge-square badge-primary">Solve: {{ u.solve }}</span>&nbsp;
                                <span
                                    class="badge badge-square badge-warning"
                                >Rating: {{ u.rating }}</span>
                            </div>
                            <span class="rank">#{{ u.rank }}</span>
                        </div>
                    </div>
                </div>
            </div>
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
                    <a class="page-link" @click="getProblem(totalPage)" href="javascript:;">
                        <i class="fas fa-chevron-right"></i>
                    </a>
                </li>
            </ul>
        </div>
    </div>
</template>

<style>
.rank {
    font-size: 60px;
    color: #d1d3d5;
    font-weight: 300;
    bottom: 0;
    right: 10px;
    position: absolute;
}
.card-rank {
    margin-bottom: 20px;
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
            isRatingLoading: true,
            isSolveLoading: true,
            UserListSolve: [],
            UserListRating: [],
            currentPage: 1,
            totalPage: 1,
        }
    },
    mounted() {
        const _t = this
        _t.$store.commit('changeTitle', '排名')
        if (_t.$route.query.page)
            _t.currentPage = _t.$route.query.page
        _t.getUsers(_t.currentPage)
    },
    methods: {
        getUsers(page) {
            let _t = this
            _t.$router.replace(`?page=${page}`)
            _t.isSolveLoading = true
            _t.isRatingLoading = true
            _t.$axios.get(`${_t.$store.state.backendURL}/api/user/rank/`).then((res) => {
                _t.isSolveLoading = false
                _t.UserListSolve = res.data.data
            }).catch((error) => {
                Toast.fire(
                    'Oops',
                    error.message,
                    'error',
                )
            })
            _t.$axios.get(`${_t.$store.state.backendURL}/api/user/rank/?xz=rating`).then((res) => {
                _t.isRatingLoading = false
                _t.UserListRating = res.data.data
                _t.totalPage = res.data.totalPage
                _t.currentPage = res.data.currentPage
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
