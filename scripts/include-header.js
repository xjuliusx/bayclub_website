(function () {
  const headerMarkup = `<header class="site-header">
  <div class="nav-inner">
    <a href="index.html" class="brand">
      <div class="brand-mark"></div>
      <div class="brand-text">
        <span class="brand-main">The Bay Club</span>
        <span class="brand-sub">Bayside · New York</span>
      </div>
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav class="nav-main">
      <a href="index.html#overview" data-nav-key="overview">Life at The Bay Club</a>
      <a href="residences.html" data-nav-key="residences">Residences</a>
      <a href="amenities.html" data-nav-key="amenities">Leisure Club</a>
      <a href="neighborhood.html" data-nav-key="neighborhood">Neighborhood</a>
      <a href="events.html" data-nav-key="events">Events</a>
      <a href="residents_area.html" data-nav-key="residents_area">Residents Area</a>
      <a href="contacts.html" data-nav-key="contacts">Contacts</a>
    </nav>
  </div>
</header>`;

  function activeNavKey(pathname, hash) {
    const page = pathname.split('/').pop() || 'index.html';

    if (page === 'index.html' || page === 'index_temp.html' || page === 'index_construction.html' || page === 'indexconstruction2.html') {
      return 'overview';
    }
    if (page === 'residences.html') return 'residences';
    if (page === 'amenities.html') return 'amenities';
    if (page === 'neighborhood.html') return 'neighborhood';
    if (page === 'events.html' || page === 'community.html') return 'events';
    if (page === 'residents_area.html') return 'residents_area';
    if (page === 'contacts.html') return 'contacts';
    if (hash === '#overview') return 'overview';

    return '';
  }

  async function injectHeader() {
    const mount = document.querySelector('[data-include="site-header"]');
    if (!mount) return;

    try {
      const res = await fetch('partials/header.html', { cache: 'no-cache' });
      if (!res.ok) throw new Error('Header partial request failed');

      mount.outerHTML = await res.text();
    } catch (_err) {
      // Fallback keeps pages working when opened directly via file://.
      mount.outerHTML = headerMarkup;
    }

    const key = activeNavKey(window.location.pathname, window.location.hash);
    if (key) {
      const activeLink = document.querySelector(`.nav-main a[data-nav-key="${key}"]`);
      if (activeLink) activeLink.classList.add('is-active');
    }

    initMobileNav();
  }

  function initMobileNav() {
    const toggle = document.querySelector('.nav-toggle');
    const nav = document.querySelector('.nav-main');
    if (!toggle || !nav) return;

    function openMenu() {
      nav.classList.add('is-open');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Close menu');
    }

    function closeMenu() {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open menu');
    }

    toggle.addEventListener('click', () => {
      nav.classList.contains('is-open') ? closeMenu() : openMenu();
    });

    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', closeMenu);
    });

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') closeMenu();
    });

    document.addEventListener('click', e => {
      if (!e.target.closest('.site-header')) closeMenu();
    });
  }

  injectHeader();
})();
