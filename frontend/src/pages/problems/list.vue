<template>
    <div>
        <h2 class="page-header">题库</h2>
        <table class="table table-hover">
            <thead>
                <tr>
                    <th>#</th>
                    <th>标题</th>
                    <th>标签</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(p, i) in ProblemList" v-bind:key="i">
                    <td>{{ p.id }}</td>
                    <td>
                        <router-link
                            :to="{ name: 'ProblemShow', params: { id: p.id } }"
                        >{{ p.title }}</router-link>
                    </td>
                    <td>{{ p.tags }}</td>
                </tr>
            </tbody>
        </table>
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
</template>
<script>
import axios from 'axios'
import Swal from 'sweetalert2'
const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000
})
window.Swal = Swal
export default {
    data() {
        return {
            ProblemList: [],
            currentPage: 1,
            totalPage: 1,
        }
    },
    mounted() {
        const _t = this
        _t.$store.commit('changeTitle', '题库')
        if (_t.$route.query.page)
            _t.currentPage = _t.$route.query.page
        _t.getProblem(_t.currentPage)
    },
    methods: {
        getProblem(page) {
            let _t = this
            axios.get(`${_t.$store.state.backendURL}/problem/list/?page=${page}`).then((res) => {
                _t.ProblemList = res.data.data
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
