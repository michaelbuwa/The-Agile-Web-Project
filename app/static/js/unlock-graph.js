document.addEventListener("DOMContentLoaded", function () {
    const step = 50;
    const x = [], y = [], z = [], colors = [];
    for (let r = 0; r <= 255; r += step) {
      for (let g = 0; g <= 255; g += step) {
        for (let b = 0; b <= 255; b += step) {
          x.push(r);
          y.push(g);
          z.push(b);
          colors.push(`rgb(${r},${g},${b})`);
        }
      }
    }
  
    const trace = {
      x: x, y: y, z: z,
      mode: 'markers',
      type: 'scatter3d',
      marker: {
        size: 5,
        color: colors,
        opacity: 0.9
      }
    };
  
    const layout = {
      title: 'RGB Color Cube',
      scene: {
        xaxis: { title: 'Red', range: [0, 255] },
        yaxis: { title: 'Green', range: [0, 255] },
        zaxis: { title: 'Blue', range: [0, 255] }
      }
    };
  
    Plotly.newPlot('myDiv', [trace], layout);
  });
  