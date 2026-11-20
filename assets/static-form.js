/* Static replacement for the Contact Form 7 backend: opens the visitor's mail client. */
(function () {
  var RECIPIENT = 'info@skainet.io';
  document.addEventListener('submit', function (event) {
    var form = event.target;
    if (!form.classList || !form.classList.contains('wpcf7-form')) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    var missing = form.querySelector([aria-required=true]:placeholder-shown);
    if (missing) { missing.focus(); return; }

    var subject = 'Contact via skainet.io';
    var lines = [];
    Array.prototype.forEach.call(form.elements, function (el) {
      if (!el.name || el.name.charAt(0) === '_' || el.type === 'hidden' || el.type === 'submit') return;
      if ((el.type === 'checkbox' || el.type === 'radio') && !el.checked) return;
      var value = (el.value || '').trim();
      if (!value) return;
      if (/subject/i.test(el.name)) { subject = value; return; }
      lines.push(el.name.replace(/^your-?/i, '') + ': ' + value);
    });
    window.location.href = 'mailto:' + RECIPIENT +
      '?subject=' + encodeURIComponent(subject) +
      '&body=' + encodeURIComponent(lines.join('\n\n'));
  }, true);
})();
