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

    // ── Dynamic projects from /api/projects ────────────────────────────
    function renderProjects(projects) {
        const grid = document.getElementById("projects-grid");
        if (!grid) return;
        if (!Array.isArray(projects) || projects.length === 0) {
            grid.innerHTML =
                '<div class="col-12"><p class="text-muted">Loading projects…</p></div>';
            return;
        }
        const cards = projects
            .map((p) => {
                const tech = (p.tech || [])
                    .map((t) => `<span class="tech-badge">${escapeHtml(t)}</span>`)
                    .join("");
                const links = (p.links || [])
                    .map((l) => {
                        const isLive = /live/i.test(l.label);
                        const cls = isLive ? "btn-primary" : "btn-outline-primary";
                        const icon = isLive
                            ? "bi bi-box-arrow-up-right"
                            : "bi bi-github";
                        return `<a href="${escapeHtml(l.url)}" class="btn ${cls} btn-sm flex-fill" target="_blank"><i class="${icon} me-1"></i>${escapeHtml(l.label)}</a>`;
                    })
                    .join("");
                return `<div class="col-lg-4">
                        <div class="card project-card h-100">
                            <div class="card-body d-flex flex-column">
                                <div class="project-icon"><i class="bi ${escapeHtml(p.icon || "bi-star")}"></i></div>
                                <h5 class="card-title">${escapeHtml(p.title)}</h5>
                                <p class="card-text text-muted small flex-grow-1">${escapeHtml(p.description)}</p>
                                <div class="mb-3">${tech}</div>
                                <div class="mt-auto d-flex gap-2">${links}</div>
                            </div>
                        </div>
                    </div>`;
            })
            .join("");
        grid.innerHTML = cards;
    }

    function escapeHtml(str) {
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;");
    }

    fetch("api/projects")
        .then((r) => r.json())
        .then(renderProjects)
        .catch(() => renderProjects([]));

    // ── Visitor counter ───────────────────────────────────────────────
    const visitEl = document.getElementById("visit-count");
    if (visitEl) {
        fetch("api/visits")
            .then((r) => r.json())
            .then((d) => {
                visitEl.textContent = d.count;
            })
            .catch(() => {
                visitEl.textContent = "—";
            });
    }

    // ── Contact form ─────────────────────────────────────────────────
    const form = document.getElementById("contact-form");
    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();
            const status = document.getElementById("cf-status");
            const btn = document.getElementById("cf-submit");
            const payload = {
                name: document.getElementById("cf-name").value,
                email: document.getElementById("cf-email").value,
                subject: document.getElementById("cf-subject").value,
                message: document.getElementById("cf-message").value,
            };
            if (!payload.name || !payload.email || !payload.message) {
                status.innerHTML = '<span class="text-warning">Please fill in all required fields.</span>';
                return;
            }
            btn.disabled = true;
            fetch("api/contact", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            })
                .then((r) => r.json())
                .then((d) => {
                    if (d.ok) {
                        status.innerHTML = '<span class="text-success">' + escapeHtml(d.message) + "</span>";
                        form.reset();
                    } else {
                        status.innerHTML = '<span class="text-danger">' + escapeHtml(d.error || "Something went wrong.") + "</span>";
                    }
                })
                .catch(() => {
                    status.innerHTML = '<span class="text-danger">Could not reach the server. Try again.</span>';
                })
                .finally(() => {
                    btn.disabled = false;
                });
        });
    }
});