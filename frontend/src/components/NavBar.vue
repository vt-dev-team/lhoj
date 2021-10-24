<script setup>
import LoginForm from "./users/login.vue"
</script>
<template>
    <div class="background-banner">
        <div class="filter"></div>
        <nav class="navbar fixed-top navbar-expand-lg navbar-transparent navbar-dark mb-4" id="nav">
            <div class="container">
                <router-link
                    class="navbar-brand d-flex align-items-center"
                    :to="{ name: 'HomePage' }"
                >
                    <img src="../assets/logo.svg" alt="Example Navbar 1" class="mr-2" height="30" />
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
                    <ul class="navbar-nav ml-auto">
                        <li class="nav-item">
                            <router-link class="nav-link" :to="{ name: 'HomePage' }">首页</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" :to="{ name: 'ProblemSet' }">题库</router-link>
                        </li>
                        <li class="nav-item">
                            <a
                                class="nav-link"
                                href="javascript:;"
                                data-toggle="modal"
                                data-target="#loginModal"
                            >登录</a>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" :to="{ name: 'ProblemSet' }">注册</router-link>
                        </li>
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
    min-height: 200px;
    background-image: url(../statics/lazykit/img/purple.jpg);
    background-position: center center;
    background-size: cover;
    position: relative;
    width: 100%;
}
.navbar {
    padding: 8px 16px;
    transition: all 0.3s;
}
.mn-nav {
    box-shadow: 0 0 6px rgba(0, 0, 0, 0.2);
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
</script>
