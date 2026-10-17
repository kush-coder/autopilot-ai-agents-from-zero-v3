/**
 * Docsify 官方 gtag 插件（适用于 GA4 / Universal Analytics）
 * 源码：https://github.com/docsifyjs/docsify/blob/develop/src/plugins/gtag.js
 * 因 docsify@4 的 npm 包未包含此插件，故本地保留一份供项目使用。
 */
(function () {
  function appendScript(id) {
    var script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + id;
    document.body.appendChild(script);
  }

  function initGlobalSiteTag(id) {
    appendScript(id);
    window.dataLayer = window.dataLayer || [];
    window.gtag =
      window.gtag ||
      function () {
        window.dataLayer.push(arguments);
      };
    window.gtag("js", new Date());
    window.gtag("config", id);
  }

  function initAdditionalTag(id) {
    window.gtag("config", id);
  }

  function init(ids) {
    if (Array.isArray(ids)) {
      initGlobalSiteTag(ids[0]);
      for (var i = 1; i < ids.length; i++) {
        initAdditionalTag(ids[i]);
      }
    } else {
      initGlobalSiteTag(ids);
    }
  }

  function collect() {
    if (!window.gtag) {
      init(window.$docsify.gtag);
    }
    window.gtag("event", "page_view", {
      page_title: document.title,
      page_location: location.href,
      page_path: location.pathname,
    });
  }

  function install(hook) {
    if (!window.$docsify.gtag) {
      console.error("[Docsify] gtag is required.");
      return;
    }
    hook.beforeEach(collect);
  }

  window.$docsify = window.$docsify || {};
  window.$docsify.plugins = [install].concat(window.$docsify.plugins || []);
})();
