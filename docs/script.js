// ======================================================
// NetWatch Website
// ======================================================

document.addEventListener("DOMContentLoaded", async () => {
  const githubRepository = "Darkrider0007/NetWatch";

  const fallbackRelease = `https://github.com/${githubRepository}/releases/latest`;

  const downloadButtons = [
    document.getElementById("download-btn"),

    document.getElementById("release-download-btn"),

    document.getElementById("footer-download-btn"),
  ];

  const versionLabel = document.getElementById("release-version");

  // ==================================================
  // Default Download Links
  // ==================================================

  downloadButtons.forEach((button) => {
    if (button) {
      button.href = fallbackRelease;
    }
  });

  if (versionLabel) {
    versionLabel.textContent = "Latest";
  }

  // ==================================================
  // Fetch Latest GitHub Release
  // ==================================================

  try {
    const response = await fetch(
      `https://api.github.com/repos/${githubRepository}/releases/latest`,
    );

    if (!response.ok) {
      throw new Error("Unable to fetch release information.");
    }

    const release = await response.json();

    let downloadUrl = release.html_url;

    if (release.assets && release.assets.length > 0) {
      const windowsAsset = release.assets.find((asset) => {
        const name = asset.name.toLowerCase();

        return name.endsWith(".zip") || name.endsWith(".exe");
      });

      if (windowsAsset) {
        downloadUrl = windowsAsset.browser_download_url;
      }
    }

    downloadButtons.forEach((button) => {
      if (button) {
        button.href = downloadUrl;
      }
    });

    if (versionLabel) {
      versionLabel.textContent = release.tag_name.replace(/^v/i, "");
    }
  } catch (error) {
    console.error(error);
  }

  // ==================================================
  // Smooth Scroll
  // ==================================================

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (event) => {
      const target = document.querySelector(link.getAttribute("href"));

      if (!target) {
        return;
      }

      event.preventDefault();

      target.scrollIntoView({
        behavior: "smooth",

        block: "start",
      });
    });
  });

  // ==================================================
  // Current Year
  // ==================================================

  const copyright = document.getElementById("copyright");

  if (copyright) {
    copyright.textContent = `© ${new Date().getFullYear()} NetWatch Contributors`;
  }
});
