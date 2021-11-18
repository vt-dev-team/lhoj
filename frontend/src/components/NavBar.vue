<script setup>
import LoginForm from "./users/login.vue"
</script>
<template>
    <div class="background-banner">
        <div></div>
        <nav class="navbar fixed-top navbar-expand-lg navbar-transparent navbar-dark mb-4" id="nav">
            <div class="container">
                <router-link
                    class="navbar-brand d-flex align-items-center logo"
                    :to="{ name: 'HomePage' }"
                >
                    <img src="../assets/logo.svg" alt="LHOJ" class="mr-2" height="30" />
                    LHOJ
                </router-link>
                <button
                    class="navbar-toggler"
                    type="button"
                    data-toggle="collapse"
                    data-target="#navbarNavDropdown-17"
                    aria-controls="navbarNavDropdown-7"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse text-center" id="navbarNavDropdown-17">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <router-link class="nav-link" :to="{ name: 'HomePage' }">首页</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" :to="{ name: 'ProblemSet' }">题库</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" :to="{ name: 'ContestSet' }">比赛</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" :to="{ name: 'SubmissionSet' }">评测</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" :to="{ name: 'UserRank' }">排名</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" :to="{ name: 'DiscussList' }">讨论</router-link>
                        </li>
                    </ul>
                    <ul class="navbar-nav ml-auto">
                        <template v-if="$store.state.loginUser.uid == -1">
                            <li class="nav-item">
                                <a
                                    class="nav-link"
                                    href="javascript:;"
                                    data-toggle="modal"
                                    data-target="#loginModal"
                                >登录</a>
                            </li>
                            <li class="nav-item">
                                <router-link class="nav-link" :to="{ name: 'RegisterPage' }">注册</router-link>
                            </li>
                        </template>
                        <template v-else>
                            <li class="nav-item dropdown">
                                <a
                                    class="nav-link dropdown-toggle"
                                    href="javascript:;"
                                    data-toggle="dropdown"
                                >{{ $store.state.loginUser.uname }}</a>
                                <div class="dropdown-menu">
                                    <router-link
                                        class="dropdown-item"
                                        :to="{ name: 'UserInfo', params: { id: $store.state.loginUser.uname } }"
                                    >个人信息</router-link>
                                    <router-link
                                        class="dropdown-item"
                                        :to="{ name: 'UserModify', params: { id: $store.state.loginUser.uname } }"
                                    >信息修改</router-link>
                                    <router-link
                                        class="dropdown-item"
                                        :to="{ name: 'UserMessage' }"
                                    >私信</router-link>
                                    <a class="dropdown-item" href="javascript:;" @click="logout">登出</a>
                                </div>
                            </li>
                        </template>
                    </ul>
                </div>
            </div>
        </nav>
        <div class="page-pointer">
            <div class="container">
                <h3 class="page-title">{{ $store.state.pageTitle }}</h3>
            </div>
        </div>
        <login-form></login-form>
    </div>
</template>

<style scoped>
.background-banner {
    min-height: 233px;
    background-image: url(../assets/bg6.jpg);
    background-position: center 90%;
    background-size: cover;
    position: relative;
    width: 100%;
}
.navbar {
    padding: 0;
    transition: all 0.3s;
}

.navbar .logo {
    font-family: "Saira";
}
.mn-nav {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}
.page-pointer {
    width: 100%;
    position: absolute;
    bottom: 10px;
}
.page-title {
    color: #fafbfc;
    font-size: 52px;
    font-weight: 300;
    text-shadow: 0px 0px 12px rgba(255, 255, 255, 0.6);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.navbar.bg-light {
    background-color: rgba(255, 255, 255, 0.95) !important;
}
.nav-link {
    position: relative;
    padding: 15px 20px !important;
    transition: border-color 0.3s;
}
.nav-link.active {
    font-weight: bold;
}
.navbar .nav-link:before {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 2px;
    z-index: 30;
    transition: all 0.3s;
}
.navbar:not(.mn-nav) .nav-link.active:before {
    background-color: #fff;
    box-shadow: 0 0 30px #fff, 0 0 30px #fff;
}
.navbar-toggler {
    outline: none;
    padding: 15px 20px !important;
}
.navbar-collapse {
    top: 40px;
    left: auto;
    width: 200px;
    text-align: left !important;
}
.navbar-collapse.show .nav-link:before {
    top: 0;
    right: auto;
    bottom: 0;
    width: 1px;
    height: auto;
}
.navbar-collapse.show .nav-link.active:before {
    background-color: #ed5f82;
    box-shadow: 0 0 30px #ed5f82, 0 0 30px #ed5f82;
}
.mn-nav .nav-link.active:before {
    background-color: #ed5f82;
    box-shadow: 0 0 30px #ed5f82, 0 0 30px #ed5f82;
}
.mn-nav .nav-link:hover:before {
    background-color: #2d8cf0;
    box-shadow: none;
}
</style>

<script>
window.onload = function () {
    let nv = document.getElementById("nav")
    document.body.onscroll = function () {
        if (document.documentElement.scrollTop > 0) {
            nv.classList.remove("navbar-transparent", "navbar-dark")
            nv.classList.add("navbar-light", "bg-light", "mn-nav")
        }
        else {
            nv.classList.add("navbar-transparent", "navbar-dark")
            nv.classList.remove("navbar-light", "bg-light", "mn-nav")
        }
    }
}
export default {
    mounted() {
        let _t = this
        _t.$axios.get(`${_t.$store.state.backendURL}/api/user/_login/`).then((res) => {
            _t.$store.commit('updateUser', res.data.user)
        })
    },
    methods: {
        logout() {
            let _t = this
            _t.$axios.post(`${_t.$store.state.backendURL}/api/user/logout/`).then((res) => {
                _t.$store.commit('updateUser', res.data.user)
            })
        }
    }
}
</script>
