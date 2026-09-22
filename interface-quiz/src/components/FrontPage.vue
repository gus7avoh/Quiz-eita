<script lang="ts" setup>
import RankingBar from './RankingBar.vue'
</script>

<template>
    <section class="body">
        <h1 class="title">Eita Quiz</h1>
        <span class="sub_title">Encontro integrador de tecnologia Anhanguera</span>

        <RankingBar />
    </section>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rubik+Marker+Hatch&display=swap');
.body {
    min-height: 30vh;
    width: 100%;
}

.title {
    text-align: center;
    font-size: 70px;
    font-family: 'Rubik Marker Hatch', cursive;
    color: var(--primary-color);
    margin-bottom: 5px;
    margin-top: 0px;
}

.sub_title {
    display: block;
    text-align: center;
    font-size: 20px;
    font-family: 'Rubik Marker Hatch', cursive;
    color: var(--primary-color);
    margin-bottom: 30px;
}
</style>