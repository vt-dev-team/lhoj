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
                    <button
                        type="button"
                        id="closeLoginButton"
                        class="close"
                        data-dismiss="modal"
                        aria-label="Close"
                    >
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
                                v-if="!isOping"
                            >登录</button>
                            <button
                                class="btn btn-info btn-block btn-round"
                                type="button"
                                disabled
                                v-else
                            >
                                <span
                                    class="spinner-border spinner-border-sm"
                                    role="status"
                                    aria-hidden="true"
                                ></span>
                                登录中
                            </button>
                        </form>
                    </div>
                </div>
                <div class="modal-footer d-flex justify-content-center">
                    <div class="signup-section">
                        还没有账号?
                        <router-link
                            :to="{ name: 'RegisterPage' }"
                            class="text-info"
                            data-dismiss="modal"
                        >注册</router-link>.
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
import Swal from 'sweetalert2'
const Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 1500,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.addEventListener("mouseenter", Swal.stopTimer);
        toast.addEventListener("mouseleave", Swal.resumeTimer);
    },
})
export default {
    data() {
        return {
            uname: '',
            pword: '',
            isOping: false,
        }
    },
    methods: {
        showError(t, m) {
            let _t = this
            Toast.fire(
                t,
                m,
                'error'
            ).then(() => {
                _t.pword = ""
            })
            _t.isOping = false
        },
        checkLogin(e) {
            let _t = this
            e.preventDefault()
            _t.isOping = true
            if (_t.uname.length > 50) {
                _t.showError("Oops", "用户名太长")
                return
            }
            if (_t.pword.length > 20 || _t.pword.length < 6) {
                _t.showError("Oops", "密码长度不对")
                return
            }
            let param = new URLSearchParams()
            param.append('uname', _t.uname)
            param.append('pword', _t.pword)
            _t.$axios.post(`${_t.$store.state.backendURL}/api/user/login/`, param).then((res) => {
                _t.isOping = false
                if (res.data.code != 0)
                    _t.showError("Oops", res.data.mes)
                else {
                    Toast.fire(
                        "登录成功",
                        res.data.mes,
                        'success'
                    ).then(() => {
                        _t.closeLogin()
                        _t.$store.commit('updateUser', res.data.user)
                    })
                }
            }).catch((error) => {
                Toast.fire(
                    'Oops',
                    error.message,
                    'error',
                )
            })
        },
        closeLogin() {
            //$('#loginModal').modal('hide')
            document.getElementById("closeLoginButton").click()
        }
    }
}
</script>