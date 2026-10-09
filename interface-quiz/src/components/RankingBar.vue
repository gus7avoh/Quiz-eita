<script lang="ts" setup>

const ranking: string[] = [
    "Gustavo",
    "Guilherme",
    "Matheus",
    "Thiago",
    "Vitor",
    "Nayara",
]

</script>

<template>
    <section class="side-bar">

        <div class="title">

            <div class="radio-input">

                <label class="label">
                    <input type="radio" name="value-radio" />
                    <span class="check"></span>
                </label>

                <label class="label">
                    <input type="radio" name="value-radio" />
                    <span class="check"></span>
                </label>

                <label class="label">
                    <input type="radio" name="value-radio" />
                    <span class="check"></span>
                </label>

                <label class="label">
                    <input type="radio" name="value-radio" />
                    <span class="check"></span>
                </label>

                <label class="label">
                    <input type="radio" name="value-radio" />
                    <span class="check"></span>
                </label>

            </div>

            <h1>Ranking</h1>

        </div>

        <div v-for="(player, index) in ranking"
            :key="player"
            class="ranking-item"
            :class="index % 2 === 0 ? 'light' : 'dark'"
        >
            {{ player }}
        </div>

    </section>
</template>

<style scoped>

.side-bar {
    box-sizing: border-box;
    padding: 20px;
    min-height: 0;
    min-width: 0;
    width:100%;
    height: 100%;
    background-color: #444;
    border-radius: 15px;
    overflow: hidden;
    
}

.title {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 1.01rem;
    font-family: 'Rubik Marker Hatch', cursive;
    font-weight: normal;
    color: var(--primary-color);
    margin: 0 0 20px 0;
}

.title h1 {
    margin: 10px 0 0 0;
}

.radio-input {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: clamp(8px, 2vw, 20px);
}

.radio-input .label input {
    display: none;
}

.radio-input .label {
    display: flex;
}

.radio-input .label .check {
    width: 30px;
    height: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    cursor: pointer;
    transition: 0.3s;
    border: 3px solid transparent;
    box-shadow:
        3px 3px 6px rgba(0, 0, 0, 0.5),
        -1px -1px 4px rgba(255, 255, 255, 0.5);
}

.radio-input .label input:checked + .check {
    box-shadow:
        3px 3px 6px rgba(0, 0, 0, 0.5),
        -1px -1px 4px rgba(255, 255, 255, 0.5),
        inset 3px 3px 6px rgba(0, 0, 0, 0.5),
        inset -1px -1px 4px rgba(255, 255, 255, 0.5);

    transform: scale(1.1);
}

.ranking-item {
    padding: 10px;
    border-radius: 5px;
    color: #fff;
    font-size: 1rem;
    font-family: 'Courier New', monospace;
    margin-bottom: 10px;
    font-weight: bold;
}

.light {
    background-color: #555;
}

.dark {
    background-color: #3a3a3a;
}

</style>