let incorrectData = [];

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
      incorrectData = data.tricky_colors; // Save it for use when swatches are clicked
    })
    .catch(err => console.error("Error fetching incorrect colours:", err));


  // Handle swatch clicks
  setupSwatches();
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

  Plotly.newPlot('colour-graph', [{
    x, y, z,
    mode: 'markers',
    type: 'scatter3d',
    marker: {
      size: 5,
      color: colors,
      opacity: 0.9
    }
  }], {
    title: 'Unlocked Colors in RGB Space',
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

// Function to handle swatch clicks
function setupSwatches() {
  const swatches = document.querySelectorAll(".swatch");
  const contentWrapper = document.querySelector(".content-wrapper");
  const instructions = document.getElementById("instructions");

  swatches.forEach(swatch => {
    swatch.addEventListener("click", function () {
      const colour = swatch.getAttribute("data-colour");

      if (colour === "4") {
        if (contentWrapper) contentWrapper.classList.remove("hidden");
        if (instructions) instructions.style.display = "none";
      }
    });
  });
}
