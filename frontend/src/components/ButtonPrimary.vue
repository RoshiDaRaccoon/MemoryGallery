<script setup>
defineProps({
    msg: {
        type: String,
        required: true,
    },
    classes: {
        type: String,
        required: false,
    }
})
</script>

<template>
    <button class="title-button" :class="classes">{{ msg }}</button>
</template>

<style scoped>
.title-button {
    padding: 0.5em 3em;
    background-color: #E0EDAB;
    border: #3F2B4C 2px solid;
    border-radius: 3em;
    font-size: 1.3rem;
    font-weight: 600;
    transition: transform 0.3s ease;

    &:hover {
        transform: scale(1.1);
    }
}

@media (max-width: 1200px) {
    .title-button {
        margin-top: 1em;
        padding: 0.5em 1.5em;
        margin-left: 0;
    }
}
</style>