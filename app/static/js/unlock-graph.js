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
  
        Plotly.newPlot('myDiv', [{
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
        const unlockedCount = document.getElementById("unlockedCount");
        if (unlockedCount) unlockedCount.textContent = unlocked_colors.length;
  
        // Fill accuracy table
        const tableBody = document.getElementById("accuracyTableBody");
        if (tableBody) {
          tableBody.innerHTML = "";
          accuracy_table.forEach(row => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
              <td>${row.color}</td>
              <td>${(row.accuracy * 100).toFixed(2)}%</td>
            `;
            tableBody.appendChild(tr);
          });
        }
      })
      .catch(err => console.error("Failed to fetch stats:", err));
  });
  