function createAberrationDiagram(containerId) {
  const container = document.getElementById(containerId);

  // Create diagram container
  const diagramContainer = document.createElement('div');
  diagramContainer.className = 'diagram-container';


  // Create and append canvas
  const canvas = document.createElement('canvas');
  canvas.style.width = "auto";
  canvas.style.height = "250px";
  canvas.style.margin = "auto";
  canvas.style.display = "grid";
  canvas.style.placeItems = "center";

  diagramContainer.appendChild(canvas);



  // Create slider container
  const sliderContainer = document.createElement('div');
  sliderContainer.className = 'slider-container';

  // Create label and value span
  const label = document.createElement('label');
  label.htmlFor = 'bSlider';
  label.textContent = "\\(u'\\) = ";
  const valueSpan = document.createElement('span');
  valueSpan.id = 'bValue';
  valueSpan.textContent = '0.000';
  label.appendChild(valueSpan);


  // Create slider
  const slider = document.createElement('input');
  slider.type = 'range';
  slider.id = 'bSlider';
  slider.min = '0.0001';
  slider.max = '0.9999999';
  slider.step = '0.0000001';
  slider.value = '0';
  slider.style.width = "100%";


  // Append elements to container
  sliderContainer.appendChild(label);
  sliderContainer.appendChild(document.createElement('br'));
  sliderContainer.appendChild(slider);
  diagramContainer.appendChild(sliderContainer);

  // Add the diagram container to the main container
  container.appendChild(diagramContainer);

  const ctx = canvas.getContext('2d');
  const bValueLabel = valueSpan;

  function updateCanvasSize() {
    const containerRect = container.getBoundingClientRect();
    const sliderHeight = sliderContainer.offsetHeight;

    // Calculate available space for canvas
    const availableHeight = containerRect.height - sliderHeight;
    const availableWidth = containerRect.width;

    // Use the smaller dimension to maintain square aspect ratio
    const size = Math.min(availableWidth, availableHeight);

    if (size > 0) {
      canvas.width = size;
      canvas.height = size;

      // Reset the transform and redraw
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.translate(canvas.width / 2, canvas.height / 2);
      ctx.scale(1, -1);
      draw();
    }
  }

  function drawArrow(ctx, x1, y1, x2, y2) {
    const headLen = canvas.width * 0.02; // Make arrow head size relative to canvas size
    const dx = x2 - x1;
    const dy = y2 - y1;
    const angle = Math.atan2(dy, dx);

    const x2_adj = x2 - headLen * Math.cos(angle);
    const y2_adj = y2 - headLen * Math.sin(angle);

    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2_adj, y2_adj);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x2 - headLen * Math.cos(angle - Math.PI / 6),
               y2 - headLen * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(x2 - headLen * Math.cos(angle + Math.PI / 6),
               y2 - headLen * Math.sin(angle + Math.PI / 6));
    ctx.lineTo(x2, y2);
    ctx.fill();
  }

  function draw() {
    ctx.save();
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.restore();

    const b = parseFloat(slider.value);
    bValueLabel.textContent = b.toFixed(3);
    const gamma = 1 / Math.sqrt(1 - b * b);

    const N = 50;
    const shift = Math.PI / N;
    const L = canvas.width * 0.5;

    for (let i = 0; i < N; i++) {
      const alpha = (2 * Math.PI * i) / N + shift;

      const denom = 1 + b * Math.cos(alpha);
      const n_x = Math.sin(alpha) / (gamma * denom);
      const n_y = (Math.cos(alpha) + b) / denom;

      let theta = Math.atan2(n_x, n_y);

      if (b >= 0.999) {
        theta = 0;
      }

      const x = L * Math.sin(theta);
      const y = L * Math.cos(theta);

      ctx.strokeStyle = "black";
      ctx.fillStyle = "black";
      ctx.lineWidth = Math.max(1, canvas.width * 0.007); // Make line width relative to canvas size
      drawArrow(ctx, 0, 0, x, y);
    }

    const L_red = L * b;
    ctx.strokeStyle = "red";
    ctx.fillStyle = "red";
    ctx.lineWidth = Math.max(2, canvas.width * 0.01); // Make line width relative to canvas size
    drawArrow(ctx, 0, 0, 0, L_red);
  }

  // Add resize observer to handle container size changes
  const resizeObserver = new ResizeObserver(() => {
    updateCanvasSize();
  });

  resizeObserver.observe(container);

  // Also handle window resize events
  window.addEventListener('resize', updateCanvasSize);

  slider.addEventListener('input', draw);

  // Initial size update and draw
  updateCanvasSize();
}