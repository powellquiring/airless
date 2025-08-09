// Airport data structure for US airports with FAA, IATA, and ICAO codes
// NOTE: This data comes from a comprehensive list of US airports

/**
 * Simple validation to ensure each airport has all required fields
 * @param {any[]} airports - Array of airport objects
 * @returns {any[]} - Validated array
 */
function validateAirports(airports) {
  if (!Array.isArray(airports)) {
    throw new Error('Airports data must be an array');
  }
  
  return airports.filter(airport => {
    const isValid = airport && 
                   typeof airport.City === 'string' &&
                   typeof airport.FAA === 'string' &&
                   typeof airport.IATA === 'string' &&
                   typeof airport.ICAO === 'string' &&
                   typeof airport.Airport === 'string' &&
                   typeof airport.Role === 'string' &&
                   typeof airport.Enplanements === 'string' &&
                   typeof airport.State === 'string' &&
                   typeof airport.StateAbbreviation === 'string';
    
    if (!isValid) {
      console.warn('Invalid airport found:', airport);
    }
    
    return isValid;
  }).map(airport => {
    return { ...airport, valid: 0 }; // Use spread syntax to create a new object and add the new field
});

}

// Function to fetch airport data from the JSON file
export async function fetchAirportData() {
  try {
    const response = await fetch('./airports.json');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    
    // Validate the data structure
    const validatedData = validateAirports(data);

    let retMap = new Map()
    validatedData.forEach(airport => {
      retMap.set(airport.IATA, airport)
    })

    const ssid_response = await fetch('./ssid.json');
    if (!ssid_response.ok) {
      throw new Error(`HTTP error! status: ${ssid_response.status}`);
    }
    const ssid_data = await ssid_response.json();


    ssid_data.forEach(ssid => {
      retMap.get(ssid.IATA).SSID = ssid.SSID
      retMap.get(ssid.IATA).valid = 1
    })
    
    return validatedData;
    
  } catch (error) {
    console.error('Error fetching airport data:', error);
    // Return fallback data if fetch fails
    return [
      { 
        City: "Portland",
        FAA: "PDX",
        IATA: "PDX", 
        ICAO: "KPDX",
        Airport: "Portland International Airport",
        Role: "P-S",
        Enplanements: "1,000,000",
        State: "OREGON",
        StateAbbreviation: "OR"
      }
    ];
  }
}

// Legacy export for backward compatibility (returns empty array initially)
export const airportData = []; 