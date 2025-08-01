<template>
  <div id="app">
    <header class="header">
      <h1>Airport Visualization</h1>
    </header>
    
    <main class="main-content">
      <div v-if="loading" class="loading">
        <p>Loading airport data...</p>
      </div>
      
      <div v-else-if="airports.length > 0" class="airport-container">
        <!-- Search Box -->
        <div class="search-container">
          <input
            v-model="searchTerm"
            type="text"
            placeholder="Search airports by name, city, state, or codes..."
            class="search-input"
          />
          <div class="search-info">
            <span v-if="searchTerm && filteredAirports.length > 0">
              Showing {{ filteredAirports.length }} of {{ airports.length }} airports
            </span>
            <span v-else-if="searchTerm && filteredAirports.length === 0">
              No airports found matching "{{ searchTerm }}"
            </span>
            <span v-else>
              {{ airports.length }} airports total
            </span>
          </div>
        </div>

        <!-- Airport Grid -->
        <div class="airport-grid">
          <div 
            v-for="(airport, index) in filteredAirports" 
            :key="index"
            class="airport-card"
          >
            <h3 class="airport-name">{{ airport.Airport }}</h3>
            <p class="airport-location">{{ airport.City }}, {{ airport.StateAbbreviation }}</p>
            <div class="airport-codes">
              <span class="code-item">FAA: {{ airport.FAA }}</span>
              <span class="code-item">IATA: {{ airport.IATA }}</span>
              <span class="code-item">ICAO: {{ airport.ICAO }}</span>
            </div>
            <p class="airport-role">Role: {{ airport.Role }}</p>
            <p class="airport-enplanements">Enplanements: {{ airport.Enplanements }}</p>
            <p class="airport-state">State: {{ airport.State }}</p>
          </div>
        </div>
      </div>
      
      <div v-else class="no-data">
        <p>No airport data available.</p>
      </div>
    </main>
  </div>
</template>

<script>
import { fetchAirportData } from './data/airports.js'

export default {
  name: 'App',
  data() {
    return {
      airports: [],
      loading: true,
      searchTerm: ''
    }
  },
  computed: {
    filteredAirports() {
      if (!this.searchTerm.trim()) {
        return this.airports;
      }
      
      const searchLower = this.searchTerm.toLowerCase();
      
      return this.airports.filter(airport => {
        // Check if search term matches any airport field
        return (
          airport.Airport.toLowerCase().includes(searchLower) ||
          airport.City.toLowerCase().includes(searchLower) ||
          airport.State.toLowerCase().includes(searchLower) ||
          airport.StateAbbreviation.toLowerCase().includes(searchLower) ||
          airport.FAA.toLowerCase().includes(searchLower) ||
          airport.IATA.toLowerCase().includes(searchLower) ||
          airport.ICAO.toLowerCase().includes(searchLower) ||
          airport.Role.toLowerCase().includes(searchLower) ||
          airport.Enplanements.toLowerCase().includes(searchLower)
        );
      });
    }
  },
  async mounted() {
    try {
      this.airports = await fetchAirportData();
    } catch (error) {
      console.error('Failed to load airport data:', error);
    } finally {
      this.loading = false;
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

.airport-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.search-container {
  background: rgba(255, 255, 255, 0.95);
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.search-input {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.3s ease;
  font-family: inherit;
}

.search-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.search-input::placeholder {
  color: #999;
}

.search-info {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
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

.airport-location {
  color: #666;
  font-size: 1rem;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.airport-codes {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.code-item {
  background: #f8f9fa;
  padding: 0.3rem 0.7rem;
  border-radius: 5px;
  border: 1px solid #e9ecef;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  color: #333;
}

.airport-role {
  color: #666;
  font-size: 0.9rem;
  font-style: italic;
  margin-bottom: 0.5rem;
}

.airport-enplanements {
  color: #666;
  font-size: 0.9rem;
  font-style: italic;
  margin-bottom: 0.5rem;
}

.airport-state {
  color: #666;
  font-size: 0.9rem;
  font-style: italic;
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

.loading {
  background: rgba(255, 255, 255, 0.95);
  padding: 3rem;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.loading p {
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
  
  .search-input {
    font-size: 1rem;
    padding: 0.8rem;
  }
}
</style>
