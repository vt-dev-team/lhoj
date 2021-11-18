<template>
    <div class="row">
        <div class="col-md-8 col-sm-12 order-md-1 order-2">
            <div class="card">
                <div class="card-body">
                    <form @submit="uploadData">
                        <div class="form-group">
                            <label>数据文件(zip格式)</label>
                            <div class="input-group">
                                <div class="custom-file">
                                    <input type="file" class="custom-file-input" @change="getFile" />
                                    <label class="custom-file-label">{{ fileName }}</label>
                                </div>
                                <div class="input-group-append">
                                    <button class="btn btn-primary" v-if="!isSubmit">上传</button>
                                    <button class="btn btn-primary" disabled v-else>
                                        <span
                                            class="spinner-border spinner-border"
                                            role="status"
                                            aria-hidden="true"
                                        ></span>
                                        上传
                                    </button>
                                </div>
                            </div>
                        </div>
                    </form>
                    <div class="progress" v-if="showProcess">
                        <div
                            class="progress-bar"
                            :class="{ 'bg-danger': isError }"
                            role="progressbar"
                            :style="`width: ${progress}%;`"
                            aria-valuenow="25"
                            aria-valuemin="0"
                            aria-valuemax="1000"
                        ></div>
                    </div>
                    <p>
                        说明：zip文件夹中
                        <b class="text-danger">不能</b>有子文件夹，根目录下
                        <b class="text-danger">必须</b>有配置文件config.lh
                    </p>
                    <p>config.lh内容为json格式，可直接使用以下模板</p>
                    <details>
                        <pre><code>{
    "time": 1000, <span class="comt">//时间限制ms(可选，默认1000)</span>
    "memory": 262144, <span class="comt">//空间限制kb(可选，默认262144)</span>
    "template": "template.py",<span class="comt">//模板文件(可选，默认无)</span>
    "checker": "checker.py",<span class="comt">//校验器文件(可选，默认无)</span>
    "datas": [<span class="comt">//数据组</span>
    {
        "in": "data1.in",<span class="comt">//输入文件(必选)</span>
        "out": "data1.out",<span class="comt">//输出文件(必选)</span>
        "score": 100<span class="comt">//测试点得分(必选)</span>
    }
    ]
}</code></pre>
                    </details>
                </div>
            </div>
            <div class="card">
                <div class="card-body">
                    <h3>数据配置</h3>
                    <table>
                        <tr>
                            <th>时间限制</th>
                            <td>{{ configlh.time }}ms</td>
                        </tr>
                        <tr>
                            <th>空间限制</th>
                            <td>{{ configlh.memory }}KB</td>
                        </tr>
                        <tr v-if="configlh.template">
                            <th>模板文件</th>
                            <td>{{ configlh.template }}</td>
                        </tr>
                        <tr v-if="configlh.checker">
                            <th>校验器</th>
                            <td>{{ configlh.checker }}</td>
                        </tr>
                    </table>
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>输入文件</th>
                                <th>输出文件</th>
                                <th>分值</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(d,i) in configlh.datas" v-bind:key="i">
                                <td>{{ i + 1 }}</td>
                                <td>{{ d.in }}</td>
                                <td>{{ d.out }}</td>
                                <td>{{ d.score }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div class="col-md-4 col-sm-12 order-md-2 order-1">
            <template v-if="($store.state.loginUser.privilege & 2048) > 0">
                <ul class="contest-menu">
                    <li>
                        <router-link
                            :to="{ name: 'ProblemShow', params: { id: $route.params.id } }"
                        >
                            <i class="fas fa-eye"></i>题目查看
                        </router-link>
                    </li>
                    <li>
                        <router-link
                            :to="{ name: 'ProblemEdit', params: { id: $route.params.id } }"
                        >
                            <i class="fas fa-edit"></i>题目编辑
                        </router-link>
                    </li>
                    <li>
                        <router-link
                            :to="{ name: 'ProblemData', params: { id: $route.params.id } }"
                        >
                            <i class="fas fa-database"></i>数据配置
                        </router-link>
                    </li>
                </ul>
            </template>
            <br />
        </div>
    </div>
</template>
<style scoped>
.comt {
    user-select: none;
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
            isSubmit: true,
            fileList: [],
            fileName: "请选择文件(*.zip)",
            configlh: {},
            showProcess: false,
            progress: 0,
            isError: false,
        }
    },
    mounted() {
        const _t = this
        _t.$store.commit('changeTitle', `数据配置#${_t.$route.params.id}`)
        _t.getConfig()
    },
    methods: {
        getFile(e) {
            let fis = e.target.files;
            for (let i = 0; i < fis.length; ++i) {
                let dataName = fis[i].name
                let idx = dataName.lastIndexOf(".")
                if (idx != -1) {
                    let ext = dataName.substr(idx + 1).toUpperCase()
                    if (ext != 'ZIP')
                        Toast.fire('出错了', '需要.zip文件', 'error')
                    else {
                        if (this.fileList.length == 0)
                            this.fileList.push(fis[i])
                        else
                            this.fileList[0] = fis[i]
                        this.fileName = this.fileList[0].name
                    }
                }
                else
                    Toast.fire('出错了', '需要.zip文件', 'error')
            }
        },
        getConfig() {
            let _t = this
            _t.$axios.get(`${_t.$store.state.backendURL}/api/problem/${_t.$route.params.id}/data/`).then((res) => {
                if (res.data.code != 0) {
                    Toast.fire(
                        'Oops',
                        res.data.mes,
                        'error',
                    )
                }
                else {
                    _t.configlh = res.data.data
                    _t.isSubmit = false
                }
            })
        },
        uploadData(e) {
            const _t = this
            e.preventDefault()
            _t.isSubmit = true
            if (_t.fileList.length == 0) {
                Toast.fire('出错了', '请选择文件', 'error')
                return
            }
            Swal.fire({
                title: '上传文件?',
                text: `即将上传文件${_t.fileList[0].name}, 大小为${_t.formatSize(_t.fileList[0].size)}!`,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes!'
            }).then((result) => {
                if (result.value) {
                    let formData = new FormData()
                    formData.append('dataFile', _t.fileList[0])
                    _t.$axios({
                        url: `${_t.$store.state.backendURL}/api/problem/${_t.$route.params.id}/upload/`,
                        method: 'post',
                        data: formData,
                        onUploadProgress: progressEvent => {
                            this.showProcess = true
                            let process = (progressEvent.loaded / progressEvent.total * 100 | 0)
                            this.progress = process
                        }
                    }).then((res) => {
                        this.showProcess = false
                        if (res.data.code != 0) {
                            Toast.fire(
                                'Oops',
                                res.data.mes,
                                'error',
                            )
                            _t.isSubmit = false
                        }
                        else {
                            Toast.fire(
                                '成功',
                                "上传成功",
                                'success',
                            ).then(() => {
                                _t.getConfig()
                            })
                        }
                    }).catch((e) => {
                        _t.isError = true
                        Toast.fire(
                            '失败',
                            e.message,
                            'error',
                        )
                    })
                }
            })
        },
        formatSize(q) {
            let dlevel = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
            let level = 0
            while (q >= 1024) {
                q = q / 1024;
                level += 1
            }
            return `${q.toFixed(2)}${dlevel[level]}`
        }
    }
}
</script>