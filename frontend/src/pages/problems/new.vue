<template>
    <div>
        <div class="card">
            <div class="card-body">
                <form @submit="NewPost">
                    <div class="form-group">
                        <label>标题</label>
                        <input type="text" class="form-control" v-model="Title" />
                    </div>
                    <div class="row">
                        <div class="col">
                            <div class="form-group">
                                <label>时间限制(ms)</label>
                                <input type="text" class="form-control" v-model="TimeLimit" />
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-group">
                                <label>空间限制(KiB)</label>
                                <input type="text" class="form-control" v-model="MemoryLimit" />
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-group">
                                <label class="vtooltip">
                                    测评方法
                                    <span class="tooltiptext">仅显示，具体配置在测试数据中</span>
                                </label>
                                <select v-model="judgeType" class="form-control">
                                    <option value="0">传统</option>
                                    <option value="1">Special Judge</option>
                                    <option value="2">提交答案</option>
                                    <option value="3">交互</option>
                                    <option value="4">程序填空</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="form-group line-numbers">
                        <label>内容</label>
                        <textarea id="PostEditor">### 题目描述

给定两个整数 $A$, $B$，输出 $A+B$ 的值

### 输入格式

一行两个整数 $A$ 和 $B$，空格隔开

### 输出格式

一行一个整数 $A+B$ 的值

### 样例1

#### 样例输入

```
1 2
```

#### 样例输出

```
3
```

### 参考代码

```python
print(sum([int(i) for i in input().split()]))
```

```python
print(eval(input().replace(" ", "+")))
```

```python
n = input().split(" ")
a = int(n[0])
b = int(n[1])
print(a + b)
```</textarea>
                    </div>
                    <div class="form-group">
                        <label for="postTitle">标签(英文,隔开)</label>
                        <input type="text" class="form-control" v-model="Tags" />
                    </div>
                    <div class="form-group">
                        <label for="postTitle">算法(英文,隔开)</label>
                        <input type="text" class="form-control" v-model="Algorithm" />
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
        </div>
    </div>
</template>

<style>
.CodeMirror {
    height: 300px;
}
</style>

<script>
import Swal from 'sweetalert2'
import showdown from 'showdown'
import showdownKatex from 'showdown-katex'
import Prism from 'prismjs'
import 'prismjs/components/prism-python.js'
import '../../statics/line-number.js'
import SimpleMDE from 'simplemde'
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
            PostEditor: '',
            Title: '',
            Algorithm: '',
            Tags: '',
            TimeLimit: 1000,
            MemoryLimit: 262144,
            judgeType: 0,
            nowTime: this.$moment().format("YYYY-MM-DD HH:mm:ss"),
            nowTimeSetter: '',
        }
    },
    mounted() {
        const _t = this
        if ((_t.$store.state.loginUser.privilege & 256) === 0)
            _t.$router.replace('/error/404')
        _t.nowTimeSetter = setInterval(() => { _t.getNowTime() }, 1000)
        _t.$store.commit('changeTitle', '新建问题')
        _t.PostEditor = new SimpleMDE({
            element: document.getElementById("PostEditor"),
            previewRender: function (plainText, preview) { // Async method
                setTimeout(() => {
                    preview.innerHTML = converter.makeHtml(plainText)
                    Prism.highlightAll()
                }, 100)
                return "Loading..."
            },
            spellChecker: false,
            hideIcons: ["guide", "heading", "side-by-side", "fullscreen"],
        })
    },
    beforeUnmount() {
        clearInterval(this.nowTimeSetter)
    },
    methods: {
        getNowTime() {
            this.nowTime = this.$moment().format("YYYY-MM-DD HH:mm:ss")
        },
        NewPost(e) {
            e.preventDefault()
            let _t = this
            let param = new URLSearchParams()
            param.append('title', _t.Title)
            param.append('content', _t.PostEditor.value())
            param.append('time_limit', _t.TimeLimit)
            param.append('memory_limit', _t.MemoryLimit)
            param.append('judge_type', _t.judgeType)
            param.append('tags', _t.Tags)
            param.append('algorithm', _t.Algorithm)
            _t.$axios.post(`${_t.$store.state.backendURL}/api/problem/new/`, param).then((res) => {
                if (res.data.code != 0) {
                    Toast.fire(
                        'Oops',
                        res.data.mes,
                        'error',
                    )
                }
                else {
                    Toast.fire(
                        '成功',
                        "添加成功",
                        'success',
                    ).then(() => {
                        _t.$router.push({
                            name: "ProblemShow",
                            params: {
                                id: res.data.id
                            }
                        })
                    })
                }
            }).catch((error) => {
                Toast.fire(
                    'Oops',
                    error.message,
                    'error',
                )
            })
        }
    }
}
</script>
