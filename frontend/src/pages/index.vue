<template>
    <div>
        <div class="row">
            <div class="col-md-8 col-sm-12">
                <h3 class="field-title">公告</h3>
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>标题</th>
                            <th>发布时间</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(a, i) in AnnoucementsList" v-bind:key="i">
                            <td>{{ a.id }}</td>
                            <td>
                                <router-link
                                    :to="{ name: 'NewsPage', params: { id: a.id } }"
                                >{{ a.title }}</router-link>
                            </td>
                            <td>{{ a.pub_date }}</td>
                        </tr>
                    </tbody>
                </table>
                <br />
                <h3 class="field-title">近期比赛</h3>
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>比赛标题</th>
                            <th>起止时间</th>
                        </tr>
                    </thead>
                </table>
                <br />
            </div>
            <div class="col-md-4 col-sm-12">
                <h3 class="field-title">最近更新</h3>
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>题目标题</th>
                        </tr>
                    </thead>
                </table>
                <br />
                <h3 class="field-title">排行榜</h3>
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>UID</th>
                        </tr>
                    </thead>
                </table>
                <br />
            </div>
        </div>
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
            AnnoucementsList: []
        }
    },
    mounted() {
        const _t = this
        _t.$store.commit('changeTitle', '首页')
        axios.get(`${_t.$store.state.backendURL}/api/announcements/list`).then((res) => {
            _t.AnnoucementsList = res.data.data
        }).catch((error) => {
            Toast.fire(
                'Oops',
                error.message,
                'error',
            )
        })
    }
}
</script>
