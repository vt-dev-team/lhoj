<template>
    <div>
        <div class="row">
            <div class="col-md-8 col-sm-12">
                <div v-html="AnnouncementView.content"></div>
            </div>
            <div class="col-md-4 col-sm-12">
                <div class="card">
                    <div class="card-body">
                        <table class="table">
                            <tr>
                                <th>发布者</th>
                                <td>{{ AnnouncementView.author }}</td>
                            </tr>
                            <tr>
                                <th>发布时间</th>
                                <td>{{ AnnouncementView.pub_date }}</td>
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
import showdown from 'showdown'
import showdownKatex from 'showdown-katex'
import Prism from 'prismjs'
import 'prismjs/components/prism-python.js'
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
            AnnouncementView: {
                id: 0,
                title: "加载中",
                content: "加载中",
                author: "加载中",
                pub_date: "加载中"
            }
        }
    },
    mounted() {
        const _t = this
        _t.$store.commit('changeTitle', '加载中')
        _t.$axios.get(`${_t.$store.state.backendURL}/api/main/announcements/${_t.$route.params.id}/`).then((res) => {
            _t.AnnouncementView = res.data
            _t.AnnouncementView.content = converter.makeHtml(_t.AnnouncementView.content)
            _t.$store.commit('changeTitle', _t.AnnouncementView.title)
            setTimeout(() => { Prism.highlightAll() }, 100)
        }).catch((error) => {
            Toast.fire(
                'Oops',
                error.message,
                'error',
            )
            _t.AnnouncementView = {
                id: 0,
                title: "加载失败",
                content: `<h3>在请求后端时遇到错误</h3><p>${error.message}</p>`,
                author: "加载失败",
                pub_date: "加载失败"
            }
            _t.$store.commit('changeTitle', _t.AnnouncementView.title)
        })
    }
}
</script>
