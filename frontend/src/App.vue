<!-- src/App.vue -->
<template>
    <div id="app">
        <nav>
            <router-link to="/" class="tab" exact>Home</router-link>
            <router-link to="/consult" class="tab"
                >Consultation Services</router-link
            >
        </nav>
        <router-view />
    </div>
</template>

<script setup>
// No additional logic is needed here.
</script>

<style scoped>
nav {
    background-color: #eee;
    padding: 1em;
    text-align: center;
}
.tab {
    margin: 0 1em;
    text-decoration: none;
    color: #333;
    font-weight: bold;
}
.tab.router-link-active {
    color: #4caf50;
    border-bottom: 2px solid #4caf50;
}
</style>
