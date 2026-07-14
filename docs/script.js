// ======================================================
// NetWatch Website
// ======================================================

document.addEventListener("DOMContentLoaded", () => {
  // ===========================================
  // Latest GitHub Release
  // ===========================================

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
    releaseDownloadButton.href = fallbackDownloadUrl;
  }

  if (footerDownloadButton) {
    footerDownloadButton.href = fallbackDownloadUrl;
  }

  if (releaseVersionLabel) {
    releaseVersionLabel.textContent = "Latest";
  }

  fetch("https://api.github.com/repos/Darkrider0007/NetWatch/releases/latest")
    .then((response) => response.json())

    .then((release) => {
      const releaseUrl = release?.html_url || fallbackDownloadUrl;
      const windowsAsset = release?.assets?.find((asset) => {
        const name = asset?.name?.toLowerCase() || "";
        return name.includes("windows") && name.endsWith(".zip");
      });
      const firstAsset = release?.assets?.[0];
      const downloadUrl =
        windowsAsset?.browser_download_url ||
        firstAsset?.browser_download_url ||
        releaseUrl;
      const latestVersion = release?.tag_name || release?.name || "Latest";

      if (downloadButton) {
        downloadButton.href = downloadUrl;
      }

      if (releaseDownloadButton) {
        releaseDownloadButton.href = downloadUrl;
      }

      if (footerDownloadButton) {
        footerDownloadButton.href = downloadUrl;
      }

      if (releaseVersionLabel) {
        releaseVersionLabel.textContent = latestVersion.replace(/^v/i, "");
      }

      if (!downloadButton && !releaseDownloadButton && !footerDownloadButton) {
        return;
      }
    })

    .catch((error) => {
      console.error(error);

      if (releaseVersionLabel) {
        releaseVersionLabel.textContent = "Latest";
      }
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

  const copyright = document.getElementById("copyright");

  if (copyright) {
    const currentYear = new Date().getFullYear();
    copyright.textContent = `© ${currentYear} Rohan Gope`;
  }
});
