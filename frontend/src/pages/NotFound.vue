<template>
    <div class="card">
        <div class="card-body text-center">
            <span class="errorText">
                <span>4</span>
                <i class="far fa-compass errorIcon"></i>
                <span>4</span>
            </span>
            <span class="errorSubText">浏览器放弃了思考</span>
            <div class="row">
                <div class="col-md-3 col-sm-12 col-12"></div>
                <div class="col-md-3 col-sm-6 col-6">
                    <a
                        href="javascript:;"
                        class="btn btn-outline-light btn-block"
                        @click="back()"
                    >返回</a>
                </div>
                <div class="col-md-3 col-sm-6 col-6">
                    <a href="javascript:;" class="btn btn-primary btn-block" @click="goHome()">主页</a>
                </div>
                <div class="col-md-3 col-sm-12 col-12"></div>
            </div>
        </div>
    </div>
</template>

<style scoped>
@keyframes error404animation {
    0% {
        transform: rotate(0deg);
    }
    20% {
        transform: rotate(-60deg);
    }
    40% {
        transform: rotate(-10deg);
    }
    60% {
        transform: rotate(50deg);
    }
    80% {
        transform: rotate(-20deg);
    }
    to {
        transform: rotate(0deg);
    }
}
.errorText {
    color: #2185d0;
    font-size: 160px;
    font-weight: 300;
    display: block;
    line-height: 1.1rem;
}
.errorIcon {
    color: #47af50;
    animation: error404animation 3s ease 0s infinite alternate;
}
.errorSubText {
    color: #d1d3d5;
    font-size: 30px;
    letter-spacing: 12px;
}
</style>

<script>
export default {
    mounted() {
        this.$store.commit('changeTitle', '404 Not Found')
    },
    methods: {
        goHome() {
            this.$router.push('/')
        },
        back() {
            this.$router.back(-1)
        }
    }
}
</script>