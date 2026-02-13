window.$docsify.plugins = [].concat(function (hook) {
  hook.doneEach(() => {

    const appName = document.querySelector('.app-name');
    const textLink = document.querySelector('.app-name-link');

    if (!appName || !textLink) return;

    /* =====================================
       1. Bild-Link erzeugen (unabhängig)
       ===================================== */
    if (!appName.querySelector('.app-img-link')) {

      const imgLink = document.createElement('a');
      imgLink.className = 'app-img-link';
      imgLink.href = '#/1refernz';
      imgLink.innerHTML = `<div><img src="/medien/KONRAD.JPG" alt="Referenz"></div>`;

      appName.insertBefore(imgLink, textLink);
    }

    /* ======================================
       2. Search-CTA direkt unter dem <h1>
       ====================================== */
    if (!document.querySelector('.sidebar-search-cta')) {
      const cta = document.createElement('div');
      cta.className = 'sidebar-search-cta';
      cta.tabIndex = 0;
      cta.innerHTML = `<span class="search-label">Suchen</span>`;
      cta.onclick = openSearch;

      appName.insertAdjacentElement('afterend', cta);
    }

  });
}, window.$docsify.plugins);


let activeIndex = -1;
const input = document.getElementById('search-input');
const resultsEl = document.getElementById('search-results');

input.addEventListener('input', () => {
  const q = input.value.trim();
  resultsEl.innerHTML = '';
  activeIndex = -1;

  if (!fuse || q.length < 3) return;

  const results = fuse.search(q, { limit: 30 });

  results.forEach((r, index) => {
    const { title = 'Ohne Titel', path = '#', content = '' } = r.item;

    const li = document.createElement('li');
    li.className = 'search-result';

    li.innerHTML = `
      <a href="#/${path}" onclick="closeSearch()">
        <span class="search-title">${title}</span>
        ${
          content
            ? `<span class="search-snippet">${content.slice(0, 140)}…</span>`
            : ''
        }
      </a>
    `;

    /* Hover → active */
    li.addEventListener('mouseenter', () => {
      activeIndex = index;
      updateActive();
    });

    resultsEl.appendChild(li);
  })

  if (results.length > 0) {
    activeIndex = 0;
    updateActive();
  }
});

document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    openSearch();
  }
  if (e.key === 'Escape') closeSearch();
});

input.addEventListener('keydown', e => {
  const items = resultsEl.querySelectorAll('.search-result');
  if (!items.length) return;

  if (e.key === 'ArrowDown') {
    e.preventDefault();
    activeIndex = (activeIndex + 1) % items.length;
    updateActive();
  }

  if (e.key === 'ArrowUp') {
    e.preventDefault();
    activeIndex = (activeIndex - 1 + items.length) % items.length;
    updateActive();
  }

  if (e.key === 'Enter' && activeIndex >= 0) {
    e.preventDefault();
    items[activeIndex].querySelector('a').click();
  }
});

/* =====================================
   Helper Functions
   ===================================== */

function updateActive() {
  const items = resultsEl.querySelectorAll('.search-result');

  items.forEach(el => el.classList.remove('active'));

  const active = items[activeIndex];
  if (!active) return;

  active.classList.add('active');
  active.scrollIntoView({ block: 'nearest' });
}

function openSearch() {
  const overlay = document.getElementById('search-overlay');
  overlay.style.display = 'block';
  input.focus();
}

function closeSearch() {
  document.getElementById('search-overlay').style.display = 'none';
  resultsEl.innerHTML = '';
  input.value = '';
  activeIndex = -1;
}

/* Klick außerhalb schließt */
document.getElementById('search-overlay')?.addEventListener('click', e => {
  if (e.target.id === 'search-overlay') closeSearch();
});