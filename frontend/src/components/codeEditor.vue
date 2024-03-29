<template>
    <div class="editor" ref="dom"></div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import * as monaco from 'monaco-editor';

const props = defineProps({
    modelValue: String,
});

import editorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker'
const emit = defineEmits(['update:modelValue']);

self.MonacoEnvironment = {
    getWorker(_, label) {
        return new editorWorker()
    }
}

const dom = ref();
let instance;

onMounted(() => {
    const pythonModel = monaco.editor.createModel(props.modelValue, 'python');
    monaco.editor.defineTheme('tomorrow', {
        "base": "vs",
        "inherit": true,
        "rules": [
            {
                "foreground": "8e908c",
                "token": "comment"
            },
            {
                "foreground": "666969",
                "token": "keyword.operator.class"
            },
            {
                "foreground": "666969",
                "token": "constant.other"
            },
            {
                "foreground": "666969",
                "token": "source.php.embedded.line"
            },
            {
                "foreground": "c82829",
                "token": "variable"
            },
            {
                "foreground": "c82829",
                "token": "support.other.variable"
            },
            {
                "foreground": "c82829",
                "token": "string.other.link"
            },
            {
                "foreground": "c82829",
                "token": "string.regexp"
            },
            {
                "foreground": "c82829",
                "token": "entity.name.tag"
            },
            {
                "foreground": "c82829",
                "token": "entity.other.attribute-name"
            },
            {
                "foreground": "c82829",
                "token": "meta.tag"
            },
            {
                "foreground": "c82829",
                "token": "declaration.tag"
            },
            {
                "foreground": "f5871f",
                "token": "constant.numeric"
            },
            {
                "foreground": "f5871f",
                "token": "constant.language"
            },
            {
                "foreground": "f5871f",
                "token": "support.constant"
            },
            {
                "foreground": "f5871f",
                "token": "constant.character"
            },
            {
                "foreground": "f5871f",
                "token": "variable.parameter"
            },
            {
                "foreground": "f5871f",
                "token": "punctuation.section.embedded"
            },
            {
                "foreground": "f5871f",
                "token": "keyword.other.unit"
            },
            {
                "foreground": "c99e00",
                "token": "entity.name.class"
            },
            {
                "foreground": "c99e00",
                "token": "entity.name.type.class"
            },
            {
                "foreground": "c99e00",
                "token": "support.type"
            },
            {
                "foreground": "c99e00",
                "token": "support.class"
            },
            {
                "foreground": "718c00",
                "token": "string"
            },
            {
                "foreground": "718c00",
                "token": "constant.other.symbol"
            },
            {
                "foreground": "718c00",
                "token": "entity.other.inherited-class"
            },
            {
                "foreground": "718c00",
                "token": "markup.heading"
            },
            {
                "foreground": "3e999f",
                "token": "keyword.operator"
            },
            {
                "foreground": "3e999f",
                "token": "constant.other.color"
            },
            {
                "foreground": "4271ae",
                "token": "entity.name.function"
            },
            {
                "foreground": "4271ae",
                "token": "meta.function-call"
            },
            {
                "foreground": "4271ae",
                "token": "support.function"
            },
            {
                "foreground": "4271ae",
                "token": "keyword.other.special-method"
            },
            {
                "foreground": "4271ae",
                "token": "meta.block-level"
            },
            {
                "foreground": "8959a8",
                "token": "keyword"
            },
            {
                "foreground": "8959a8",
                "token": "storage"
            },
            {
                "foreground": "8959a8",
                "token": "storage.type"
            },
            {
                "foreground": "373b41",
                "background": "e0e0e0",
                "token": "meta.separator"
            }
        ],
        "colors": {
            "editor.foreground": "#4D4D4C",
            "editor.background": "#FFFFFF",
            "editor.selectionBackground": "#D6D6D6",
            "editor.lineHighlightBackground": "#EFEFEF",
            "editorCursor.foreground": "#AEAFAD",
            "editorWhitespace.foreground": "#D1D1D1"
        }
    })
    instance = monaco.editor.create(dom.value, {
        model: pythonModel,
        tabSize: 4,
        automaticLayout: true,
        fontSize: 16,
        scrollBeyondLastLine: false,
        theme: 'tomorrow'
    });

    instance.onDidChangeModelContent(() => {
        const value = instance.getValue();
        emit('update:modelValue', value);
    });
});
</script>

<style scoped>
.editor {
    height: 100%;
}
</style>