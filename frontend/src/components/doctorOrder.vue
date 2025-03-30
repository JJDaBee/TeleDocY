<template>
    <div class="order-page">
        <nav class="navbar">
            <div class="logo">TeleDocY</div>
            <ul class="nav-links">
                <li><router-link to="/">Home</router-link></li>
                <li><router-link to="/consult">Consultations</router-link></li>
                <li><router-link to="/profile">Profile</router-link></li>
            </ul>
        </nav>

        <div class="container">
            <h2 class="title">Prescribe Medication</h2>

            <div class="inventory">
                <table>
                    <thead>
                        <tr>
                            <th>Medication</th>
                            <th>Price</th>
                            <th>Qty Left</th>
                            <th>Allergies</th>
                            <th>Prescribe Qty</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="med in medications" :key="med.medicationID">
                            <td>{{ med.medication }}</td>
                            <td>${{ med.price.toFixed(2) }}</td>
                            <td>{{ med.quantityLeft }}</td>
                            <td>{{ med.allergies }}</td>
                            <td>
                                <input type="number" min="0" v-model.number="prescriptions[med.medicationID]"
                                    class="qty-input" />
                            </td>
                            <td>
                                <button class="add-btn" @click="addToOrder(med)"
                                    :disabled="!prescriptions[med.medicationID]">
                                    Add
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Selected Prescriptions -->
            <div class="selected-box" v-if="order.length">
                <h3>Selected Prescriptions</h3>
                <ul>
                    <li v-for="item in order" :key="item.medicationID">
                        {{ item.medication }} x {{ item.quantity }} - ${{ (item.price * item.quantity).toFixed(2) }}
                    </li>
                </ul>
                <div class="total">
                    Total: ${{ total.toFixed(2) }}
                </div>
                <button class="submit-btn" @click="submitOrder">Submit Order</button>
            </div>
        </div>

        <footer>
            <p>&copy; 2025 TeleDocY. All rights reserved.</p>
        </footer>
    </div>
</template>

<script>
export default {
    name: "DoctorOrder",
    data() {
        return {
            // Dummy medications — same structure as your DB model
            medications: [
                {
                    medicationID: 1,
                    medication: "Panadol 500mg",
                    price: 3.50,
                    quantityLeft: 120,
                    nextRestockDate: "2025-04-10",
                    allergies: "None",
                },
                {
                    medicationID: 2,
                    medication: "Amoxicillin",
                    price: 5.20,
                    quantityLeft: 50,
                    nextRestockDate: "2025-04-05",
                    allergies: "Penicillin",
                },
                {
                    medicationID: 3,
                    medication: "Cough Syrup",
                    price: 4.80,
                    quantityLeft: 30,
                    nextRestockDate: "2025-04-08",
                    allergies: "None",
                },
                {
                    medicationID: 4,
                    medication: "Cetirizine 10mg",
                    price: 2.20,
                    quantityLeft: 80,
                    nextRestockDate: "2025-04-12",
                    allergies: "None",
                },
    
      
    

      ],
        prescriptions: { }, // Stores prescribed quantity for each item
        order: [], // Final list of selected items
    };
},
computed: {
    total() {
        return this.order.reduce((acc, item) => acc + item.quantity * item.price, 0);
    },
},
methods: {
    addToOrder(med) {
        const quantity = this.prescriptions[med.medicationID];
        const existing = this.order.find(o => o.medicationID === med.medicationID);
        if (existing) {
            existing.quantity = quantity;
        } else {
            this.order.push({
                ...med,
                quantity,
            });
        }
    },
    submitOrder() {
        alert("Prescription submitted successfully!\n\n" + JSON.stringify(this.order, null, 2));
        this.order = [];
        this.prescriptions = {};
    },
},
};
</script>


<style scoped>
.order-page {
    font-family: 'Arial', sans-serif;
    background-color: #f7f7f7;
    min-height: 100vh;
    color: #333;
}

.navbar {
    display: flex;
    justify-content: space-between;
    padding: 1em;
    background-color: #4caf50;
}

.navbar .logo {
    font-weight: bold;
    color: white;
    font-size: 1.5em;
}

.nav-links {
    display: flex;
    gap: 1em;
    list-style: none;
}

.nav-links a {
    color: white;
    text-decoration: none;
}

.container {
    max-width: 1000px;
    margin: 2em auto;
    padding: 1em;
    background: white;
    border-radius: 1em;
}

.title {
    text-align: center;
    font-size: 2em;
    margin-bottom: 1em;
}

.inventory table {
    width: 100%;
    border-collapse: collapse;
}

.inventory th,
.inventory td {
    padding: 0.75em;
    border-bottom: 1px solid #ccc;
    text-align: left;
}

.qty-input {
    width: 60px;
    padding: 0.3em;
}

.add-btn {
    background: #4caf50;
    color: white;
    padding: 0.4em 1em;
    border: none;
    border-radius: 6px;
    cursor: pointer;
}

.selected-box {
    margin-top: 2em;
    background: #e9f5eb;
    padding: 1em;
    border-radius: 10px;
}

.selected-box ul {
    padding: 0;
    list-style: none;
}

.total {
    font-weight: bold;
    margin-top: 1em;
}

.submit-btn {
    margin-top: 1em;
    background: #4caf50;
    color: white;
    padding: 0.7em 2em;
    border: none;
    border-radius: 6px;
    font-size: 1em;
}

footer {
    background: #333;
    color: white;
    text-align: center;
    padding: 1em;
    margin-top: 2em;
}
</style>