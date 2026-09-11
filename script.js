const stage = document.getElementById('stage');
const envelope = document.getElementById('envelope');
const replay = document.getElementById('replay');
const sectionNav = document.getElementById('section-nav');

// koniec sekwencji = --card-in + --card-dur ze style.css
const OPEN_MS = 5800;
const FADE_MS = 450;
let navTimer;

const slow = !matchMedia('(prefers-reduced-motion: reduce)').matches;

envelope.addEventListener('click', () => {
  if (stage.classList.contains('is-open')) return;
  stage.classList.add('is-open');
  envelope.disabled = true;
  navTimer = setTimeout(() => { sectionNav.hidden = false; }, slow ? OPEN_MS : 0);
  setTimeout(() => { replay.hidden = false; }, slow ? OPEN_MS - 400 : 0);
});

replay.addEventListener('click', () => {
  clearTimeout(navTimer);
  stage.classList.add('is-resetting');
  setTimeout(() => {
    stage.classList.remove('is-open');
    sectionNav.hidden = true;
    replay.hidden = true;
    envelope.disabled = false;
    stage.offsetWidth; // reflow, zeby animacje wystartowaly od zera
    stage.classList.remove('is-resetting');
  }, slow ? FADE_MS : 0);
});
