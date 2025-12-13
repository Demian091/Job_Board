// Robust dropdown: click to open, click outside to close, arrow rotates
document.addEventListener("DOMContentLoaded", () => {
  const dd = document.querySelector("[data-dropdown]");
  if (!dd) return;

  const trigger = dd.querySelector(".nav__trigger");
  const menu = dd.querySelector(".nav__menu");

  const close = () => {
    dd.classList.remove("open");
    trigger.setAttribute("aria-expanded", "false");
  };

  trigger.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    const isOpen = dd.classList.toggle("open");
    trigger.setAttribute("aria-expanded", String(isOpen));
  });

  // Close when clicking outside
  document.addEventListener("click", (e) => {
    if (!dd.contains(e.target)) close();
  });

  // Close on Escape
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") close();
  });

  // Keep menu fully visible on tiny screens
  const keepInView = () => {
    const rect = menu.getBoundingClientRect();
    if (rect.right > window.innerWidth) menu.style.left = `-${rect.right - window.innerWidth + 16}px`;
    else menu.style.left = "";
  };
  window.addEventListener("resize", keepInView);
});

function toggleCommentForm(postId) {
    const el = document.getElementById(`comment-form-${postId}`);
    el.style.display = el.style.display === "none" ? "block" : "none";
}

function sharePost(url) {
    navigator.clipboard.writeText(url);
    alert("Post link copied!");
}
