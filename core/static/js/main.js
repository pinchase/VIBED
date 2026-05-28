document.addEventListener("DOMContentLoaded", () => {

    /* ── Mobile nav ─────────────────────────────────────── */
    const menuToggle = document.getElementById("menu-toggle");
    const navMenu = document.getElementById("nav-menu");

    if (menuToggle && navMenu) {
        menuToggle.addEventListener("click", () => {
            const isOpen = navMenu.classList.toggle("active");
            menuToggle.setAttribute("aria-expanded", String(isOpen));
        });
        navMenu.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", () => {
                navMenu.classList.remove("active");
                menuToggle.setAttribute("aria-expanded", "false");
            });
        });
    }

    /* ── Contact form — inline error messages ───────────── */
    const contactForm = document.querySelector(".contact-form");
    if (contactForm) {
        contactForm.addEventListener("submit", (event) => {
            const requiredFields = contactForm.querySelectorAll("[required]");
            let hasError = false;

            requiredFields.forEach((field) => {
                if (!field.value.trim()) {
                    hasError = true;
                    field.setAttribute("aria-invalid", "true");
                } else {
                    field.removeAttribute("aria-invalid");
                }
            });

            const email = contactForm.querySelector('input[type="email"]');
            if (email && email.value.trim() && !email.checkValidity()) {
                hasError = true;
                email.setAttribute("aria-invalid", "true");
            }

            if (hasError) {
                event.preventDefault();
                let errorBox = contactForm.querySelector(".form-error");
                if (!errorBox) {
                    errorBox = document.createElement("p");
                    errorBox.className = "form-error";
                    contactForm.prepend(errorBox);
                }
                // Re-trigger shake animation
                errorBox.style.animation = "none";
                errorBox.offsetHeight; // reflow
                errorBox.style.animation = "";
                errorBox.textContent = "Please fill out all required fields with valid details.";
                errorBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
            }
        });
    }

    /* ── Lightbox ────────────────────────────────────────── */
    const galleryButtons = Array.from(document.querySelectorAll("[data-lightbox-src]"));
    const lightbox = document.getElementById("lightbox");
    const lightboxImage = lightbox ? lightbox.querySelector(".lightbox-image") : null;
    const closeButton = lightbox ? lightbox.querySelector(".lightbox-close") : null;
    const prevButton = lightbox ? lightbox.querySelector(".lightbox-prev") : null;
    const nextButton = lightbox ? lightbox.querySelector(".lightbox-next") : null;
    let currentIndex = 0;

    function showImage(index) {
        if (!lightbox || !lightboxImage || galleryButtons.length === 0) return;
        currentIndex = (index + galleryButtons.length) % galleryButtons.length;
        const activeButton = galleryButtons[currentIndex];
        lightboxImage.src = activeButton.dataset.lightboxSrc;
        lightboxImage.alt = activeButton.dataset.lightboxAlt || "";
        lightbox.classList.add("active");
        lightbox.setAttribute("aria-hidden", "false");
        document.body.style.overflow = "hidden";
    }

    function closeLightbox() {
        if (!lightbox || !lightboxImage) return;
        lightbox.classList.remove("active");
        lightbox.setAttribute("aria-hidden", "true");
        lightboxImage.src = "";
        document.body.style.overflow = "";
    }

    galleryButtons.forEach((button, index) => button.addEventListener("click", () => showImage(index)));
    if (closeButton) closeButton.addEventListener("click", closeLightbox);
    if (prevButton) prevButton.addEventListener("click", () => showImage(currentIndex - 1));
    if (nextButton) nextButton.addEventListener("click", () => showImage(currentIndex + 1));
    if (lightbox) {
        lightbox.addEventListener("click", (event) => { if (event.target === lightbox) closeLightbox(); });
    }
    document.addEventListener("keydown", (event) => {
        if (!lightbox || !lightbox.classList.contains("active")) return;
        if (event.key === "Escape") closeLightbox();
        if (event.key === "ArrowLeft") showImage(currentIndex - 1);
        if (event.key === "ArrowRight") showImage(currentIndex + 1);
    });

    /* ── Scroll-reveal ───────────────────────────────────── */
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    const revealTargets = document.querySelectorAll(
        ".section, .feature-card, .value-card, .testimonial-card, " +
        ".client-card, .step-card, .stat-item, " +
        ".story-block, .expertise-list > div"
    );
    revealTargets.forEach((el) => {
        el.classList.add("reveal");
        revealObserver.observe(el);
    });

    /* ── Program carousel controls ─────────────────────────── */
    document.querySelectorAll("[data-program-section]").forEach((section) => {
        const carousel = section.querySelector("[data-program-carousel]");
        const prevButton = section.querySelector("[data-program-prev]");
        const nextButton = section.querySelector("[data-program-next]");
        const status = section.querySelector("[data-program-status]");
        if (!carousel || !prevButton || !nextButton || !status) return;

        const cards = Array.from(carousel.querySelectorAll(".program-card"));
        if (cards.length === 0) return;

        const getActiveIndex = () => {
            const carouselLeft = carousel.getBoundingClientRect().left;
            return cards.reduce((closestIndex, card, index) => {
                const currentDistance = Math.abs(card.getBoundingClientRect().left - carouselLeft);
                const closestDistance = Math.abs(cards[closestIndex].getBoundingClientRect().left - carouselLeft);
                return currentDistance < closestDistance ? index : closestIndex;
            }, 0);
        };

        const updateCarouselState = () => {
            const activeIndex = getActiveIndex();
            status.textContent = `Program ${activeIndex + 1} of ${cards.length}`;
            prevButton.disabled = activeIndex === 0;
            nextButton.disabled = activeIndex === cards.length - 1;
        };

        const scrollToCard = (index) => {
            const targetIndex = Math.max(0, Math.min(cards.length - 1, index));
            cards[targetIndex].scrollIntoView({
                behavior: "smooth",
                block: "nearest",
                inline: "start",
            });
        };

        prevButton.addEventListener("click", () => scrollToCard(getActiveIndex() - 1));
        nextButton.addEventListener("click", () => scrollToCard(getActiveIndex() + 1));
        carousel.addEventListener("scroll", () => window.requestAnimationFrame(updateCarouselState), { passive: true });
        window.addEventListener("resize", updateCarouselState, { passive: true });
        updateCarouselState();
    });

    /* ── Back to top ─────────────────────────────────────── */
    const backTop = document.getElementById("back-top");
    if (backTop) {
        window.addEventListener("scroll", () => {
            backTop.classList.toggle("visible", window.scrollY > 400);
        }, { passive: true });
        backTop.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    /* ── SFA Modal ───────────────────────────────────────── */
    const sfaModal = document.getElementById("sfa-modal");
    const sfaOpenBtns = document.querySelectorAll(".sfa-modal-open");
    const sfaCloseBtn = document.getElementById("sfa-modal-close");

    function openSfaModal() {
        if (!sfaModal) return;
        sfaModal.classList.add("active");
        sfaModal.setAttribute("aria-hidden", "false");
        document.body.style.overflow = "hidden";
        sfaCloseBtn && sfaCloseBtn.focus();
    }

    function closeSfaModal() {
        if (!sfaModal) return;
        sfaModal.classList.remove("active");
        sfaModal.setAttribute("aria-hidden", "true");
        document.body.style.overflow = "";
    }

    sfaOpenBtns.forEach(btn => btn.addEventListener("click", openSfaModal));
    if (sfaCloseBtn) sfaCloseBtn.addEventListener("click", closeSfaModal);
    if (sfaModal) {
        sfaModal.addEventListener("click", (e) => { if (e.target === sfaModal) closeSfaModal(); });
    }
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && sfaModal && sfaModal.classList.contains("active")) closeSfaModal();
    });

});
