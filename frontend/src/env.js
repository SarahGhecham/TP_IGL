(function (window) {
    window.__env = window.__env || {};
    window.__env.API_URL = "${API_URL}";
    window.__env.TOKEN_EXPIRY = "${process.env.TOKEN_EXPIRY}";
  })(this);
  