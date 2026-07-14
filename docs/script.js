// ======================================================
// NetWatch Website
// ======================================================

document.addEventListener("DOMContentLoaded", () => {
  // ===========================================
  // Latest GitHub Release
  // ===========================================

  const releaseVersion = "1.0.0";
  const releaseFileName = `NetWatch-v${releaseVersion}-Windows.zip`;
  const releaseDownloadUrl = `https://github.com/Darkrider0007/NetWatch/releases/download/v${releaseVersion}/${releaseFileName}`;
  const downloadButton = document.getElementById("download-btn");
  const releaseDownloadButton = document.getElementById("release-download-btn");
  const footerDownloadButton = document.getElementById("footer-download-btn");
  const releaseVersionLabel = document.getElementById("release-version");
  const fallbackDownloadUrl =
    "https://github.com/Darkrider0007/NetWatch/releases/latest";

  if (downloadButton) {
    downloadButton.href = fallbackDownloadUrl;
  }

  if (releaseDownloadButton) {
    releaseDownloadButton.href = releaseDownloadUrl;
  }

  if (footerDownloadButton) {
    footerDownloadButton.href = releaseDownloadUrl;
  }

  if (releaseVersionLabel) {
    releaseVersionLabel.textContent = releaseVersion;
  }

  fetch("https://api.github.com/repos/Darkrider0007/NetWatch/releases/latest")
    .then((response) => response.json())

    .then((release) => {
      if (!downloadButton) {
        return;
      }

      if (release.assets && release.assets.length > 0) {
        downloadButton.href = release.assets[0].browser_download_url;
      } else if (release.html_url) {
        downloadButton.href = release.html_url;
      }
    })

    .catch((error) => {
      console.error(error);
    });

  // ===========================================
  // Smooth Scroll
  // ===========================================

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", function (e) {
      const target = document.querySelector(this.getAttribute("href"));

      if (!target) return;

      e.preventDefault();

      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    });
  });

  // ===========================================
  // Fade In Sections
  // ===========================================

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = 1;
          entry.target.style.transform = "translateY(0)";
        }
      });
    },

    {
      threshold: 0.15,
    },
  );

  document
    .querySelectorAll(".card, .gallery img, .download-box, .notice")
    .forEach((element) => {
      element.style.opacity = 0;
      element.style.transform = "translateY(35px)";
      element.style.transition = "all .7s ease";

      observer.observe(element);
    });

  // ===========================================
  // Active Navigation
  // ===========================================

  const sections = document.querySelectorAll("section");
  const navLinks = document.querySelectorAll(".navbar a");

  window.addEventListener("scroll", () => {
    let current = "";

    sections.forEach((section) => {
      const top = section.offsetTop - 120;

      if (window.scrollY >= top) {
        current = section.id;
      }
    });

    navLinks.forEach((link) => {
      link.classList.remove("active");

      if (link.getAttribute("href") === "#" + current) {
        link.classList.add("active");
      }
    });
  });

  // ===========================================
  // Lightbox
  // ===========================================

  const images = document.querySelectorAll(".gallery img");

  if (images.length) {
    const overlay = document.createElement("div");

    overlay.style.position = "fixed";
    overlay.style.left = 0;
    overlay.style.top = 0;
    overlay.style.width = "100%";
    overlay.style.height = "100%";
    overlay.style.background = "rgba(0,0,0,.92)";
    overlay.style.display = "none";
    overlay.style.justifyContent = "center";
    overlay.style.alignItems = "center";
    overlay.style.zIndex = "9999";
    overlay.style.cursor = "zoom-out";

    const img = document.createElement("img");

    img.style.maxWidth = "90%";
    img.style.maxHeight = "90%";
    img.style.borderRadius = "15px";
    img.style.boxShadow = "0 20px 60px rgba(0,0,0,.6)";

    overlay.appendChild(img);

    document.body.appendChild(overlay);

    images.forEach((image) => {
      image.addEventListener("click", () => {
        img.src = image.src;

        overlay.style.display = "flex";
      });
    });

    overlay.addEventListener("click", () => {
      overlay.style.display = "none";
    });
  }

  // ===========================================
  // Download Counter
  // ===========================================

  const downloadBtn = document.querySelector(".download-btn");

  if (downloadBtn) {
    downloadBtn.addEventListener("click", () => {
      console.log("Download Started");
    });
  }

  // ===========================================
  // Ripple Effect
  // ===========================================

  document.querySelectorAll(".btn").forEach((button) => {
    button.addEventListener("click", function (e) {
      const ripple = document.createElement("span");

      const rect = this.getBoundingClientRect();

      const size = Math.max(rect.width, rect.height);

      ripple.style.width = size + "px";
      ripple.style.height = size + "px";
      ripple.style.position = "absolute";
      ripple.style.borderRadius = "50%";
      ripple.style.background = "rgba(255,255,255,.35)";
      ripple.style.pointerEvents = "none";
      ripple.style.left = e.clientX - rect.left - size / 2 + "px";
      ripple.style.top = e.clientY - rect.top - size / 2 + "px";
      ripple.style.transform = "scale(0)";
      ripple.style.transition = "transform .6s, opacity .6s";

      this.style.position = "relative";
      this.style.overflow = "hidden";

      this.appendChild(ripple);

      requestAnimationFrame(() => {
        ripple.style.transform = "scale(4)";
        ripple.style.opacity = "0";
      });

      setTimeout(() => {
        ripple.remove();
      }, 600);
    });
  });

  // ===========================================
  // Current Year
  // ===========================================

  const year = document.getElementById("year");

  if (year) {
    year.textContent = new Date().getFullYear();
  }
});
