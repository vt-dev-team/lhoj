<script setup>
const g = process.env.NODE_ENV
</script>

<template>
    <div class="v-footer">
        <div class="container">
            {{ $store.state.ojName }} powered by
            <a
                href="https://github.com/vt-dev-team/lhoj"
                target="_blank"
            >LHOJ</a> v1.0.1 beta.
            <div style="float:right">Designed & Developed by vt-dev-team.</div>
        </div>
    </div>
</template>

<style>
.v-footer {
    padding: 20px 0px;
    margin-top: 50px;
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.2);
    color: #818283;
}
</style>