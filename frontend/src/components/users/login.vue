<template>
    <div
        class="modal fade"
        id="loginModal"
        tabindex="-1"
        role="dialog"
        aria-labelledby="loginModalLabel"
        aria-hidden="true"
    >
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header border-bottom-0">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="form-title text-center">
                        <h4>登 录</h4>
                    </div>
                    <div class="d-flex flex-column text-center">
                        <form>
                            <div class="form-group">
                                <input
                                    type="text"
                                    class="form-control"
                                    id="username1"
                                    name="username"
                                    placeholder="用户名"
                                    v-model="uname"
                                />
                            </div>
                            <div class="form-group">
                                <input
                                    type="password"
                                    class="form-control"
                                    id="password1"
                                    name="password"
                                    placeholder="密码"
                                    v-model="pword"
                                />
                            </div>
                            <button
                                type="submit"
                                class="btn btn-info btn-block btn-round"
                                @click="checkLogin"
                            >Login</button>
                        </form>
                    </div>
                </div>
                <div class="modal-footer d-flex justify-content-center">
                    <div class="signup-section">
                        Not a member yet?
                        <a href="#a" class="text-info">Sign Up</a>.
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.form-title {
    margin-top: -10px;
    margin-bottom: 30px;
}
</style>

<script>
export default {
    data() {
        return {
            uname: '',
            pword: ''
        }
    },
    methods: {
        checkLogin(e) {
            let _t = this
            e.preventDefault();
            console.log(_t.uname, _t.pword)
        }
    }
}
</script>