export function getSSIDStyle(airport) {
  if (airport.valid === 1) {
    return {
      backgroundColor: '#d4edda',
      color: '#155724',
      borderLeftColor: '#28a745',
      borderColor: '#c3e6cb'
    }
  } else if (airport.valid === 0) {
    return {
      backgroundColor: '#fff3cd',
      color: '#856404',
      borderLeftColor: '#ffc107',
      borderColor: '#ffeaa7'
    }
  } else {
    return {
      backgroundColor: '#f8d7da',
      color: '#721c24',
      borderLeftColor: '#dc3545',
      borderColor: '#f5c6cb'
    }
  }
}