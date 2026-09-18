/* pdf_view.js — "View PDF" opens an inline viewer in the page instead of
 * navigating away, so it does something Download does not.
 *
 * Progressive enhancement: the control is a plain link to the PDF, so with
 * JavaScript off (or if this file fails to load) it still opens the document
 * in a new tab. The viewer is built on first click and torn down on the
 * second, so a page with several papers never loads a PDF nobody asked for.
 */
(function () {
  'use strict';

  function frameFor(src) {
    var f = document.createElement('iframe');
    f.className = 'doc-frame';
    f.title = 'PDF preview';
    f.src = src + '#view=FitH';
    return f;
  }

  function label(a, key) {
    var t = a.getAttribute(key);
    if (t) a.textContent = t;
  }

  document.addEventListener('click', function (e) {
    if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target && e.target.closest ? e.target.closest('a.js-view') : null;
    if (!a) return;

    var box = document.getElementById(a.getAttribute('data-target') || '');
    if (!box) return;                       // no viewer slot: let the link work

    e.preventDefault();
    if (box.firstChild) {                   // open -> close, and drop the iframe
      box.textContent = '';
      box.hidden = true;
      a.setAttribute('aria-expanded', 'false');
      label(a, 'data-label-show');
    } else {
      box.hidden = false;
      box.appendChild(frameFor(a.getAttribute('href')));
      a.setAttribute('aria-expanded', 'true');
      label(a, 'data-label-hide');
      box.scrollIntoView({ block: 'nearest' });
    }
  });
})();
