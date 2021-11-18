<template>
    <div>
        <div class="row">
            <div class="col-md-8 col-sm-12">
                <template v-if="isLoadingDiscussList">
                    <div class="card">
                        <div class="card-body">
                            <div class="d-flex justify-content-center">
                                <div class="spinner-grow text-primary" role="status">
                                    <span class="sr-only">Loading...</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
                <template v-else-if="DiscussList.length === 0">
                    <div class="card">
                        <div class="card-body">
                            <div class="text-center">
                                <h1>
                                    <i class="fas fa-exclamation-circle"></i>
                                </h1>Nothing found here
                            </div>
                        </div>
                    </div>
                    <br />
                </template>
                <template v-for="(d, i) in DiscussList" v-bind:key="i">
                    <div class="card">
                        <div class="card-body">
                            <h4>
                                <router-link
                                    :to="{ name: 'DiscussShow', params: { id: d.id } }"
                                >{{ d.title }}</router-link>
                            </h4>
                            <div class="card-description">
                                <template v-if="d.toplevel > 1">
                                    <span
                                        class="badge badge-pill badge-square badge-danger vtooltip"
                                        style="margin-right: 3px"
                                    >
                                        置顶
                                        <span class="tooltiptext">置顶等级:{{ d.toplevel }}</span>
                                    </span>
                                </template>
                                <span
                                    class="badge badge-square badge-primary section-bdg"
                                    @click="getDiscuss(1, getSectionById(d.section).id)"
                                >{{ getSectionById(d.section).title }}</span>
                                {{ d.author }} @
                                <span
                                    class="vtooltip"
                                >
                                    {{ getFormatDate(d.date) }}
                                    <span
                                        class="tooltiptext"
                                    >{{ getFormatDate(d.date, 0) }}</span>
                                </span>
                            </div>
                        </div>
                    </div>
                </template>
                <ul class="pagination">
                    <li class="page-item">
                        <a class="page-link" @click="getDiscuss(1, section)" href="javascript:;">
                            <i class="fas fa-chevron-left"></i>
                        </a>
                    </li>
                    <li class="page-item" v-if="currentPage > 1">
                        <a
                            class="page-link"
                            @click="getDiscuss(currentPage - 1, section)"
                            href="javascript:;"
                        >{{ currentPage - 1 }}</a>
                    </li>
                    <li class="page-item active">
                        <a class="page-link">{{ currentPage }}</a>
                    </li>
                    <li class="page-item" v-if="currentPage < totalPage">
                        <a
                            class="page-link"
                            @click="getDiscuss(currentPage + 1, section)"
                            href="javascript:;"
                        >{{ currentPage + 1 }}</a>
                    </li>
                    <li class="page-item">
                        <a
                            class="page-link"
                            @click="getDiscuss(totalPage, section)"
                            href="javascript:;"
                        >
                            <i class="fas fa-chevron-right"></i>
                        </a>
                    </li>
                </ul>
            </div>
            <div class="col-md-4 col-sm-12">
                <div class="card">
                    <div class="card-body">
                        <h4>版块</h4>
                        <div class="divider"></div>
                        <div
                            class="spinner-grow text-primary"
                            role="status"
                            v-if="SectionList.length <= 0"
                        >
                            <span class="sr-only">Loading...</span>
                        </div>
                        <template v-for="(s,i) in SectionList" v-bind:key="i">
                            <button
                                type="button"
                                class="btn btn-primary section-button"
                                @click="getDiscuss(1, s.id)"
                            >{{ s.title }}</button>
                        </template>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h4>新建帖子</h4>
                        <div class="divider"></div>
                        <template v-if="section == 'all' || $store.state.loginUser.uid === -1">
                            要新建一个帖子，请
                            <template v-if="$store.state.loginUser.uid !== -1">先选择一个板块</template>
                            <template v-else>
                                先
                                <a
                                    href="javascript:;"
                                    data-toggle="modal"
                                    data-target="#loginModal"
                                >登录</a>
                            </template>
                        </template>
                        <template v-else>
                            <router-link
                                :to="{ name: 'DiscussNew', query: { section: section } }"
                                class="btn btn-primary"
                            >新建帖子</router-link>
                        </template>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.section-bdg {
    cursor: pointer;
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
            isLoadingDiscussList: true,
            DiscussList: [],
            section: 'all',
            currentPage: 1,
            totalPage: 1,
            SectionList: [],
            PostEditor: '',
        }
    },
    mounted() {
        const _t = this
        _t.$store.commit('changeTitle', '讨论')
        if (_t.$route.query.page)
            _t.currentPage = _t.$route.query.page
        if (_t.$route.query.section)
            _t.section = _t.$route.query.section
        _t.getDiscuss(_t.currentPage, _t.section)
        _t.$axios.get(`${_t.$store.state.backendURL}/api/discuss/sections/`).then((res) => {
            _t.SectionList = res.data.data
        })
    },
    methods: {
        getDiscuss(page, section) {
            let _t = this
            _t.isLoadingDiscussList = true
            _t.section = section
            _t.$router.replace(`?page=${page}&section=${section}`)
            _t.$axios.get(`${_t.$store.state.backendURL}/api/discuss/list/?page=${page}&section=${section}`).then((res) => {
                _t.isLoadingDiscussList = false
                _t.DiscussList = res.data.data
                _t.totalPage = res.data.totalPage
                _t.currentPage = res.data.currentPage
                _t.$store.commit('changeTitle', `讨论 - ${_t.getSectionById(section).title}`)
            }).catch((error) => {
                Toast.fire(
                    'Oops',
                    error.message,
                    'error',
                )
                _t.section = "all"
            })
        },
        getSectionById(e) {
            if (e == 'all')
                return {
                    id: "全局板块",
                    title: "全局板块"
                }
            if (e > 1000)
                return {
                    id: 'P' + (e - 1000),
                    title: 'P' + (e - 1000)
                }
            if (typeof e == 'string' && e.search(/^P(\d+)$/) != -1)
                return {
                    id: e,
                    title: e
                }
            for (let i in this.SectionList) {
                if (this.SectionList[i].id == e)
                    return this.SectionList[i]
            }
            return {
                id: "undefined",
                title: "undefined"
            }
        },
        getFormatDate(e, k = 1) {
            return k ? this.$moment(e).fromNow() : this.$moment(e).format("YYYY-MM-DD HH:mm:ss")
        }
    }
}
</script>
