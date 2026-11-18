(function () {
  var ROOT = new URL("../", document.currentScript.src);
  var box = document.getElementById("player");
  if (!box) return;

  var section = box.dataset.section;
  var lesson = box.dataset.lesson;
  var src = ((window.MEDIA || {})[section + "-" + lesson] || "").trim();

  function el(tag, attrs, html) {
    var e = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (html) e.innerHTML = html;
    return e;
  }

  function youtubeId(u) {
    var m = u.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?(?:.*&)?v=|embed\/|shorts\/|live\/))([\w-]{11})/);
    return m ? m[1] : null;
  }

  function render() {
    if (!src) {
      box.appendChild(el("div", { "class": "empty" },
        '<span class="big">⏳</span>سيتم إضافة الشرح قريبًا'));
      return;
    }

    var yt = youtubeId(src);
    if (yt) {
      box.appendChild(el("iframe", {
        src: "https://www.youtube-nocookie.com/embed/" + yt + "?rel=0",
        title: document.title, allowfullscreen: "", loading: "lazy",
        allow: "accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture"
      }));
      return;
    }

    var vm = src.match(/vimeo\.com\/(?:video\/)?(\d+)/);
    if (vm) {
      box.appendChild(el("iframe", {
        src: "https://player.vimeo.com/video/" + vm[1], title: document.title,
        allowfullscreen: "", loading: "lazy", allow: "autoplay; fullscreen; picture-in-picture"
      }));
      return;
    }

    var dr = src.match(/drive\.google\.com\/(?:file\/d\/|open\?id=|uc\?(?:.*&)?id=)([\w-]+)/);
    if (dr) {
      box.appendChild(el("iframe", {
        src: "https://drive.google.com/file/d/" + dr[1] + "/preview", title: document.title,
        allowfullscreen: "", loading: "lazy", allow: "autoplay"
      }));
      return;
    }

    var url = /^https?:\/\//i.test(src) ? src : new URL(src, ROOT).href;
    var path = url.split("?")[0].toLowerCase();

    if (/\.(mp3|m4a|ogg|oga|wav|aac)$/.test(path) || (section === "audio" && !/\.(mp4|webm|mov)$/.test(path))) {
      var wrap = el("div", { "class": "audio-box" }, '<span class="big">🎧</span>');
      wrap.appendChild(el("audio", { controls: "", preload: "none", src: url }));
      box.appendChild(wrap);
    } else if (/\.(mp4|webm|mov|m4v)$/.test(path)) {
      box.appendChild(el("video", { controls: "", preload: "metadata", playsinline: "", src: url }));
    } else {
      box.appendChild(el("div", { "class": "linkout" },
        '<a class="btn primary" target="_blank" rel="noopener" href="' + url + '">فتح الشرح ←</a>'));
    }
  }

  render();

  // التنقل بالأسهم (في الواجهة العربية: ← التالي، → السابق)
  document.addEventListener("keydown", function (e) {
    var t = e.target && e.target.tagName;
    if (/^(AUDIO|VIDEO|INPUT|TEXTAREA|IFRAME)$/.test(t) || e.altKey || e.ctrlKey || e.metaKey) return;
    var b = document.body.dataset;
    if (e.key === "ArrowLeft" && b.next) location.href = b.next + ".html";
    if (e.key === "ArrowRight" && b.prev) location.href = b.prev + ".html";
  });
})();
