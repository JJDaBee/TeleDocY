<template>
    <div class="container">
      <h2>Symptom Checker</h2>
  
      <form @submit.prevent="submitForm" class="form">
        <div class="form-group">
          <label for="uuid">Patient UUID:</label>
          <input v-model="uuid" id="uuid" type="text" required />
        </div>
  
        <div class="form-group">
          <label for="symptom">Symptom Description:</label>
          <textarea v-model="symptom" id="symptom" rows="4" required></textarea>
        </div>
  
        <button type="submit">Check Symptoms</button>
      </form>
  
      <div v-if="response" class="response">
        <h3>Patient Info</h3>
        <pre>{{ response.patient_info }}</pre>
  
        <h3>Consultation History</h3>
        <pre>{{ response.consultation_history }}</pre>
  
        <h3>AI Response</h3>
        <p>{{ response.ai_response }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "SymptomChecker",
    data() {
      return {
        uuid: "",
        symptom: "",
        response: null,
      };
    },
    methods: {
      async submitForm() {
        try {
          const res = await fetch("http://localhost:8000/check-symptoms", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              uuid: this.uuid,
              symptom_description: this.symptom,
            }),
          });
  
          if (!res.ok) {
            throw new Error("Failed to fetch response");
          }
  
          const data = await res.json();
          this.response = data;
        } catch (error) {
          console.error(error);
          alert("Something went wrong. Please try again.");
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
    margin: 40px auto;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px #ccc;
    background-color: #f9f9f9;
  }
  
  h2 {
    text-align: center;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    font-weight: bold;
  }
  
  input,
  textarea {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    box-sizing: border-box;
  }
  
  button {
    display: block;
    width: 100%;
    padding: 10px;
    font-size: 16px;
    background-color: #007acc;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .response {
    margin-top: 30px;
    background: #fff;
    padding: 20px;
    border-radius: 5px;
  }
  </style>
  