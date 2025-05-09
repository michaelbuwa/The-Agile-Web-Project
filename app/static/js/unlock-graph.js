document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/stats")
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
        .catch(err => console.error("Failed to fetch stats:", err));
      });
  