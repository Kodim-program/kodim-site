gsap.registerPlugin(Draggable, InertiaPlugin, Physics2DPlugin);

// Elements & config
const emitter = document.getElementById("emitter");
// we'll put all the dots into this container so we can move the "explosion" anywhere
const container = document.createElement("div");

// Tweakables
const emitterSize = 100;
const dotQuantity = 25;
const dotSizeMax = 20;
const dotSizeMin = 10;
const speed = 3;
const gravity = 3;

// Setup the container
container.style.cssText = "position:absolute; left:0; top:0; overflow:visible; z-index:5000; pointer-events:none;";
document.body.appendChild(container);

// Build the explosion timeline once (reuse for performance)
const explosion = createExplosion(container);

function createExplosion(container) {
  const tl = gsap.timeline();
  for (let i = 0; i < dotQuantity; i++) {
    const dot = document.createElement("div");
    dot.className = "dot";
    const size = gsap.utils.random(dotSizeMin, dotSizeMax, 1);
    container.appendChild(dot);

    const angle = Math.random() * Math.PI * 2; // radians
    const length = Math.random() * (emitterSize / 2 - size / 2);

    // Place dot within emitter and size it
    gsap.set(dot, {
      x: Math.cos(angle) * length,
      y: Math.sin(angle) * length,
      width: size,
      height: size,
      xPercent: -50,
      yPercent: -50,
      force3D: true
    });

    // Animate via Physics2D (GSAP plugin)
    tl.to(
      dot,
      {
        physics2D: {
          angle: (angle * 180) / Math.PI,
          velocity: (100 + Math.random() * 250) * speed,
          gravity: 500 * gravity
        },
        duration: 1 + Math.random()
      },
      0
    ).to(
      dot,
      {
        opacity: 0,
        duration: 0.2,
        ease: "power2.inOut"
      },
      0.7
    );

    // If you'd rather not do physics, you can swap the physics2D block for:
    // { x: Math.cos(angle) * length * 6, y: Math.sin(angle) * length * 6, duration: 1 + Math.random() }
  }
  return tl;
}

// Move the container to the center of an element and play the explosion
function explode(element) {
  const bounds = element.getBoundingClientRect();
  gsap.set(container, { x: bounds.left + bounds.width / 2, y: bounds.top + bounds.height / 2 });
  explosion.play(0);
}

// Go boom on load and on click
explode(emitter);
emitter.addEventListener("click", () => explode(emitter));

// Make the emitter draggable (requires InertiaPlugin for inertia:true)
Draggable.create("#emitter", {
  inertia: true,
  bounds: window,
  edgeResistance: 0.7
});
