<template>
  <div :class="cardClass">
    <h3 :class="titleClass">{{ airport.Airport }}</h3>
    <p :class="ssidClass"><strong>SSID:</strong> {{ airport.SSID }}</p>
    <p :class="locationClass">{{ airport.City }}, {{ airport.StateAbbreviation }}</p>
    <div :class="codesClass">
      <span :class="codeItemClass">FAA: {{ airport.FAA }}</span>
      <span :class="codeItemClass">IATA: {{ airport.IATA }}</span>
      <span :class="codeItemClass">ICAO: {{ airport.ICAO }}</span>
    </div>
    <p :class="roleClass">Role: {{ airport.Role }}</p>
    <p :class="enplanementsClass">Enplanements: {{ airport.Enplanements }}</p>
    <p :class="stateClass">State: {{ airport.State }}</p>
  </div>
</template>

<script>
export default {
  name: 'AirportCard',
  props: {
    airport: {
      type: Object,
      required: true
    },
    variant: {
      type: String,
      default: 'card', // 'card' or 'hover'
      validator: value => ['card', 'hover'].includes(value)
    }
  },
  computed: {
    cardClass() {
      return this.variant === 'hover' ? 'hover-card-content' : 'airport-card-content'
    },
    titleClass() {
      return this.variant === 'hover' ? 'hover-card-title' : 'airport-name'
    },
    ssidClass() {
      return this.variant === 'hover' ? 'hover-card-ssid' : 'airport-ssid'
    },
    locationClass() {
      return this.variant === 'hover' ? 'hover-card-location' : 'airport-location'
    },
    codesClass() {
      return this.variant === 'hover' ? 'hover-card-codes' : 'airport-codes'
    },
    codeItemClass() {
      return this.variant === 'hover' ? 'hover-code-item' : 'code-item'
    },
    roleClass() {
      return this.variant === 'hover' ? 'hover-card-role' : 'airport-role'
    },
    enplanementsClass() {
      return this.variant === 'hover' ? 'hover-card-enplanements' : 'airport-enplanements'
    },
    stateClass() {
      return this.variant === 'hover' ? 'hover-card-state' : 'airport-state'
    }
  }
}
</script>