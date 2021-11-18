<template>
    <div class="row">
        <div class="col-md-9 col-sm-12 order-md-1 order-2">
            <div class="card">
                <div class="card-body">
                    <form @submit="modifyInfo">
                        <div class="form-group">
                            <label for="username">用户名</label>
                            {{ UserView.username }}
                        </div>
                        <div class="form-group">
                            <label for="email">邮箱</label>
                            <div class="input-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text" id="basic-addon4">
                                        <i class="fas fa-envelope"></i>
                                    </span>
                                </div>
                                <input
                                    type="email"
                                    class="form-control"
                                    placeholder="邮箱"
                                    aria-label="邮箱"
                                    v-model="UserView.email"
                                    aria-describedby="basic-addon4"
                                />
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="motto">个性签名</label>
                            <textarea class="form-control" v-model="UserView.motto"></textarea>
                        </div>
                        <template v-if="($store.state.loginUser.privilege & 16384) > 0">
                            <div class="form-group">
                                <label for="motto">权限设置</label>
                            </div>
                            <div class="row">
                                <div
                                    class="col-3 text-center"
                                    v-for="(p, i) in privilegeList"
                                    v-bind:key="i"
                                >
                                    <span>{{ p.e }}</span>
                                    <br />
                                    <label class="custom-toggle">
                                        <input type="checkbox" v-model="privilegeHas" :value="p.n" />
                                        <span class="custom-toggle-slider rounded-circle"></span>
                                    </label>
                                    <span class="clearfix"></span>
                                </div>
                            </div>
                        </template>
                        <button
                            class="btn btn-primary"
                            :disabled="isSubmit"
                            v-if="(($store.state.loginUser.privilege & 16384) > 0) || ($store.state.loginUser.uname == UserView.username)"
                        >修改</button>
                    </form>
                </div>
            </div>
        </div>
        <div class="col-md-3 col-sm-12 order-md-2 order-1">
            <template v-if="$store.state.loginUser.uname == $route.params.id">
                <ul class="contest-menu">
                    <li>
                        <router-link :to="{ name: 'UserInfo', params: { id: $route.params.id } }">
                            <i class="far fa-user"></i>个人信息
                        </router-link>
                    </li>
                    <li>
                        <router-link :to="{ name: 'UserModify', params: { id: $route.params.id } }">
                            <i class="fas fa-cog"></i>信息修改
                        </router-link>
                    </li>
                    <li>
                        <router-link :to="{ name: 'UserMessage' }">
                            <i class="far fa-envelope"></i>站内私信
                        </router-link>
                    </li>
                </ul>
            </template>
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
            UserView: {
                id: 0,
                username: "加载中",
                email: "加载中",
                motto: "加载中",
                rating: "加载中",
                privilege: 5,
                reg_time: "加载中",
                posts: 0,
                solved: 0,
            },
            isSubmit: true,
            privilegeList: [
                {
                    "n": 1,
                    "e": "访问主站"
                },
                {
                    "n": 2,
                    "e": "提交题目"
                },
                {
                    "n": 4,
                    "e": "查看题目"
                },
                {
                    "n": 8,
                    "e": "查看他人代码"
                },
                {
                    "n": 16,
                    "e": "参加比赛"
                },
                {
                    "n": 32,
                    "e": "使用博客"
                },
                {
                    "n": 64,
                    "e": "发送私信"
                },
                {
                    "n": 128,
                    "e": "自由发言"
                },
                {
                    "n": 256,
                    "e": "添加题目"
                },
                {
                    "n": 512,
                    "e": "举办比赛"
                },
                {
                    "n": 1024,
                    "e": "获取题目数据"
                },
                {
                    "n": 2048,
                    "e": "编辑题目"
                },
                {
                    "n": 4096,
                    "e": "管理比赛"
                },
                {
                    "n": 8192,
                    "e": "管理发言"
                },
                {
                    "n": 16384,
                    "e": "管理权限"
                },
                {
                    "n": 32768,
                    "e": "操作提交记录"
                },
                {
                    "n": 65536,
                    "e": "下载题目数据"
                }
            ],
            privilegeHas: []
        }
    },
    mounted() {
        let _t = this
        _t.$axios.get(`${_t.$store.state.backendURL}/api/user/${_t.$route.params.id}/`).then((res) => {
            _t.UserView = res.data
            _t.isSubmit = false
            for (let i in _t.privilegeList) {
                if ((_t.privilegeList[i].n & _t.UserView.privilege) > 0)
                    _t.privilegeHas.push(_t.privilegeList[i].n)
            }
            _t.$store.commit('changeTitle', `修改信息 用户${_t.UserView.username}`)
        }).catch((error) => {
            Toast.fire(
                'Oops',
                error.message,
                'error',
            )
        })
    },
    methods: {
        modifyInfo(e) {
            e.preventDefault();
            const _t = this
            if (!(((_t.$store.state.loginUser.privilege & 16384) > 0) || (_t.$store.state.loginUser.uname == _t.UserView.username))) {
                Toast.fire(
                    'Oops',
                    '没有权限',
                    'error',
                )
                return
            }
            _t.UserView.privilege = 0
            for (let i in _t.privilegeHas)
                _t.UserView.privilege |= _t.privilegeHas[i]
            if (_t.UserView.motto.length > 200) {
                _t.showError("Oops", "个性签名太长")
                return
            }
            let param = new URLSearchParams()
            param.append('motto', _t.UserView.motto)
            param.append('email', _t.UserView.email)
            param.append('privilege', _t.UserView.privilege)
            _t.isSubmit = true
            _t.$axios.post(`${_t.$store.state.backendURL}/api/user/${_t.$route.params.id}/modify/`, param).then((res) => {
                _t.isSubmit = false
                if (res.data.code != 0) {
                    Toast.fire(
                        'Oops',
                        res.data.mes,
                        'error',
                    )
                }
                else {
                    _t.$axios.get(`${_t.$store.state.backendURL}/api/user/_login/`).then((res) => {
                        _t.$store.commit('updateUser', res.data.user)
                    })
                    Toast.fire(
                        '成功',
                        "修改成功",
                        'success',
                    )
                }
            })
        }
    }
}
</script>