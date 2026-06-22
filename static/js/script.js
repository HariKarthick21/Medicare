document.addEventListener("DOMContentLoaded", function () {

    /* ================= NAVBAR CLOSE (MOBILE) ================= */
    document.addEventListener("click", function (event) {
        const navbar = document.getElementById("navbarNav");
        const toggler = document.querySelector(".navbar-toggler");

        const isClickInside =
            navbar.contains(event.target) ||
            toggler.contains(event.target);

        if (!isClickInside && navbar.classList.contains("show")) {
            new bootstrap.Collapse(navbar).hide();
        }
    });

    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", () => {
            const navbar = document.getElementById("navbarNav");
            if (navbar.classList.contains("show")) {
                new bootstrap.Collapse(navbar).hide();
            }
        });
    });

    /* ================= YEAR ================= */
    const yearSpan = document.getElementById("year");
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    /* ================= MAP MODAL ================= */
    const openBtns = document.querySelectorAll(".openMap");
    const mapModal = document.getElementById("mapModal");
    const closeMap = document.getElementById("closeMap");

    if (openBtns && mapModal && closeMap) {

        openBtns.forEach(btn => {
            btn.addEventListener("click", function () {
                mapModal.classList.add("show");   // ✅ OPEN
            });
        });

        closeMap.addEventListener("click", function () {
            mapModal.classList.remove("show");   // ✅ CLOSE
        });

        window.addEventListener("click", function (e) {
            if (e.target === mapModal) {
                mapModal.classList.remove("show");
            }
        });
    }

    /* ================= SOCIAL MODAL ================= */
    const socialBtns = document.querySelectorAll(".social-btn");
    const socialModal = document.getElementById("socialModal");
    const closeSocial = document.getElementById("closeSocial");
    const socialTitle = document.getElementById("socialTitle");
    const socialText = document.getElementById("socialText");
    const socialLink = document.getElementById("socialLink");

    const socialData = {
        facebook: {
            title: "Follow us on Facebook",
            text: "Get latest updates, health tips and news.",
            link: "https://www.facebook.com/"
        },
        instagram: {
            title: "Follow us on Instagram",
            text: "See our hospital life and stories.",
            link: "https://www.instagram.com/"
        },
        youtube: {
            title: "Subscribe to our YouTube",
            text: "Watch health awareness videos.",
            link: "https://www.youtube.com/"
        },
        twitter: {
            title: "Follow us on Twitter",
            text: "Stay updated with quick announcements.",
            link: "https://twitter.com/"
        }
    };

    if (socialBtns && socialModal && closeSocial) {

        socialBtns.forEach(btn => {
            btn.addEventListener("click", function () {
                const platform = btn.getAttribute("data-platform");
                const data = socialData[platform];

                if (!data) return;

                socialTitle.textContent = data.title;
                socialText.textContent = data.text;
                socialLink.href = data.link;

                socialModal.classList.add("show");   // ✅ OPEN
            });
        });

        closeSocial.addEventListener("click", function () {
            socialModal.classList.remove("show");   // ✅ CLOSE
        });

        window.addEventListener("click", function (e) {
            if (e.target === socialModal) {
                socialModal.classList.remove("show");
            }
        });
    }

});