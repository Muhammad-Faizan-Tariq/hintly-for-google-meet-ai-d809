(function () {
  'use strict';

  if (document.getElementById('hintly-sidebar')) return;

  var SIDEBAR_URL = 'https://hintly.ai/embed/sidebar';

  function getMeetingId() {
    var match = window.location.pathname.match(/\/([a-z0-9\-]{10,})/i);
    return match ? match[1] : 'unknown';
  }

  var sidebar = document.createElement('iframe');
  sidebar.id = 'hintly-sidebar';
  sidebar.src = SIDEBAR_URL + '?meetingId=' + getMeetingId();
  sidebar.setAttribute('title', 'Hintly AI Assistant');
  sidebar.style.cssText = [
    'position:fixed',
    'top:0',
    'right:0',
    'width:320px',
    'height:100vh',
    'z-index:9999',
    'border:none',
    'border-left:1px solid rgba(255,255,255,0.08)',
    'background:transparent',
    'transition:transform 0.25s cubic-bezier(0.16,1,0.3,1)',
  ].join(';');

  document.body.appendChild(sidebar);

  var visible = true;

  // Toggle sidebar with Alt+H
  document.addEventListener('keydown', function (e) {
    if (e.altKey && e.key === 'h') {
      visible = !visible;
      sidebar.style.transform = visible ? 'translateX(0)' : 'translateX(100%)';
    }
  });

  // Notify sidebar of meeting ID via postMessage when it loads
  sidebar.addEventListener('load', function () {
    sidebar.contentWindow.postMessage(
      { type: 'HINTLY_INIT', meetingId: getMeetingId() },
      SIDEBAR_URL
    );
  });
})();
