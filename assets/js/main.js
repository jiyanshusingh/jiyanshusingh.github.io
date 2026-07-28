document.addEventListener("DOMContentLoaded", function () {
    const nav = document.querySelector("#mainNav");
    const navLinks = document.querySelectorAll(".nav-link");

    function setActiveLink() {
        const scrollPos = window.scrollY + 100;
        let currentSection = "";

        document.querySelectorAll("section").forEach((section) => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            if (scrollPos >= top && scrollPos < top + height) {
                currentSection = section.getAttribute("id");
            }
        });

        navLinks.forEach((link) => {
            link.classList.remove("active");
            if (link.getAttribute("href") === "#" + currentSection) {
                link.classList.add("active");
            }
        });
    }

    window.addEventListener("scroll", setActiveLink);
    setActiveLink();

    navLinks.forEach((link) => {
        link.addEventListener("click", function (e) {
            const target = document.querySelector(this.getAttribute("href"));
            if (target) {
                e.preventDefault();
                const offset = 76;
                window.scrollTo({
                    top: target.offsetTop - offset,
                    behavior: "smooth",
                });
                const coll = document.querySelector(".navbar-collapse");
                if (coll.classList.contains("show")) {
                    bootstrap.Collapse.getInstance(coll).hide();
                }
            }
        });
    });
});
