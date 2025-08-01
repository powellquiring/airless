# Airless - Airport Data Visualization

A Vue.js application for visualizing airport data from JSON files. The app displays airport information including names and SSIDs in a modern, responsive grid layout.

## Features

- Upload and parse JSON files containing airport data
- Visualize airports in a responsive card grid
- Sample data included for testing
- Modern, responsive design with hover effects
- File validation and error handling

## Data Format

The application expects JSON files with the following structure:

```json
[
  {
    "name": "Airport Name",
    "ssid": "Airport_SSID"
  }
]
```

A sample file (`airports.json`) is included in the `public` folder.

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

## Usage

1. Start the development server with `npm run serve`
2. Open the application in your browser
3. Either:
   - Click "Load Sample Data" to see example airports
   - Upload a JSON file using the file input
4. View the airport data in the responsive grid layout

## Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
