function drawSpeedometer(score) {
    const canvas = document.getElementById("speedometer");
    if (!canvas) return;
  
    const ctx = canvas.getContext("2d");
    const width = 300;
    const height = 200;
    canvas.width = width;
    canvas.height = height;
  
    // Clear the canvas
    ctx.clearRect(0, 0, width, height);
  
    // Draw the background arc (gray)
    ctx.beginPath();
    ctx.arc(width / 2, height, 100, Math.PI, 0, false);
    ctx.lineWidth = 10;
    ctx.strokeStyle = "#ccc";
    ctx.stroke();
  
    // Map score (0-100) to an angle (π to 0)
    const angle = Math.PI + (score / 100) * Math.PI;
  
    // Draw the needle
    ctx.beginPath();
    ctx.moveTo(width / 2, height);
    ctx.lineTo(
      width / 2 + 90 * Math.cos(angle),
      height + 90 * Math.sin(angle)
    );
    ctx.lineWidth = 6;
    ctx.strokeStyle = score > 50 ? "#ff686b" : "#00c853"; // red or green
    ctx.stroke();
  
    // Display the numeric score
    ctx.font = "18px 'Poppins', sans-serif";
    ctx.fillStyle = "#333";
    ctx.fillText(`Fake Score: ${score.toFixed(0)}%`, 90, 190);
  }
  
  // Simple animation from `start` to `end` over `duration` ms
  function animateSpeedometer(start, end, duration) {
    let startTime;
  
    function animate(currentTime) {
      if (!startTime) startTime = currentTime;
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const currentScore = start + (end - start) * progress;
  
      drawSpeedometer(currentScore);
  
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    }
  
    requestAnimationFrame(animate);
  }
  
  document.addEventListener("DOMContentLoaded", function () {
    const scoreElement = document.getElementById("score-value");
    if (!scoreElement) return;
  
    const finalScore = parseFloat(scoreElement.textContent);
  
    // Animate from 0 to finalScore in 1.5 seconds
    animateSpeedometer(0, finalScore, 1500);
  
    setTimeout(() => {
      const loadingOverlay = document.getElementById("loading-overlay");
      if (loadingOverlay) {
        loadingOverlay.style.opacity = "0";
        setTimeout(() => {
          loadingOverlay.style.display = "none";
        }, 300);
      }
    }, 1000);
  });
  