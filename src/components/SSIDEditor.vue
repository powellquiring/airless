<template>
  <div class="ssid-editor">
    <div class="editor-header">
      <h2>SSID Editor</h2>
      <p>Edit the public/ssid.json file entries</p>
    </div>

    <div v-if="loading" class="loading">
      <p>Loading SSID data...</p>
    </div>

    <div v-else class="editor-content">
      <!-- Add New Entry Form -->
      <div class="add-form">
        <h3>Add New SSID Entry</h3>
        <div class="form-row">
          <input
            v-model="newEntry.IATA"
            type="text"
            placeholder="IATA Code (e.g., MSP)"
            class="form-input"
          />
          <input
            v-model="newEntry.SSID"
            type="text"
            placeholder="SSID (e.g., MSP Airport WiFi)"
            class="form-input"
          />
          <input
            v-model="newEntry.Comment"
            type="text"
            placeholder="Comment (optional)"
            class="form-input"
          />
          <button @click="addEntry" class="add-btn" :disabled="!canAdd">
            Add Entry
          </button>
        </div>
      </div>

      <!-- Existing Entries -->
      <div class="entries-list">
        <h3>Existing Entries ({{ ssidData.length }})</h3>
        <div v-if="ssidData.length === 0" class="no-entries">
          <p>No SSID entries found.</p>
        </div>
        <div v-else class="entries-grid">
          <div
            v-for="(entry, index) in ssidData"
            :key="index"
            class="entry-card"
          >
            <div class="entry-header">
              <span class="iata-code">{{ entry.IATA }}</span>
              <button @click="deleteEntry(index)" class="delete-btn">
                ✕
              </button>
            </div>
            <div class="entry-ssid">{{ entry.SSID }}</div>
            <div v-if="entry.Comment" class="entry-comment">
              {{ entry.Comment }}
            </div>
            <div v-if="entry.Date" class="entry-date">
              {{ entry.Date }}
            </div>
          </div>
        </div>
      </div>

      <!-- Save Button -->
      <div class="save-section">
        <button @click="copyToClipboard" class="copy-btn" :disabled="ssidData.length === 0">
          Copy JSON
        </button>
        <span v-if="copyStatus" class="copy-status" :class="copyStatus.type">
          {{ copyStatus.message }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SSIDEditor',
  data() {
    return {
      ssidData: [],
      originalData: [],
      loading: true,
      newEntry: {
        IATA: '',
        SSID: '',
        Comment: '',
        Date: ''
      },
      copyStatus: null
    }
  },
  computed: {
    canAdd() {
      return this.newEntry.IATA.trim() && this.newEntry.SSID.trim()
    }
  },
  methods: {
    async loadSSIDData() {
      try {
        const response = await fetch('./ssid.json')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        this.ssidData = [...data]
        this.originalData = [...data]
      } catch (error) {
        console.error('Error loading SSID data:', error)
        this.ssidData = []
        this.originalData = []
      } finally {
        this.loading = false
      }
    },
    addEntry() {
      if (!this.canAdd) return
      
      const entry = {
        IATA: this.newEntry.IATA.trim().toUpperCase(),
        SSID: this.newEntry.SSID.trim(),
        Comment: this.newEntry.Comment.trim(),
        Date: new Date().toISOString().split('T')[0]
      }
      
      this.ssidData.push(entry)
      this.resetForm()
    },
    deleteEntry(index) {
      if (confirm('Are you sure you want to delete this entry?')) {
        this.ssidData.splice(index, 1)
      }
    },
    resetForm() {
      this.newEntry = {
        IATA: '',
        SSID: '',
        Comment: '',
        Date: ''
      }
    },
    async copyToClipboard() {
      this.copyStatus = { type: 'info', message: 'Copying...' }
      
      try {
        const jsonString = JSON.stringify(this.ssidData, null, 2)
        await navigator.clipboard.writeText(jsonString)
        
        this.copyStatus = { type: 'success', message: 'JSON copied to clipboard!' }
        
        setTimeout(() => {
          this.copyStatus = null
        }, 3000)
      } catch (error) {
        console.error('Error copying to clipboard:', error)
        this.copyStatus = { type: 'error', message: 'Failed to copy to clipboard' }
        
        // Fallback: log to console for manual copy
        console.log('SSID JSON data:', JSON.stringify(this.ssidData, null, 2))
      }
    }
  },
  async mounted() {
    await this.loadSSIDData()
  }
}
</script>

<style scoped>
.ssid-editor {
  background: rgba(255, 255, 255, 0.95);
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.editor-header {
  text-align: center;
  margin-bottom: 2rem;
}

.editor-header h2 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.add-form {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.add-form h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.form-row {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.form-input {
  flex: 1;
  padding: 0.8rem;
  border: 2px solid #e9ecef;
  border-radius: 6px;
  font-size: 0.9rem;
}

.form-input:focus {
  border-color: #667eea;
  outline: none;
}

.add-btn {
  background: #28a745;
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.add-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.entries-list h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.entries-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.entry-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1rem;
}

.entry-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.iata-code {
  font-family: 'Courier New', monospace;
  font-weight: bold;
  color: #2c3e50;
  font-size: 1.1rem;
}

.delete-btn {
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  font-size: 0.8rem;
}

.entry-ssid {
  font-weight: 600;
  color: var(--ssid-text-color);
  margin-bottom: 0.5rem;
}

.entry-comment {
  font-style: italic;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.3rem;
}

.entry-date {
  font-size: 0.8rem;
  color: #999;
}

.save-section {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
}

.copy-btn {
  background: #17a2b8;
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
}

.copy-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.copy-status {
  margin-left: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 600;
}

.copy-status.success {
  background: #d4edda;
  color: #155724;
}

.copy-status.error {
  background: #f8d7da;
  color: #721c24;
}

.copy-status.info {
  background: #d1ecf1;
  color: #0c5460;
}

.no-entries {
  text-align: center;
  padding: 2rem;
  color: #666;
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
  }
  
  .entries-grid {
    grid-template-columns: 1fr;
  }
}
</style>
