<template>
  <div id="app">
    <header class="header">
      <h1>Airport Visualization</h1>
    </header>
    
    <main class="main-content">
      <div v-if="airports.length > 0" class="airport-grid">
        <div 
          v-for="(airport, index) in airports" 
          :key="index"
          class="airport-card"
        >
          <div class="airport-icon">✈️</div>
          <h3 class="airport-name">{{ airport.name }}</h3>
          <p class="airport-ssid">SSID: {{ airport.ssid }}</p>
        </div>
      </div>
      
      <div v-else class="no-data">
        <p>No airport data available.</p>
      </div>
    </main>
  </div>
</template>

<script>
import { airportData } from './data/airports.js'

export default {
  name: 'App',
  data() {
    return {
      airports: airportData
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  color: #333;
}

.header {
  background: rgba(255, 255, 255, 0.95);
  padding: 2rem;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header h1 {
  color: #2c3e50;
  font-size: 2.5rem;
  font-weight: 300;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.airport-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.airport-card {
  background: rgba(255, 255, 255, 0.95);
  padding: 2rem;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.airport-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.airport-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.airport-name {
  color: #2c3e50;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.airport-ssid {
  color: #666;
  font-size: 1rem;
  font-family: 'Courier New', monospace;
  background: #f8f9fa;
  padding: 0.5rem;
  border-radius: 5px;
  border: 1px solid #e9ecef;
}

.no-data {
  background: rgba(255, 255, 255, 0.95);
  padding: 3rem;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.no-data p {
  color: #666;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .header h1 {
    font-size: 2rem;
  }
  
  .main-content {
    padding: 1rem;
  }
  
  .airport-grid {
    grid-template-columns: 1fr;
  }
}
</style>
