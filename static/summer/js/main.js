

/*=============== SHOW MENU ===============*/
const navMenu = document.getElementById('nav-menu'),
    navToggle = document.getElementById('nav-toggle'),
    navClose = document.getElementById('nav-close')

/* Menu show */
if (navToggle) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.add('show-menu')
    })
}

/* Menu hidden */
if (navClose) {
    navClose.addEventListener('click', () => {
        navMenu.classList.remove('show-menu')
    })
}

/*=============== REMOVE MENU MOBILE ===============*/
const navLink = document.querySelectorAll('.nav__link')

const linkAction = () => {
    const navMenu = document.getElementById('nav-menu')
    navMenu.classList.remove('show-menu')
}
navLink.forEach(n => n.addEventListener('click', linkAction))

/*=============== GSAP ENTRANCE ANIMATIONS ===============*/
gsap.from('.home__waterback', { duration: 3.7, opacity: 0, delay: 2, y: 200, x: 200 })
gsap.from('.home__watertop', { duration: 3.7, opacity: 0, delay: .1, y: 200, x: 200 })
gsap.from('.home__glasses', { duration: 3.5, opacity: 0, delay: 3, y: 200, x: 200 })
gsap.from('.home__lemonade', { duration: 1.2, opacity: 0, delay: 6, y: 200, x: 200 })
gsap.from('.home__flamingo', { duration: 2.4, opacity: 0, delay: 5, y: 200, x: 200 })
gsap.from('.home__stars', { duration: 1.2, opacity: 0, delay: 7 })
gsap.from('.home__title', { duration: 1.4, opacity: 0, delay: 7, y: 200, ease: "back.out(1.2)" })
gsap.from('.home__topflamingo', { duration: 1, opacity: 0, delay: 8.3, y: -10, x: -200 })
gsap.from('.home__water', { duration: 3.7, opacity: 0, delay: 4., y: -200, x: -200 })

/*=============== WATER SPLASH ON FLAMINGO CLICK ===============*/
const splashContainer = document.createElement('div');
splashContainer.style.cssText = `
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  pointer-events: none;
  z-index: 9999;
  overflow: hidden;
`;
document.body.appendChild(splashContainer);

function createSplash(originX, originY) {
    const dropCount = 28;
    const drops = [];

    for (let i = 0; i < dropCount; i++) {
        const drop = document.createElement('div');
        drop.classList.add('water-drop');

        // Random size: mix of small droplets and bigger splashes
        const size = Math.random() < 0.3
            ? gsap.utils.random(10, 20, 1)   // big drops
            : gsap.utils.random(3, 9, 1);    // small droplets

        // Slight horizontal elongation for "drop" look
        const w = size;
        const h = size * gsap.utils.random(1.1, 1.8);

        drop.style.cssText = `
      width: ${w}px;
      height: ${h}px;
      left: ${originX}px;
      top: ${originY}px;
      transform: translate(-50%, -50%);
    `;

        splashContainer.appendChild(drop);
        drops.push({ el: drop, size });
    }

    const tl = gsap.timeline({
        onComplete: () => drops.forEach(d => d.el.remove())
    });

    drops.forEach(({ el, size }, i) => {
        const angle = (Math.random() * 360); // full circle
        const rad = (angle * Math.PI) / 180;
        const dist = gsap.utils.random(60, 220);

        // Parabolic arc: shoot up & out, then fall with gravity
        const vx = Math.cos(rad) * dist;
        const vy = Math.sin(rad) * dist - gsap.utils.random(80, 160); // upward bias

        tl.to(el, {
            x: vx,
            y: vy + gsap.utils.random(100, 200), // gravity pull
            scaleX: 0.4,
            scaleY: 0.4,
            opacity: 0,
            duration: gsap.utils.random(0.55, 1.1),
            ease: 'power2.out',
        }, 0)
            .to(el, {
                opacity: 0,
                duration: 0.25,
                ease: 'power1.in',
            }, gsap.utils.random(0.4, 0.75));
    });

    // Central burst ring
    const ring = document.createElement('div');
    ring.classList.add('water-ring');
    ring.style.cssText = `
    left: ${originX}px;
    top: ${originY}px;
    transform: translate(-50%, -50%) scale(0);
  `;
    splashContainer.appendChild(ring);

    tl.to(ring, {
        scale: 2.5,
        opacity: 0,
        duration: 0.6,
        ease: 'power1.out',
        onComplete: () => ring.remove()
    }, 0);
}

// Attach click handler to topflamingo
const topFlamingo = document.querySelector('.home__topflamingo');
if (topFlamingo) {
    topFlamingo.addEventListener('click', (e) => {
        const rect = topFlamingo.getBoundingClientRect();
        // Origin at center of the flamingo image
        const cx = e.clientX;
        const cy = e.clientY;
        createSplash(cx, cy);
    });

    // Subtle hover wiggle to hint it's clickable
    topFlamingo.style.cursor = 'pointer';
    /*topFlamingo.addEventListener('mouseenter', () => {
      gsap.to(topFlamingo, { rotate: 4, duration: 0.25, ease: 'power1.out' });
    });
    topFlamingo.addEventListener('mouseleave', () => {
      gsap.to(topFlamingo, { rotate: 0, duration: 0.35, ease: 'elastic.out(1, 0.5)' });
    });*/
}

