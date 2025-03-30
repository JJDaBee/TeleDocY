<template>
    <div class="payment-page">
      <!-- Navigation -->
      <nav class="navbar">
        <div class="logo">TeleDocY</div>
        <ul class="nav-links">
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/consult">Consultations</router-link></li>
          <li><router-link to="/pharmacy">Pharmacy</router-link></li>
          <li><router-link to="/profile">Profile</router-link></li>
        </ul>
      </nav>
  
      <!-- Payment Container -->
      <div class="payment-container">
        <h2 class="title">Confirm Your Payment</h2>
  
        <!-- Medicines Box -->
        <div class="medicine-box">
          <h3>Prescribed Medicines</h3>
          <ul>
            <li v-for="(med, index) in medicines" :key="index">
              <span>{{ med.name }} × {{ med.quantity }}</span>
              <span>${{ (med.quantity * med.price).toFixed(2) }}</span>
            </li>
          </ul>
        </div>
  
        <!-- Subtotal / Total -->
        <div class="price-summary">
          <div class="line">
            <span>Subtotal</span>
            <span>${{ subtotal.toFixed(2) }}</span>
          </div>
          <div class="line total">
            <span>Total</span>
            <span>${{ subtotal.toFixed(2) }}</span>
          </div>
        </div>
  
        <!-- Action Buttons -->
        <div class="action-buttons">
          <button class="back-btn" @click="$router.back()">Back</button>
          <button class="pay-btn" :disabled="loading" @click="handleStripePayment">
            {{ loading ? 'Redirecting...' : 'Pay with Stripe' }}
          </button>
        </div>
      </div>
  
      <!-- Footer -->
      <footer>
        <p>&copy; 2025 TeleDocY. All rights reserved.</p>
      </footer>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PaymentPage',
    data() {
      return {
        loading: false,
        medicines: [
          { name: 'Panadol 500mg', quantity: 2, price: 3.5 },
          { name: 'Cough Syrup', quantity: 1, price: 5.0 },
        ],
      };
    },
    computed: {
      subtotal() {
        return this.medicines.reduce((acc, med) => acc + med.quantity * med.price, 0);
      },
    },
    methods: {
      async handleStripePayment() {
        this.loading = true;
        try {
          const res = await fetch('/api/create-checkout-session', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              consultationId: this.$route.params.consultationId, // example
            }),
          });
          const data = await res.json();
          window.location.href = data.url;
        } catch (err) {
          alert('Failed to redirect to Stripe.');
          console.error(err);
        } finally {
          this.loading = false;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .payment-page {
    font-family: 'Arial', sans-serif;
    color: #333;
    background-color: #f7f7f7;
    min-height: 100vh;
  }
  
  /* Reuse your navbar styling */
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
  
  /* Main container */
  .payment-container {
    max-width: 600px;
    margin: 2em auto;
    background: #fff;
    padding: 2em;
    border-radius: 1em;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .title {
    text-align: center;
    font-size: 2em;
    margin-bottom: 1em;
  }
  
  /* Medicine box */
  .medicine-box {
    background-color: #e9f5eb;
    border: 1px solid #c6e5d3;
    border-radius: 10px;
    padding: 1em;
    margin-bottom: 1.5em;
  }
  
  .medicine-box h3 {
    font-size: 1.2em;
    margin-bottom: 0.5em;
  }
  
  .medicine-box ul {
    list-style: none;
    padding: 0;
  }
  
  .medicine-box li {
    display: flex;
    justify-content: space-between;
    padding: 0.3em 0;
  }
  
  /* Price summary */
  .price-summary .line {
    display: flex;
    justify-content: space-between;
    margin: 0.5em 0;
  }
  
  .price-summary .total {
    font-weight: bold;
    font-size: 1.2em;
  }
  
  /* Buttons */
  .action-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 1.5em;
  }
  
  .back-btn,
  .pay-btn {
    flex: 1;
    margin: 0 0.5em;
    padding: 0.8em;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
  }
  
  .back-btn {
    background-color: #ccc;
  }
  
  .pay-btn {
    background-color: #4caf50;
    color: white;
  }
  
  .pay-btn:hover {
    background-color: #45a049;
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
  