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
        responseMessage.value = '⚠️ Error connecting to the server.';
    }

    isLoading.value = false;
};
</script>

<template>
    <!-- Navigation Bar -->
    <nav class="navbar">
        <div class="logo">TeleDocY</div>
        <ul class="nav-links">
            <li><router-link to="/">Home</router-link></li>
            <li><router-link to="/consult">Consultations</router-link></li>
            <li><router-link to="/about">About Us</router-link></li>
            <li><router-link to="/symptom">Symptom Checker</router-link></li>
            <li><router-link to="/pharmacy">Pharmacy</router-link></li>
            <li><router-link to="/profile">Profile</router-link></li>
        </ul>
    </nav>

    <!-- Hero -->
    <header class="hero">
        <div class="hero-overlay">
            <h1>Welcome to TeleDocY</h1>
            <p>Your trusted telehealth portal connecting you to quality healthcare from the comfort of your home.</p>
            <router-link to="/consult" class="btn">Consultation Services</router-link>
        </div>
    </header>

    <!-- Consultation Form -->
    <div class="consult-container">
        <h2>Consult a Doctor</h2>
        <p class="subtitle">Describe your symptoms below and a doctor will respond shortly.</p>

        <textarea
            v-model="symptoms"
            placeholder="e.g. I’ve had a persistent sore throat and mild fever for the past two days..."
        ></textarea>

        <button @click="consultDoctor" :disabled="isLoading">
            {{ isLoading ? 'Consulting...' : 'Consult Doctor' }}
        </button>

        <p v-if="responseMessage" class="response-msg">{{ responseMessage }}</p>
    </div>

    <!-- Footer -->
    <footer>
        <p>&copy; 2025 TeleDocY. All rights reserved.</p>
    </footer>
</template>

<style scoped>
/* Consultation Container */
 /* Reuse your navbar styling */
 .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1em;
    background-color: #4caf50;
  }
.consult-container {
    max-width: 700px;
    margin: 3em auto;
    background: #fff;
    padding: 2em;
    border-radius: 1em;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    text-align: center;
    font-family: 'Arial', sans-serif;
}
.consult-container h2 {
    font-size: 2em;
    margin-bottom: 0.5em;
}
.subtitle {
    color: #666;
    margin-bottom: 1.5em;
}

textarea {
    width: 100%;
    height: 120px;
    padding: 1em;
    font-size: 1em;
    border: 1px solid #ccc;
    border-radius: 8px;
    resize: none;
    margin-bottom: 1em;
    transition: border-color 0.3s;
}
textarea:focus {
    border-color: #4caf50;
    outline: none;
}

button {
    background-color: #4caf50;
    color: white;
    padding: 0.75em 2em;
    border: none;
    border-radius: 8px;
    font-size: 1em;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s;
}
button:disabled {
    background-color: #a5d6a7;
    cursor: not-allowed;
}
button:hover:not(:disabled) {
    background-color: #45a049;
}

.response-msg {
    margin-top: 1.5em;
    font-weight: bold;
    color: #333;
}

/* Footer */
footer {
    background-color: #333;
    color: #fff;
    text-align: center;
    padding: 1em;
    margin-top: 4em;
}
</style>
