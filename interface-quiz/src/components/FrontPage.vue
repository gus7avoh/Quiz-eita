<script lang="ts" setup>
import RankingBar from './RankingBar.vue'
import SelectGame from './SelectGame.vue';
</script>

<template>
    <section class="janela">

        <header>
            <h1 class="title">Eita Quiz</h1>
            <span class="sub_title">Encontro integrador de tecnologia Anhanguera</span>
        </header>

        <div class="content_wrapper">

            <aside>
                <RankingBar/>
            </aside>
        
            <main>
                <SelectGame/>
            </main>

        </div>
        
        
    </section>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rubik+Marker+Hatch&display=swap');

.janela{
    width: 100vw;
    height: 100vh;
    display:flex;
    flex-direction: column;
    justify-content: center;
}

header{
    width: 100vw;
}

.content_wrapper{
    display:flex;
    flex:1;
    flex-direction: row;
    gap:20px;
    min-width: 0;
    min-height: 0;
    padding: 0 20px 20px;
    box-sizing: border-box;

}
.content_wrapper main{
    flex:8;
    min-width: 0;
    min-height: 0;
}
.content_wrapper aside {
    flex:2;
    min-width: 0;
    min-height: 0;
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