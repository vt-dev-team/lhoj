<template>
    <div>
        <form @submit="checkReg">
            <div class="form-group">
                <label for="username">用户名</label>
                <div class="input-group">
                    <div class="input-group-prepend">
                        <span class="input-group-text" id="basic-addon1">
                            <i class="fas fa-user"></i>
                        </span>
                    </div>
                    <input
                        type="text"
                        class="form-control"
                        placeholder="用户名(不超过50个字符)"
                        aria-label="用户名"
                        v-model="uname"
                        aria-describedby="basic-addon1"
                    />
                </div>
            </div>
            <div class="form-group">
                <label for="password">密码</label>
                <div class="input-group">
                    <div class="input-group-prepend">
                        <span class="input-group-text" id="basic-addon2">
                            <i class="fas fa-lock"></i>
                        </span>
                    </div>
                    <input
                        type="password"
                        class="form-control"
                        placeholder="密码(6-20位)"
                        aria-label="密码"
                        v-model="pword"
                        aria-describedby="basic-addon2"
                    />
                </div>
            </div>
            <div class="form-group">
                <label for="password2">确认密码</label>
                <div class="input-group">
                    <div class="input-group-prepend">
                        <span class="input-group-text" id="basic-addon3">
                            <i class="fas fa-lock"></i>
                        </span>
                    </div>
                    <input
                        type="password"
                        class="form-control"
                        placeholder="确认密码"
                        aria-label="确认密码"
                        v-model="rptpword"
                        aria-describedby="basic-addon3"
                    />
                </div>
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
                        v-model="email"
                        aria-describedby="basic-addon4"
                    />
                </div>
            </div>
            <div class="form-group">
                <label for="motto">个性签名</label>
                <textarea class="form-control" v-model="motto"></textarea>
            </div>
            <button type="submit" class="btn btn-info" v-if="!isOping">提交</button>
            <button class="btn btn-info" type="button" disabled v-else>
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                提交中
            </button>
        </form>
    </div>
</template>

<script>
import Swal from 'sweetalert2'
export default {
    data() {
        return {
            uname: '',
            pword: '',
            rptpword: '',
            email: '',
            motto: '',
            isOping: false,
        }
    },
    mounted() {
        let _t = this
        _t.$store.commit('changeTitle', '注册')
    },
    methods: {
        showError(t, m) {
            let _t = this
            Swal.fire(
                t,
                m,
                'error'
            ).then(() => {
                _t.pword = ""
                _t.rptpword = ""
            })
            _t.isOping = false
        },
        checkReg(e) {
            let _t = this
            e.preventDefault();
            _t.isOping = true
            if (_t.uname.length > 50) {
                _t.showError("Oops", "用户名太长")
                return
            }
            if (_t.pword.length > 20 || _t.pword.length < 6) {
                _t.showError("Oops", "密码长度不对")
                return
            }
            if (_t.pword != _t.rptpword) {
                _t.showError("Oops", "前后密码不一样")
                return
            }
            if (_t.motto.length > 200) {
                _t.showError("Oops", "个性签名太长")
                return
            }
            let param = new URLSearchParams()
            param.append('uname', _t.uname)
            param.append('pword', _t.pword)
            param.append('email', _t.email)
            param.append('motto', _t.motto)
            _t.$axios.post(`${_t.$store.state.backendURL}/api/user/reg/`, param).then((res) => {
                _t.isOping = false
                if (res.data.code != 0)
                    _t.showError("Oops", res.data.mes)
                else {
                    _t.$store.commit('updateUser', res.data.user)
                    Swal.fire(
                        "注册成功",
                        res.data.mes,
                        'success'
                    ).then(() => {
                        _t.$router.push("/")
                    })
                }
            }).catch((error) => {
                Swal.fire(
                    'Oops',
                    error.message,
                    'error',
                )
            })
        }
    }
}
</script>