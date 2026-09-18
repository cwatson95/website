/* pdf_view.js — "View PDF" renders the document into the page.
 *
 * It draws with PDF.js onto <canvas> rather than pointing an <iframe> at the
 * file, because a browser set to "save PDFs" (Firefox: Applications -> PDF ->
 * Save File; Chrome: "Download PDFs instead of automatically opening them")
 * downloads an embedded PDF and leaves the frame blank. Canvas rendering does
 * not go through that handler, so the preview works whatever the setting.
 *
 * Progressive enhancement: the control is a plain link to the PDF, so with
 * JavaScript off it still opens in a new tab. Pages render lazily as they
 * scroll into view, and closing the viewer destroys the document, so nothing
 * is fetched or held for a paper nobody opened.
 */
(function () {
  'use strict';

  var VER = '3.11.174';
  var BASE = 'https://cdn.jsdelivr.net/npm/pdfjs-dist@' + VER + '/build/';
  var libPromise = null;

  function lib() {
    if (libPromise) return libPromise;
    libPromise = new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = BASE + 'pdf.min.js';
      s.onload = function () {
        if (!window.pdfjsLib) { reject(new Error('pdf.js did not initialise')); return; }
        window.pdfjsLib.GlobalWorkerOptions.workerSrc = BASE + 'pdf.worker.min.js';
        resolve(window.pdfjsLib);
      };
      s.onerror = function () { reject(new Error('could not load the PDF renderer')); };
      document.head.appendChild(s);
    });
    return libPromise;
  }

  function note(box, text, url) {
    box.textContent = '';
    var p = document.createElement('p');
    p.className = 'doc-status';
    p.textContent = text + ' ';
    if (url) {
      var a = document.createElement('a');
      a.href = url; a.target = '_blank'; a.rel = 'noopener';
      a.textContent = 'Open the PDF in a new tab';
      p.appendChild(a);
    }
    box.appendChild(p);
    return p;
  }

  function draw(pdf, slot) {
    if (slot.dataset.done) return;
    slot.dataset.done = '1';
    pdf.getPage(Number(slot.dataset.page)).then(function (page) {
      var css = page.getViewport({ scale: 1 });
      var wide = slot.clientWidth || 700;
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var vp = page.getViewport({ scale: (wide / css.width) * dpr });
      var c = document.createElement('canvas');
      c.width = Math.floor(vp.width);
      c.height = Math.floor(vp.height);
      slot.appendChild(c);
      page.render({ canvasContext: c.getContext('2d'), viewport: vp });
    }).catch(function () { slot.dataset.done = ''; });
  }

  function render(box, url) {
    note(box, 'Loading preview…');
    lib().then(function (L) {
      return L.getDocument({ url: url }).promise;
    }).then(function (pdf) {
      box.textContent = '';
      box._pdf = pdf;
      var pages = document.createElement('div');
      pages.className = 'pdf-pages';
      box.appendChild(pages);
      return pdf.getPage(1).then(function (p1) {
        var v = p1.getViewport({ scale: 1 });
        var io = ('IntersectionObserver' in window) ? new IntersectionObserver(function (entries) {
          entries.forEach(function (e) {
            if (!e.isIntersecting) return;
            io.unobserve(e.target);
            draw(pdf, e.target);
          });
        }, { root: pages, rootMargin: '600px 0px' }) : null;
        for (var i = 1; i <= pdf.numPages; i++) {
          var slot = document.createElement('div');
          slot.className = 'pdf-page';
          slot.dataset.page = i;
          slot.style.aspectRatio = v.width + ' / ' + v.height;
          pages.appendChild(slot);
          if (io) io.observe(slot); else draw(pdf, slot);
        }
      });
    }).catch(function (err) {
      note(box, 'Preview unavailable (' + (err && err.message ? err.message : err) + ').', url);
    });
  }

  function close(box) {
    if (box._pdf) { try { box._pdf.destroy(); } catch (e) {} box._pdf = null; }
    box.textContent = '';
    box.hidden = true;
  }

  document.addEventListener('click', function (e) {
    if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target && e.target.closest ? e.target.closest('a.js-view') : null;
    if (!a) return;
    var box = document.getElementById(a.getAttribute('data-target') || '');
    if (!box) return;                        // no slot: let the link do its job

    e.preventDefault();
    if (box.firstChild) {
      close(box);
      a.setAttribute('aria-expanded', 'false');
      a.textContent = a.getAttribute('data-label-show') || 'View PDF';
    } else {
      box.hidden = false;
      render(box, a.getAttribute('href'));
      a.setAttribute('aria-expanded', 'true');
      a.textContent = a.getAttribute('data-label-hide') || 'Hide preview';
      box.scrollIntoView({ block: 'nearest' });
    }
  });
})();
