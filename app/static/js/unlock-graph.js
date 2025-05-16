let incorrectData = [];

function setupSwatches() {
    const swatchGrid = document.getElementById("swatch-grid");
    const contentWrapper = document.querySelector("#gradient .content-wrapper");
    const instructions = document.getElementById("instructions");
    const gradientContainer = document.querySelector(".gradient-container");
    const distanceVal = document.getElementById("distance-val");

    swatchGrid.innerHTML = ""; // Clear any existing content

    incorrectData.forEach((item, index) => {
      const { correct, selected, distance } = item;

      // Create swatch element
      const swatch = document.createElement("div");
      swatch.className = "swatch";
      swatch.style.backgroundColor = `rgb(${selected.r}, ${selected.g}, ${selected.b})`;
      swatch.title = `Click to compare`;

      // Add click handler
      swatch.addEventListener("click", () => {
        if (contentWrapper) contentWrapper.classList.remove("hidden");


        // Update gradient display
        const correctColor = `rgb(${correct.r}, ${correct.g}, ${correct.b})`;
      const selectedColor = `rgb(${selected.r}, ${selected.g}, ${selected.b})`;

      gradientContainer.style.background = `linear-gradient(90deg, ${correctColor} 0%, ${selectedColor} 100%)`;


        // Update distance
      distanceVal.textContent = (typeof distance === "number") ? distance.toFixed(2) : "N/A";
      });

      swatchGrid.appendChild(swatch);
    });
  }

document.addEventListener("DOMContentLoaded", function () {
  // Fetch data for the graph
  fetchUnlockedData().then(data => {
    const { unlocked_colors, accuracy_table } = data;
    plotGraph(unlocked_colors);
    updateUnlockedCount(unlocked_colors.length);
  }).catch(err => console.error("Failed to fetch unlocked:", err));

  fetch("/api/incorrect")
    .then(res => res.json())
    .then(data => {
      incorrectData = data.tricky_colors;
      setupSwatches(); // Call only after data is ready
    })
    .catch(err => console.error("Error fetching incorrect colours:", err));



  
});

// Function to fetch unlocked color data
function fetchUnlockedData() {
  return fetch("/api/unlocked")
    .then(response => response.json());
}

// Function to plot the graph using Plotly
function plotGraph(unlocked_colors) {
  const x = [], y = [], z = [], colors = [];
  unlocked_colors.forEach(color => {
    const { r, g, b } = color;
    x.push(r);
    y.push(g);
    z.push(b);
    colors.push(`rgb(${r},${g},${b})`);
  });

  Plotly.newPlot('color-graph', [{
    x, y, z,
    mode: 'markers',
    type: 'scatter3d',
    marker: {
      size: 5,
      color: colors,
      opacity: 0.9
    }
  }], {
    title: 'Unlocked Colours in RGB Space',
    scene: {
      xaxis: { title: 'Red', range: [0, 255] },
      yaxis: { title: 'Green', range: [0, 255] },
      zaxis: { title: 'Blue', range: [0, 255] }
    }
  });
}

// Function to update the unlocked count
function updateUnlockedCount(count) {
  const unlockedCount = document.getElementById("unlocked-count");
  if (unlockedCount) unlockedCount.textContent = count;
}


