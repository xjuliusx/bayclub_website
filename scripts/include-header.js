(function () {
  const headerMarkup = `<header class="site-header">
  <div class="nav-inner">
    <a href="/" class="brand">
      <img src="/images/bay_club_logo.svg" alt="The Bay Club Bayside New York" class="brand-logo" />
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav class="nav-main">
      <a href="/#overview" data-nav-key="overview">Life at The Bay Club</a>
      <a href="/residences/" data-nav-key="residences">Residences</a>
      <a href="/amenities/" data-nav-key="amenities">Leisure Club</a>
      <a href="/neighborhood/" data-nav-key="neighborhood">Neighborhood</a>
      <a href="/events/" data-nav-key="events">Events</a>
      <a href="/residents-area/" data-nav-key="residents_area">Residents Area</a>
      <a href="/contact/" data-nav-key="contacts">Contacts</a>
    </nav>
  </div>
</header>`;

  function activeNavKey(pathname, hash) {
    if (pathname === '/' || pathname === '/index.html') {
      return hash === '#overview' ? 'overview' : 'overview';
    }
    if (pathname.startsWith('/residences')) return 'residences';
    if (pathname.startsWith('/amenities')) return 'amenities';
    if (pathname.startsWith('/neighborhood')) return 'neighborhood';
    if (pathname.startsWith('/events') || pathname.startsWith('/community')) return 'events';
    if (pathname.startsWith('/residents-area') || pathname.startsWith('/residents_area')) return 'residents_area';
    if (pathname.startsWith('/contact') || pathname.startsWith('/contacts')) return 'contacts';

    return '';
  }

  async function injectHeader() {
    const mount = document.querySelector('[data-include="site-header"]');
    if (!mount) return;

    try {
      const res = await fetch('/partials/header.html', { cache: 'no-cache' });
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
