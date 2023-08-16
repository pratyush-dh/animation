//Requires Google Earth Engine
//Run on Google Earth Engine

Map.setCenter(85.29, 27.74, 13);
//var mapLayers = Map.layers(); 
//Map.setOptions('satellite');
Map.style().set({cursor: 'crosshair'});


// Load CHIRPS precipitation dataset
var chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
              .select('precipitation');

// Define the date range
var startDate = ee.Date('2013-01-01');
var endDate = ee.Date('2023-12-31');

// Define the point of interest
//var point = ee.Geometry.Point([85.340243, 27.686168]);


Map.onClick(function(coords) {
  
  //widgetList.set(0, ui.Label(''));
  
  var point = ee.Geometry.Point([coords.lon, coords.lat]);
  
  console.log(point)
  
  // Filter CHIRPS data for the selected point and date range
  var filteredChirps = chirps.filterBounds(point).filterDate(startDate, endDate);
  
  // Generate a time series chart
  var chart = ui.Chart.image.seriesByRegion({
    imageCollection: filteredChirps,
    regions: point,
    reducer: ee.Reducer.mean(),
    scale: 1000,
    xProperty: 'system:time_start',
    seriesProperty: 'label'
  }).setChartType('LineChart')  // Set chart type to LineChart
    .setOptions({
      title: "CHIRPS Precipitation Time Series at ("  + (coords.lon).toFixed(3) + "E, " + (coords.lat).toFixed(3) + "N) ",
      vAxis: {title: 'Precipitation (mm)'},
      hAxis: {title: 'Date'}
    });
  
  // Print the chart to the console
  print(chart);
});
