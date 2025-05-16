// This script handles the sidebar navigation for the dashboard
// It shows/hides sections based on the clicked link
document.addEventListener("DOMContentLoaded", function () {
  const links = document.querySelectorAll(".sidebar-link");
  const sections = document.querySelectorAll("#dashboardContent section");
  links.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const targetId = this.getAttribute("href").substring(1);
      sections.forEach((section) => {
        section.classList.add("hidden");
        if (section.id === targetId) {
          section.classList.remove("hidden");
        }
      });
      links.forEach((l) =>
        l.classList.remove("text-indigo-700", "font-semibold")
      );
      this.classList.add("text-indigo-700", "font-semibold");
    });
  });
});
