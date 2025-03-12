<script setup>
import { ref } from 'vue';

const symptoms = ref('');
const responseMessage = ref('');
const isLoading = ref(false);

console.log('🔍 Using API URL:', import.meta.env.VITE_API_URL);

const consultDoctor = async () => {
    isLoading.value = true;
    responseMessage.value = '';

    try {
        const response = await fetch(
            `${import.meta.env.VITE_API_URL}/api/consultation`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    symptoms: symptoms.value,
                    nric: 'T0123456A',
                }),
            }
        );

        const data = await response.json();
        responseMessage.value = data.message || 'Consultation request sent!';
    } catch (error) {
        responseMessage.value = 'Error connecting to the server.';
    }

    isLoading.value = false;
};
</script>

<template>
    <div class="container">
        <h1>Consult a Doctor</h1>
        <textarea
            v-model="symptoms"
            placeholder="Describe your symptoms..."
        ></textarea>
        <button @click="consultDoctor" :disabled="isLoading">
            {{ isLoading ? 'Consulting...' : 'Consult Doctor' }}
        </button>
        <p v-if="responseMessage">{{ responseMessage }}</p>
    </div>
</template>

<style>
.container {
    text-align: center;
    padding: 20px;
}
textarea {
    width: 80%;
    height: 100px;
    margin: 10px 0;
}
button {
    padding: 10px;
    cursor: pointer;
}
</style>
