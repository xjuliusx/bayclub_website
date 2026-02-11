(function () {
  function buildEventPath(href) {
    if (!href) return null;
    var raw = href.trim();
    if (!raw || raw === '#') return 'click-#';
    var lower = raw.toLowerCase();
    if (lower.startsWith('mailto:')) {
      return 'click-mailto-' + raw.slice(7).replace(/[^a-z0-9@._-]+/gi, '_');
    }
    if (lower.startsWith('tel:')) {
      return 'click-tel-' + raw.slice(4).replace(/[^a-z0-9+._-]+/gi, '_');
    }
    if (lower.startsWith('javascript:')) {
      return 'click-js';
    }
    try {
      var url = new URL(raw, window.location.href);
      var path = 'click-' + url.hostname + url.pathname;
      if (url.search) path += url.search;
      if (url.hash) path += url.hash;
      return path;
    } catch (e) {
      return 'click-' + raw.replace(/[^a-z0-9+._-]+/gi, '_');
    }
  }

  function handleClick(event) {
    var el = event.target;
    if (!el) return;
    if (el.closest) {
      el = el.closest('a');
    } else {
      while (el && el.tagName !== 'A') el = el.parentNode;
    }
    if (!el || !el.getAttribute) return;
    var href = el.getAttribute('href');
    if (!href) return;
    if (!window.goatcounter || typeof window.goatcounter.count !== 'function') return;

    var path = buildEventPath(href);
    if (!path) return;

    window.goatcounter.count({
      path: path,
      title: el.getAttribute('data-goatcounter-title') || el.title || (el.textContent || '').trim().slice(0, 200),
      event: true
    });
  }

  document.addEventListener('click', handleClick, true);
})();
