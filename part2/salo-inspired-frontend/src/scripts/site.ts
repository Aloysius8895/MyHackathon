import Lenis from "lenis";

type LenisInstance = InstanceType<typeof Lenis>;

declare global {
  interface Window {
    __studioLenis?: LenisInstance;
  }
}

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function initLenis() {
  if (reduceMotion || window.__studioLenis) return;

  const lenis = new Lenis({
    lerp: 0.085,
    smoothWheel: true,
  });

  window.__studioLenis = lenis;

  function raf(time: number) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }

  requestAnimationFrame(raf);
}

function initHeader() {
  const header = document.querySelector<HTMLElement>("[data-site-header]");
  if (!header) return;

  let lastY = window.scrollY;

  const update = () => {
    const y = window.scrollY;
    const direction = y > lastY ? "down" : "up";
    header.dataset.sticky = y <= 12 ? "default" : direction === "down" ? "hidden" : "visible";
    lastY = y;
  };

  window.addEventListener("scroll", update, { passive: true });
  update();
}

function initMenu() {
  const toggle = document.querySelector<HTMLButtonElement>("[data-menu-toggle]");
  const close = document.querySelector<HTMLButtonElement>("[data-menu-close]");
  const menu = document.querySelector<HTMLElement>("[data-mobile-menu]");
  if (!toggle || !menu) return;

  const setOpen = (open: boolean) => {
    toggle.setAttribute("aria-expanded", String(open));
    menu.hidden = !open;
    document.body.dataset.menuOpen = open ? "true" : "false";
    if (open) window.__studioLenis?.stop();
    else window.__studioLenis?.start();
  };

  toggle.addEventListener("click", () => setOpen(toggle.getAttribute("aria-expanded") !== "true"));
  close?.addEventListener("click", () => setOpen(false));
  menu.addEventListener("click", (event) => {
    if (event.target === menu) setOpen(false);
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") setOpen(false);
  });
}

function initGlowButtons() {
  document.querySelectorAll<HTMLElement>(".js-glow").forEach((button) => {
    button.addEventListener("pointermove", (event) => {
      const rect = button.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width) * 100;
      const y = ((event.clientY - rect.top) / rect.height) * 100;
      button.style.setProperty("--glow-x", `${x}%`);
      button.style.setProperty("--glow-y", `${y}%`);
    });
  });
}

function initCarousel() {
  const carousel = document.querySelector<HTMLElement>("[data-carousel]");
  const prev = document.querySelector<HTMLButtonElement>("[data-carousel-prev]");
  const next = document.querySelector<HTMLButtonElement>("[data-carousel-next]");
  const progress = document.querySelector<HTMLElement>("[data-carousel-progress]");
  if (!carousel || !prev || !next || !progress) return;

  const getStep = () => {
    const first = carousel.querySelector<HTMLElement>(".project-slide");
    if (!first) return carousel.clientWidth;
    const gap = Number.parseFloat(getComputedStyle(carousel).columnGap || "0");
    return first.offsetWidth + gap;
  };

  const update = () => {
    const max = carousel.scrollWidth - carousel.clientWidth;
    const percentage = max <= 0 ? 100 : Math.min(100, Math.max(0, (carousel.scrollLeft / max) * 100));
    progress.style.width = `${percentage}%`;
    prev.disabled = carousel.scrollLeft <= 2;
    next.disabled = carousel.scrollLeft >= max - 2;
  };

  prev.addEventListener("click", () => {
    carousel.scrollBy({ left: -getStep(), behavior: reduceMotion ? "auto" : "smooth" });
  });
  next.addEventListener("click", () => {
    carousel.scrollBy({ left: getStep(), behavior: reduceMotion ? "auto" : "smooth" });
  });

  carousel.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
  update();
}

initLenis();
initHeader();
initMenu();
initGlowButtons();
initCarousel();
