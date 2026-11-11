document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".image-switcher").forEach((gallery) => {
    const hero = gallery.querySelector(".hero-image");
    const caption = gallery.querySelector(".hero-caption");
    const thumbs = Array.from(
      gallery.querySelectorAll(".image-thumbnails img"),
    );

    if (!hero || thumbs.length === 0) return;

    thumbs.forEach((thumb) => {
      thumb.addEventListener("click", () => {
        hero.src = thumb.src;
        hero.alt = thumb.alt;

        if (caption) {
          caption.textContent = thumb.alt;
        }
      });
    });
  });
});
