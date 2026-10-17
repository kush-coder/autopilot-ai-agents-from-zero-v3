(function (root, factory) {
  var api = factory(root);

  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  }

  if (root && typeof root === "object") {
    root.DocsifyAnnouncementBubble = api;
  }
})(
  typeof window !== "undefined" ? window : globalThis,
  function (root) {
    var BUBBLE_ID = "docsify-announcement-bubble";
    var DISMISSED_VALUE = "dismissed";

    function canShow(config, localStorage) {
      if (!config || config.enabled === false || !config.text) return false;
      if (!config.storageKey || !localStorage) return true;

      try {
        return localStorage.getItem(config.storageKey) !== DISMISSED_VALUE;
      } catch (error) {
        return true;
      }
    }

    function rememberDismissal(config, localStorage) {
      if (!config || !config.storageKey || !localStorage) return;

      try {
        localStorage.setItem(config.storageKey, DISMISSED_VALUE);
      } catch (error) {
        // Private browsing or blocked storage should not break reading.
      }
    }

    function renderAnnouncementBubble(config, env) {
      var runtime = env || root || {};
      var document = runtime.document;
      var localStorage = runtime.localStorage;
      var existing;
      var bubble;
      var content;
      var dot;
      var text;
      var close;

      if (!document || !document.body || !canShow(config, localStorage)) {
        return null;
      }

      existing = document.getElementById && document.getElementById(BUBBLE_ID);
      if (existing && existing.remove) existing.remove();

      bubble = document.createElement("div");
      bubble.className = "announcement-bubble";
      bubble.setAttribute("id", BUBBLE_ID);
      bubble.setAttribute("aria-label", config.text);

      content = document.createElement(config.link ? "a" : "span");
      content.className = "announcement-bubble__content";
      if (config.link) {
        content.href = config.link;
      }

      dot = document.createElement("span");
      dot.className = "announcement-bubble__dot";
      dot.setAttribute("aria-hidden", "true");

      text = document.createElement("span");
      text.className = "announcement-bubble__text";
      text.textContent = config.text;

      close = document.createElement("button");
      close.type = "button";
      close.className = "announcement-bubble__close";
      close.setAttribute("aria-label", "关闭公告");
      close.textContent = "x";
      close.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();
        rememberDismissal(config, localStorage);
        bubble.remove();
      });

      content.appendChild(dot);
      content.appendChild(text);
      bubble.appendChild(content);
      bubble.appendChild(close);
      document.body.appendChild(bubble);

      return bubble;
    }

    function init(config, env) {
      var runtime = env || root || {};
      var document = runtime.document;

      if (!document) return null;

      function render() {
        return renderAnnouncementBubble(config, runtime);
      }

      if (document.readyState === "loading" && document.addEventListener) {
        document.addEventListener("DOMContentLoaded", render, { once: true });
        return null;
      }

      return render();
    }

    function initFromDocsify(env) {
      var runtime = env || root || {};
      var config = runtime.$docsify && runtime.$docsify.announcementBubble;

      return init(config, runtime);
    }

    if (root && root.document) {
      initFromDocsify(root);
    }

    return {
      canShow: canShow,
      init: init,
      initFromDocsify: initFromDocsify,
      renderAnnouncementBubble: renderAnnouncementBubble,
    };
  }
);
