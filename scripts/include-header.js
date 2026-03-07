(function () {
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
    if (hash === '#overview') return 'overview';

    return '';
  }

  async function injectHeader() {
    const mount = document.querySelector('[data-include="site-header"]');
    if (!mount) return;

    try {
      const res = await fetch('partials/header.html', { cache: 'no-cache' });
      if (!res.ok) return;

      mount.outerHTML = await res.text();
      const key = activeNavKey(window.location.pathname, window.location.hash);
      if (!key) return;

      const activeLink = document.querySelector(`.nav-main a[data-nav-key="${key}"]`);
      if (activeLink) {
        activeLink.classList.add('is-active');
      }
    } catch (_err) {
      // Keep page functional if the shared header cannot be fetched.
    }
  }

  injectHeader();
})();
