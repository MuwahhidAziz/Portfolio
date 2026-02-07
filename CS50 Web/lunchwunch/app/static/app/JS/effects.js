// Js file for various efects

// Adding automatic hover effects for background color

document.querySelectorAll("[class*='bg-']").forEach(el => {
  let bgClass = [...el.classList].find(c => c.startsWith("bg-") && /\d+$/.test(c));
  if (!bgClass) return;

  // Example: bg-blue-700 → ["bg", "blue", "700"]
  let parts = bgClass.split("-");
  let color = parts[1];
  let shade = parseInt(parts[2]);

  if (isNaN(shade)) return; // extra safety: skip if no valid number

  // Calculate new shade
  let newShade;
  if (shade > 500) {
    newShade = shade - 200;
  } else {
    newShade = shade + 200;
  }

  newShade = Math.min(950, Math.max(50, newShade));

  // Build hover class
  let hoverClass = `hover:bg-${color}-${newShade}`;

  // Add it to element
  el.classList.add(hoverClass);
});

// Adding margins around hr elements
document.querySelectorAll('hr').forEach(el => {
  el.classList.add('mx-4');
});