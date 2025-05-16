document.addEventListener("DOMContentLoaded", function () {
  // Fetch data for the graph
  fetch("/api/unlocked")
    .then(response => response.json())
    .then(data => {
      const { unlocked_colors, accuracy_table } = data;

      // Graph
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

      // Display total colors unlocked
      const unlockedCount = document.getElementById("unlocked-count");
      if (unlockedCount) unlockedCount.textContent = unlocked_colors.length;
    })
    .catch(err => console.error("Failed to fetch unlocked:", err));

  // New functionality: Handle swatch clicks
  const swatches = document.querySelectorAll(".swatch");
  const contentWrapper = document.querySelector(".content-wrapper");
  const instructions = document.getElementById("instructions");

  swatches.forEach(swatch => {
      swatch.addEventListener("click", function () {
          const colour = swatch.getAttribute("data-colour");

          // Check if the clicked swatch has data-color="4"
          if (colour === "4") {
              // Show the content-wrapper and hide the instructions
              if (contentWrapper) contentWrapper.classList.remove("hidden");
              if (instructions) instructions.style.display = "none";
          }
      });
  });
});


fetch("/api/incorrect")
  .then(response => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then(data => {
    const trickyColors = data.tricky_colors;

    trickyColors.forEach(entry => {
      const { correct, selected, distance } = entry;

      console.log("Correct colour:", correct);
      console.log("User selected:", selected);
      console.log("Distance:", distance.toFixed(2));
      
      // Example: do something with each pair
      // You can add them to the DOM, generate swatches, etc.
    });
  })
  .catch(error => {
    console.error("Error fetching /api/incorrect:", error);
  });

