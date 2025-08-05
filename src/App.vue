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
        <!-- Search and View Controls -->
        <div class="controls-container">
          <div class="search-section">
            <input
              v-model="searchTerm"
              type="text"
              placeholder="Search airports..."
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

          <!-- View Toggle -->
          <div class="view-toggle-container">
            <button 
              @click="currentView = 'card'" 
              :class="['view-toggle-btn', { active: currentView === 'card' }]"
            >
              <span class="toggle-icon">📋</span>
              Card View
            </button>
            <button 
              @click="currentView = 'table'" 
              :class="['view-toggle-btn', { active: currentView === 'table' }]"
            >
              <span class="toggle-icon">📊</span>
              Table View
            </button>
          </div>
        </div>

        <!-- Card View -->
        <div v-if="currentView === 'card'" class="airport-grid">
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
            <p class="airport-ssid"><strong>SSID:</strong> {{ airport.SSID }}</p>
            <p class="airport-role">Role: {{ airport.Role }}</p>
            <p class="airport-enplanements">Enplanements: {{ airport.Enplanements }}</p>
            <p class="airport-state">State: {{ airport.State }}</p>
          </div>
        </div>

        <!-- Table View -->
        <div v-else-if="currentView === 'table'" class="table-container">
          <table class="airport-table">
            <thead>
              <tr>
                <th>IATA</th>
                <th>City</th>
                <th>State</th>
                <th>SSID</th>
                <th>Airport</th>
                <th>Enplanements</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="(airport, index) in filteredAirports" 
                :key="index"
                class="table-row"
                @mouseenter="handleMouseEnter(airport, $event)"
                @mouseleave="hoveredAirport = null"
              >
                <td class="code-cell">{{ airport.IATA }}</td>
                <td>{{ airport.City }}</td>
                <td>{{ airport.StateAbbreviation }}</td>
                <td class="ssid-cell">{{ airport.SSID }}</td>
                <td class="airport-name-cell">{{ airport.Airport }}</td>
                <td class="enplanements-cell">{{ airport.Enplanements }}</td>
              </tr>
            </tbody>
          </table>
          
          <!-- Hover Card -->
          <div v-if="hoveredAirport" class="hover-card" :style="hoverCardStyle">
            <h3 class="hover-card-title">{{ hoveredAirport.Airport }}</h3>
            <p class="hover-card-location">{{ hoveredAirport.City }}, {{ hoveredAirport.StateAbbreviation }}</p>
            <div class="hover-card-codes">
              <span class="hover-code-item">FAA: {{ hoveredAirport.FAA }}</span>
              <span class="hover-code-item">IATA: {{ hoveredAirport.IATA }}</span>
              <span class="hover-code-item">ICAO: {{ hoveredAirport.ICAO }}</span>
            </div>
            <p class="hover-card-ssid"><strong>SSID:</strong> {{ hoveredAirport.SSID }}</p>
            <p class="hover-card-role">Role: {{ hoveredAirport.Role }}</p>
            <p class="hover-card-enplanements">Enplanements: {{ hoveredAirport.Enplanements }}</p>
            <p class="hover-card-state">State: {{ hoveredAirport.State }}</p>
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
      searchTerm: '',
      currentView: 'table',
      hoveredAirport: null,
      mousePosition: { x: 0, y: 0 }
    }
  },
  computed: {
    filteredAirports() {
      let filtered = this.airports;
      
      if (this.searchTerm.trim()) {
        const searchLower = this.searchTerm.toLowerCase();
        
        filtered = this.airports.filter(airport => {
          // Check if search term matches any airport field
          return (
            airport.Airport.toLowerCase().replace("airport", "").includes(searchLower) ||
            airport.City.toLowerCase().includes(searchLower) ||
            airport.State.toLowerCase().includes(searchLower) ||
            airport.StateAbbreviation.toLowerCase().includes(searchLower) ||
            airport.FAA.toLowerCase().includes(searchLower) ||
            airport.IATA.toLowerCase().includes(searchLower) ||
            airport.ICAO.toLowerCase().includes(searchLower) ||
            airport.SSID.toLowerCase().includes(searchLower) ||
            airport.Role.toLowerCase().includes(searchLower) ||
            airport.Enplanements.toLowerCase().includes(searchLower)
          );
        });
      }
      
      // Sort by enplanements (descending - highest first)
      return filtered.sort((a, b) => {
        const aEnplanements = parseInt(a.Enplanements.replace(/,/g, '')) || 0;
        const bEnplanements = parseInt(b.Enplanements.replace(/,/g, '')) || 0;
        return bEnplanements - aEnplanements;
      });
    },
    hoverCardStyle() {
      if (!this.hoveredAirport) return {};
      
      // Card dimensions (approximate)
      const cardWidth = 300;
      const cardHeight = 200;
      const offsetX = 20;
      const offsetY = 10;
      
      // Get viewport dimensions
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;
      
      // Calculate initial position
      let left = this.mousePosition.x + offsetX;
      let top = this.mousePosition.y + offsetY;
      
      // Check if card would overflow right edge
      if (left + cardWidth > viewportWidth) {
        left = this.mousePosition.x - cardWidth - offsetX;
      }
      
      // Check if card would overflow bottom edge
      if (top + cardHeight > viewportHeight) {
        top = this.mousePosition.y - cardHeight - offsetY;
      }
      
      // Ensure card doesn't go off the left edge
      if (left < 0) {
        left = 10;
      }
      
      // Ensure card doesn't go off the top edge
      if (top < 0) {
        top = 10;
      }
      
      return {
        left: `${left}px`,
        top: `${top}px`
      };
    }
  },
  methods: {
    handleMouseEnter(airport, event) {
      this.hoveredAirport = airport;
      this.mousePosition = {
        x: event.clientX,
        y: event.clientY
      };
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

.controls-container {
  background: rgba(255, 255, 255, 0.95);
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
}

.search-section {
  flex: 1;
  min-width: 0;
}

.search-input {
  width: 100%;
  padding: 0.8rem;
  font-size: 1rem;
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

.view-toggle-container {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.view-toggle-btn {
  background-color: #e9ecef;
  color: #333;
  padding: 0.8rem 1.5rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
}

.view-toggle-btn:hover {
  background-color: #dee2e6;
  border-color: #ced4da;
}

.view-toggle-btn.active {
  background-color: #667eea;
  color: white;
  border-color: #667eea;
}

.view-toggle-btn.active:hover {
  background-color: #5a67d8;
  border-color: #5a67d8;
}

.toggle-icon {
  font-size: 1.2rem;
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

.airport-ssid {
  color: #2c3e50;
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  background: #e8f4fd;
  padding: 0.5rem;
  border-radius: 5px;
  border-left: 3px solid #667eea;
}

.airport-state {
  color: #666;
  font-size: 0.9rem;
  font-style: italic;
}

.table-container {
  background: rgba(255, 255, 255, 0.95);
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  overflow-x: auto; /* Ensure table is scrollable if content is wide */
  position: relative; /* For hover card positioning */
}

.airport-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
  color: #333;
}

.airport-table th,
.airport-table td {
  padding: 0.8rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
}

.airport-table th {
  background-color: #f8f9fa;
  color: #495057;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
}

.airport-table tbody tr:hover {
  background-color: #f1f3f5;
}

.airport-name-cell {
  font-weight: 600;
  color: #2c3e50;
}

.code-cell {
  font-family: 'Courier New', monospace;
  background: #f8f9fa;
  padding: 0.3rem 0.7rem;
  border-radius: 5px;
  border: 1px solid #e9ecef;
  font-size: 0.9rem;
  color: #333;
}

.ssid-cell {
  font-family: 'Courier New', monospace;
  background: #e8f4fd;
  padding: 0.3rem 0.7rem;
  border-radius: 5px;
  border: 1px solid #b3d9ff;
  font-size: 0.9rem;
  color: #2c3e50;
  font-weight: 500;
}

.enplanements-cell {
  font-weight: 600;
  color: #2c3e50;
}

/* Hover Card Styles */
.hover-card {
  position: fixed;
  background: rgba(255, 255, 255, 0.98);
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border: 1px solid #e9ecef;
  z-index: 1000;
  max-width: 300px;
  pointer-events: none;
  animation: fadeIn 0.2s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hover-card-title {
  color: #2c3e50;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.hover-card-location {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.hover-card-codes {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  margin-bottom: 0.5rem;
}

.hover-code-item {
  background: #f8f9fa;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  border: 1px solid #e9ecef;
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  color: #333;
}

.hover-card-ssid {
  color: #2c3e50;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  background: #e8f4fd;
  padding: 0.3rem 0.5rem;
  border-radius: 4px;
  border-left: 2px solid #667eea;
  font-family: 'Courier New', monospace;
}

.hover-card-role,
.hover-card-enplanements,
.hover-card-state {
  color: #666;
  font-size: 0.8rem;
  font-style: italic;
  margin-bottom: 0.3rem;
}

.hover-card-enplanements {
  font-weight: 600;
  color: #2c3e50;
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
  
  .controls-container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .search-input {
    font-size: 1rem;
    padding: 0.8rem;
  }

  .view-toggle-container {
    flex-direction: row;
    gap: 0.5rem;
    justify-content: center;
  }

  .view-toggle-btn {
    flex: 1;
    justify-content: center;
  }
}
</style>
