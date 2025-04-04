<!-- src/components/Homepage.vue -->
<template>
    <div class="homepage">
        <!-- Navigation Bar -->
        <nav class="navbar">
            <div class="logo">TeleDocY</div>
            <ul class="nav-links">
                <li><router-link to="/">Home</router-link></li>
                <li><router-link to="/consult">Consulations</router-link></li>
                <li><router-link to="/about">About Us</router-link></li>
                <li><router-link to="/symptom-checker">Symptom Checker</router-link></li>
                <li><router-link to="/pharmacy">Pharmacy</router-link></li>
                <li><router-link to="/profile">Profile</router-link></li>
            </ul>
        </nav>

        <!-- Hero Section -->
        <header class="hero">
            <div class="hero-overlay">
                <h1>Welcome to TeleDocY</h1>
                <p>
                    Your trusted telehealth portal connecting you to quality
                    healthcare from the comfort of your home.
                </p>
                <router-link to="/consult" class="btn">Consultation Services</router-link>
            </div>
        </header>

        <!-- About Us Section -->
        <section class="about-us">
            <h2>About Us</h2>
            <p>
                We are TeleDocY, committed to revolutionizing healthcare with
                innovative telemedicine services. [Customize your About Us text here.]
            </p>
        </section>

      

        <!-- Footer -->
        <footer>
            <p>&copy; 2025 TeleDocY. All rights reserved.</p>
        </footer>
    </div>
</template>

<script>
export default {
    name: 'Homepage',
};
</script>

<style scoped>
/* General Styles */
.homepage {
    font-family: 'Arial', sans-serif;
    color: #333;
}

/* Navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1em;
    background-color: #4caf50;
}

.navbar .logo {
    font-size: 1.5em;
    color: white;
    font-weight: bold;
}

.nav-links {
    list-style: none;
    display: flex;
    gap: 1em;
}

.nav-links li a {
    text-decoration: none;
    color: white;
}

/* Hero Section */
.hero {
    position: relative;
    background: url('@/assets/hero-bg.jpg') center center/cover no-repeat;
    height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.hero-overlay {
    background-color: rgba(0, 0, 0, 0.5);
    padding: 2em;
    border-radius: 8px;
    text-align: center;
    color: #fff;
}

.hero h1 {
    font-size: 3em;
    margin-bottom: 0.5em;
}

.hero p {
    font-size: 1.2em;
    margin-bottom: 1em;
}

.btn {
    background-color: #4caf50;
    color: #fff;
    padding: 0.75em 1.5em;
    text-decoration: none;
    border-radius: 4px;
    font-weight: bold;
    transition: background-color 0.3s;
}

.btn:hover {
    background-color: #45a049;
}

/* About Us Section */
.about-us {
    padding: 2em;
    text-align: center;
    background-color: #f7f7f7;
}

.about-us h2 {
    font-size: 2em;
    margin-bottom: 0.5em;
}

.about-us p {
    font-size: 1em;
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto;
}

/* Media Section */
.media {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    padding: 2em;
    gap: 1.5em;
}

.media-item {
    flex: 1 1 300px;
    text-align: center;
}

.media-item img,
.media-item video {
    max-width: 100%;
    border-radius: 8px;
}

/* Footer */
footer {
    background-color: #333;
    color: #fff;
    text-align: center;
    padding: 1em;
}
</style>
