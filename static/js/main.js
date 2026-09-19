document.addEventListener("DOMContentLoaded", () => {
  // 0. Remove is-loading state on initial animation frame to prevent FOUC / load transition flash
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      document.body.classList.remove("is-loading");
    });
  });

  // 1. Ensure Background Video Autoplays smoothly
  const heroVideo = document.querySelector(".hero-video");
  if (heroVideo) {
    heroVideo.muted = true;
    const playPromise = heroVideo.play();
    if (playPromise !== undefined) {
      playPromise.catch(() => {
        // Retry on first user interaction if browser autoplay policy blocks
        const playOnGesture = () => {
          heroVideo.play().catch(() => {});
          window.removeEventListener("click", playOnGesture);
          window.removeEventListener("touchstart", playOnGesture);
        };
        window.addEventListener("click", playOnGesture, { once: true });
        window.addEventListener("touchstart", playOnGesture, { once: true });
      });
    }
  }

  // 2. Scroll-driven Floating Boxed Navbar (Smooth Slide Down)
  const floatingNav = document.getElementById("floating-box-nav");
  const SCROLL_ENTER = 140; // Slide down once user scrolls past 140px
  const SCROLL_LEAVE = 70;  // Slide up cleanly when user returns near top

  const updateFloatingNav = () => {
    const scrollY = window.scrollY || document.documentElement.scrollTop || 0;
    if (!floatingNav) return;

    if (scrollY > SCROLL_ENTER) {
      floatingNav.classList.add("is-visible");
    } else if (scrollY <= SCROLL_LEAVE) {
      floatingNav.classList.remove("is-visible");
    }
  };

  let scrollStopTimer = null;
  const onScroll = () => {
    updateFloatingNav();
    clearTimeout(scrollStopTimer);
    scrollStopTimer = setTimeout(updateFloatingNav, 50);
  };

  window.addEventListener("scroll", onScroll, { passive: true });
  if ("onscrollend" in window) {
    window.addEventListener("scrollend", updateFloatingNav, { passive: true });
  }
  updateFloatingNav();

  // 3. Mobile Navigation Drawer
  const drawer = document.querySelector(".mobile-drawer");
  const overlay = document.querySelector(".drawer-overlay");
  const toggleButtons = document.querySelectorAll(".mobile-toggle");
  const closeBtn = document.querySelector(".drawer-close");

  const openDrawer = () => {
    if (drawer && overlay) {
      drawer.classList.add("is-open");
      overlay.classList.add("is-open");
      document.body.style.overflow = "hidden";
    }
  };

  const closeDrawer = () => {
    if (drawer && overlay) {
      drawer.classList.remove("is-open");
      overlay.classList.remove("is-open");
      document.body.style.overflow = "";
    }
  };

  toggleButtons.forEach((btn) => {
    btn.addEventListener("click", openDrawer);
  });
  if (closeBtn) closeBtn.addEventListener("click", closeDrawer);
  if (overlay) overlay.addEventListener("click", closeDrawer);

  document.querySelectorAll(".drawer-menu a").forEach((link) => {
    link.addEventListener("click", closeDrawer);
  });

  // 4. Smooth Scroll Reveal Animations
  const revealElements = document.querySelectorAll(".scroll-reveal");
  if (revealElements.length > 0) {
    if ("IntersectionObserver" in window) {
      const revealObserver = new IntersectionObserver(
        (entries, observer) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              observer.unobserve(entry.target);
            }
          });
        },
        {
          threshold: 0.12,
          rootMargin: "0px 0px -30px 0px",
        }
      );

      revealElements.forEach((el) => revealObserver.observe(el));
    } else {
      revealElements.forEach((el) => el.classList.add("is-visible"));
    }
  }

  // 5. Category Text Rotator in Primary Button (Nutraceuticals -> Beverages -> Personal Care)
  const heroCtaBtn = document.getElementById("hero-cta-btn");
  const rotator = document.querySelector(".btn-rotator");
  const rotatorItems = document.querySelectorAll(".btn-rotator-item");
  if (heroCtaBtn && rotator && rotatorItems.length > 1) {
    let currentIndex = 0;
    let rotatorTimer = null;
    const intervalTime = 2600; // 2.6 seconds per category

    const cycleCategory = () => {
      const currentItem = rotatorItems[currentIndex];
      currentIndex = (currentIndex + 1) % rotatorItems.length;
      const nextItem = rotatorItems[currentIndex];

      currentItem.classList.remove("is-active");
      currentItem.classList.add("is-exiting");

      nextItem.classList.remove("is-exiting");
      nextItem.classList.add("is-active");

      if (nextItem.dataset.href) {
        heroCtaBtn.setAttribute("href", nextItem.dataset.href);
        heroCtaBtn.setAttribute("aria-label", "Shop " + nextItem.textContent.trim());
      }

      setTimeout(() => {
        currentItem.classList.remove("is-exiting");
      }, 400);
    };

    const startRotator = () => {
      if (!rotatorTimer) {
        rotatorTimer = setInterval(cycleCategory, intervalTime);
      }
    };

    const stopRotator = () => {
      if (rotatorTimer) {
        clearInterval(rotatorTimer);
        rotatorTimer = null;
      }
    };

    startRotator();

    // Pause on hover for comfortable clicking
    heroCtaBtn.addEventListener("mouseenter", stopRotator);
    heroCtaBtn.addEventListener("mouseleave", startRotator);
  }

  // 6. Living Botanical Categories Section: Scroll Reveals & 3D Parallax Tilt
  const categoriesSection = document.getElementById("categories");
  const categoryRevealGroup = document.querySelector(".categories-grid.reveal-group");
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // 6a. Scroll Reveal for Botanical Line-art Borders, Growing Vine Underline, and Cascading Cards
  if (categoriesSection) {
    if (prefersReducedMotion || !("IntersectionObserver" in window)) {
      categoriesSection.classList.add("is-in-view");
      if (categoryRevealGroup) categoryRevealGroup.classList.add("is-visible");
    } else {
      const botanicalObserver = new IntersectionObserver(
        (entries, observer) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              categoriesSection.classList.add("is-in-view");
              if (categoryRevealGroup) categoryRevealGroup.classList.add("is-visible");
              observer.unobserve(entry.target); // Trigger ONCE only
            }
          });
        },
        {
          threshold: 0.1,
          rootMargin: "0px 0px -40px 0px",
        }
      );
      botanicalObserver.observe(categoriesSection);
    }
  }

  // 6b. Subtle 3D Parallax Tilt on Product Image Stage (rAF Throttled, Disabled on Touch & Reduced Motion)
  const isTouchDevice =
    "ontouchstart" in window ||
    navigator.maxTouchPoints > 0 ||
    window.matchMedia("(hover: none)").matches;

  if (!prefersReducedMotion && !isTouchDevice) {
    const categoryCards = document.querySelectorAll(".category-card");

    categoryCards.forEach((card) => {
      const tiltWrap = card.querySelector(".category-img-tilt-wrap");
      if (!tiltWrap) return;

      let bounds = null;
      let rafId = null;
      let targetRotX = 0;
      let targetRotY = 0;
      const MAX_TILT = 6.5; // Max 6.5 degrees for organic, calm feel

      const onMouseEnter = () => {
        bounds = card.getBoundingClientRect();
      };

      const onMouseMove = (e) => {
        if (!bounds) bounds = card.getBoundingClientRect();

        const x = e.clientX - bounds.left;
        const y = e.clientY - bounds.top;
        const normX = (x / bounds.width - 0.5) * 2; // -1 to 1
        const normY = (y / bounds.height - 0.5) * 2; // -1 to 1

        targetRotY = normX * MAX_TILT;
        targetRotX = -normY * MAX_TILT;

        if (!rafId) {
          rafId = requestAnimationFrame(() => {
            tiltWrap.style.transform = `perspective(800px) rotateX(${targetRotX.toFixed(2)}deg) rotateY(${targetRotY.toFixed(2)}deg) scale3d(1.04, 1.04, 1.04)`;
            rafId = null;
          });
        }
      };

      const onMouseLeave = () => {
        if (rafId) {
          cancelAnimationFrame(rafId);
          rafId = null;
        }
        bounds = null;
        tiltWrap.style.transform = "perspective(800px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)";
      };

      card.addEventListener("mouseenter", onMouseEnter, { passive: true });
      card.addEventListener("mousemove", onMouseMove, { passive: true });
      card.addEventListener("mouseleave", onMouseLeave, { passive: true });
    });
  }

  // ============================================================
  // 7. FEATURED PRODUCTS: DATA CATALOG, ENTRANCE & ADD TO CART
  // ============================================================
  const FEATURED_PRODUCTS = [
    {
      id: "herbs-aloe-vera",
      name: "Herbs Aloe Vera",
      categoryTag: "Digestion & Liver",
      price: 990,
      priceFormatted: "Rs 990",
      spec: "500mg × 60 Caps",
      benefit: "Maintains liver health, improves digestion",
      image: "/static/Medicine/Herbs Aloe Vera.png",
      alt: "Herbs Aloe Vera capsules for liver health and digestion"
    },
    {
      id: "herbs-glucosamine",
      name: "Herbs Glucosamine",
      subtitle: "(Joint Care)",
      categoryTag: "Joint Care",
      price: 1490,
      priceFormatted: "Rs 1,490",
      spec: "500mg × 90 Caps",
      benefit: "Reduces joint pain, strengthens bones",
      image: "/static/Medicine/Herbs Glucosamine.jpeg",
      alt: "Herbs Glucosamine Joint Care capsules"
    },
    {
      id: "herbs-ginkgo-biloba",
      name: "Herbs Ginkgo Biloba",
      subtitle: "(Antioxidant)",
      categoryTag: "Brain & Memory",
      price: 2150,
      priceFormatted: "Rs 2,150",
      spec: "500mg × 90 Caps",
      benefit: "Protects brain health, fights depression/migraine",
      image: "/static/Medicine/Herbs Gingko Biloba.png",
      alt: "Herbs Ginkgo Biloba antioxidant capsules"
    },
    {
      id: "herbs-green-coffee-beans",
      name: "Herbs Green Coffee Beans",
      categoryTag: "Weight Care",
      price: 3200,
      priceFormatted: "Rs 3,200",
      spec: "500mg × 90 Caps",
      benefit: "Weight care, cuts body fat",
      image: "/static/Medicine/Herbs Green Coffee Beans.png",
      alt: "Herbs Green Coffee Beans weight care supplement"
    },
    {
      id: "herbs-green-tea",
      name: "Herbs Green Tea",
      categoryTag: "Beverages & Tea",
      price: 540,
      priceFormatted: "Rs 540",
      spec: "2.5g × 50 Bags",
      benefit: "Cleanses blood, aids digestion",
      image: "/static/Medicine/Herbs Green Tea.jpeg",
      alt: "Herbs Green Tea antioxidant tea bags"
    },
    {
      id: "herbs-black-coffee",
      name: "Herbs Black Coffee",
      categoryTag: "Vitality & Energy",
      price: 1000,
      priceFormatted: "Rs 1,000",
      spec: "4.5g × 20 Sachets",
      benefit: "Relieves stress, fights fatigue",
      image: "/static/Medicine/Herbs Black Coffee.jpeg",
      alt: "Herbs Black Coffee herbal vitality sachets"
    },
    {
      id: "herbs-toothpaste",
      name: "Herbs Toothpaste",
      categoryTag: "Oral Care",
      price: 170,
      priceFormatted: "Rs 170",
      spec: "50g",
      benefit: "Protects teeth, cures bad breath",
      image: "/static/Medicine/Herbs Toothpaste 50 Gm.png",
      alt: "Herbs Toothpaste natural herbal oral care"
    },
    {
      id: "herbs-massage-oil",
      name: "Herbs Massage Oil",
      categoryTag: "Body Ritual",
      price: 440,
      priceFormatted: "Rs 440",
      spec: "100ml",
      benefit: "Reduces joint/muscle pain",
      image: "/static/Medicine/Herbs Massage Oil.jpeg",
      alt: "Herbs Massage Oil joint and muscle pain relief"
    }
  ];

  // Expose to window for client extensibility / runtime inspection
  window.FEATURED_PRODUCTS = FEATURED_PRODUCTS;

  // 7a. Synchronized Scroll Reveal (Group Entrance)
  const featuredProductsGrid = document.getElementById("featured-products-grid");
  if (featuredProductsGrid) {
    if (prefersReducedMotion || !("IntersectionObserver" in window)) {
      featuredProductsGrid.classList.add("is-visible");
    } else {
      const productsObserver = new IntersectionObserver(
        (entries, observer) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              featuredProductsGrid.classList.add("is-visible");
              observer.unobserve(entry.target); // Trigger ONCE
            }
          });
        },
        {
          threshold: 0.1,
          rootMargin: "0px 0px -30px 0px",
        }
      );
      productsObserver.observe(featuredProductsGrid);
    }
  }

  // 7b. "Add to Cart" Micro-interaction & Cart Badge Increment
  let cartCount = 0;
  const cartBadges = document.querySelectorAll(".cart-badge, .cart-badge-drawer");

  const getCsrfToken = () => {
    let cookieValue = "";
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, 10) === "csrftoken=") {
          cookieValue = decodeURIComponent(cookie.substring(10));
          break;
        }
      }
    }
    return cookieValue;
  };

  const updateCartCount = (count) => {
    cartCount = count;
    cartBadges.forEach((badge) => {
      badge.textContent = cartCount;
      badge.classList.remove("is-popping");
      void badge.offsetWidth; // Trigger reflow for CSS keyframe restart
      badge.classList.add("is-popping");
    });
  };

  const setupAddToCartButtons = () => {
    const addButtons = document.querySelectorAll(".field-wax-seal, .specimen-wax-seal, .apothecary-add-btn, .product-add-btn");

    // Initialize cartCount from rendered DOM badge
    const initialBadge = document.querySelector(".cart-badge");
    if (initialBadge) {
      const parsed = parseInt(initialBadge.textContent.trim(), 10);
      if (!isNaN(parsed)) cartCount = parsed;
    }

    addButtons.forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        if (btn.classList.contains("is-added")) return;

        const card = btn.closest(".apothecary-card, .specimen-card, .field-card, .product-card");
        const prodId = btn.getAttribute("data-product-id") || 
                       btn.getAttribute("data-product-slug") || 
                       (card ? card.getAttribute("data-product-id") : null);

        // Quick wax-seal press animation
        btn.classList.add("is-pressed");
        setTimeout(() => {
          btn.classList.remove("is-pressed");
        }, 280);

        // Button morphs to show "Added ✓" state / checkmark glyph
        btn.classList.add("is-added");

        if (prodId) {
          fetch("/cart/add/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCsrfToken(),
              "X-Requested-With": "XMLHttpRequest"
            },
            body: JSON.stringify({ product_id: prodId, quantity: 1 })
          })
          .then((res) => res.json())
          .then((data) => {
            if (data.status === "success" && typeof data.cart_count !== "undefined") {
              updateCartCount(data.cart_count);
            } else {
              updateCartCount(cartCount + 1);
            }
          })
          .catch(() => {
            updateCartCount(cartCount + 1);
          });
        } else {
          updateCartCount(cartCount + 1);
        }

        // Revert quietly after ~1.2s
        setTimeout(() => {
          btn.classList.remove("is-added");
        }, 1200);
      });
    });
  };

  setupAddToCartButtons();

  // 7c. Accessible Keyboard Navigation for Specimen, Field & Product Cards
  const productCards = document.querySelectorAll(".field-card, .specimen-card, .apothecary-card, .product-card");
  productCards.forEach((card) => {
    card.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && e.target === card) {
        const addBtn = card.querySelector(".field-wax-seal, .specimen-wax-seal, .apothecary-add-btn, .product-add-btn");
        if (addBtn) addBtn.click();
      }
    });
  });

  // 8. Site-wide Language Switcher (ENG / नेपाली)
  const setSiteLanguage = (lang) => {
    document.documentElement.setAttribute("data-lang", lang);
    document.querySelectorAll(".nav-lang-btn").forEach((btn) => {
      if (btn.getAttribute("data-lang") === lang) {
        btn.classList.add("is-active");
        btn.setAttribute("aria-pressed", "true");
      } else {
        btn.classList.remove("is-active");
        btn.setAttribute("aria-pressed", "false");
      }
    });

    const isNep = lang === "nep";
    document.querySelectorAll(".say-quote-eng").forEach((el) => {
      el.style.display = isNep ? "none" : "inline";
    });
    document.querySelectorAll(".say-quote-nep").forEach((el) => {
      el.style.display = isNep ? "inline" : "none";
    });
    document.querySelectorAll(".lang-eng").forEach((el) => {
      el.style.display = isNep ? "none" : "";
    });
    document.querySelectorAll(".lang-nep").forEach((el) => {
      el.style.display = isNep ? "" : "none";
    });

    try {
      localStorage.setItem("site_lang", lang);
    } catch (e) {}

    window.dispatchEvent(new CustomEvent("siteLanguageChange", { detail: { lang: lang } }));
  };

  document.querySelectorAll(".nav-lang-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const lang = btn.getAttribute("data-lang") || "eng";
      setSiteLanguage(lang);
    });
  });

  // Initialize with saved preference or default to 'eng'
  const savedSiteLang = localStorage.getItem("site_lang") || "eng";
  setSiteLanguage(savedSiteLang);

  // 9. Client Item Ratings & Continuous Non-Stop Ticker Showcase
  const initClientRatingsSystem = () => {
    const sliderTrack = document.getElementById("ratings-slider-track");
    const sliderViewport = document.getElementById("ratings-slider-viewport");
    const prevBtn = document.getElementById("ratings-slider-prev");
    const nextBtn = document.getElementById("ratings-slider-next");

    if (!sliderTrack || !sliderViewport) return;

    let currentOffset = 0;
    let isPaused = false;
    let singleSetWidth = 0;
    let cardStep = 0;
    let rafId = null;
    let lastTime = null;
    // Brisk & lively steady reading speed: 72 pixels per second
    const speedPixelsPerSec = 72;

    // 1. Setup Seamless Clones (duplicate the set so it streams continuously with 0 gap/glitch)
    const setupSeamlessClones = () => {
      // Remove existing clones if any
      sliderTrack.querySelectorAll(".is-clone").forEach((el) => el.remove());

      const originalCards = Array.from(sliderTrack.querySelectorAll(".item-rating-slide-card:not(.is-clone)"));
      if (originalCards.length === 0) return;

      // Duplicate cards to guarantee infinite stream
      originalCards.forEach((card) => {
        const clone = card.cloneNode(true);
        clone.classList.add("is-clone");
        clone.setAttribute("aria-hidden", "true");
        sliderTrack.appendChild(clone);
      });
    };

    // 2. Measure dimensions accurately on load and resize
    const updateDimensions = () => {
      const viewportWidth = sliderViewport.clientWidth || window.innerWidth;
      let cardsPerView = 3;
      if (window.innerWidth <= 640) cardsPerView = 1;
      else if (window.innerWidth <= 992) cardsPerView = 2;

      const gap = 24;
      const totalGaps = (cardsPerView - 1) * gap;
      const cardWidth = Math.max(260, Math.floor((viewportWidth - totalGaps) / cardsPerView));

      sliderTrack.style.setProperty("--card-width", `${cardWidth}px`);

      const originalCards = sliderTrack.querySelectorAll(".item-rating-slide-card:not(.is-clone)");
      cardStep = cardWidth + gap;
      singleSetWidth = originalCards.length * cardStep;
    };

    // 3. Continuous Non-Stop Animation Loop (from Right to Left)
    const startTicker = () => {
      if (rafId) cancelAnimationFrame(rafId);
      lastTime = null;

      const animate = (timestamp) => {
        if (lastTime === null) lastTime = timestamp;
        const elapsed = Math.min(64, timestamp - lastTime); // clamp delta
        lastTime = timestamp;

        if (!isPaused && singleSetWidth > 0) {
          // Continuous smooth stream strictly from Right to Left:
          currentOffset += (speedPixelsPerSec * (elapsed / 1000));

          // Infinite Seamless Wrap
          if (currentOffset >= singleSetWidth) {
            currentOffset -= singleSetWidth;
          } else if (currentOffset < 0) {
            currentOffset += singleSetWidth;
          }

          sliderTrack.style.transform = `translate3d(-${currentOffset.toFixed(2)}px, 0, 0)`;
        }

        rafId = requestAnimationFrame(animate);
      };

      rafId = requestAnimationFrame(animate);
    };

    // 4. Hover Pause strictly on rating item cards: Stop when mouse cursor is on item
    const bindItemHoverListeners = () => {
      const allCards = sliderTrack.querySelectorAll(".item-rating-slide-card");
      allCards.forEach((card) => {
        if (card.dataset.hoverBound) return;
        card.dataset.hoverBound = "true";

        card.addEventListener("mouseenter", () => {
          isPaused = true;
        });

        card.addEventListener("mouseleave", () => {
          isPaused = false;
        });
      });
    };

    // 5. Manual Controls: Prev (<) and Next (>) buttons
    if (prevBtn) {
      prevBtn.addEventListener("mouseenter", () => { isPaused = true; });
      prevBtn.addEventListener("mouseleave", () => { isPaused = false; });
      prevBtn.addEventListener("click", () => {
        currentOffset -= (cardStep || 380);
        if (currentOffset < 0) currentOffset += singleSetWidth;
        sliderTrack.style.transform = `translate3d(-${currentOffset.toFixed(2)}px, 0, 0)`;
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("mouseenter", () => { isPaused = true; });
      nextBtn.addEventListener("mouseleave", () => { isPaused = false; });
      nextBtn.addEventListener("click", () => {
        currentOffset += (cardStep || 380);
        if (currentOffset >= singleSetWidth) currentOffset -= singleSetWidth;
        sliderTrack.style.transform = `translate3d(-${currentOffset.toFixed(2)}px, 0, 0)`;
      });
    }

    // 6. Touch Drag / Swipe for Mobile
    let touchStartX = 0;
    let touchInitialOffset = 0;

    sliderViewport.addEventListener("touchstart", (e) => {
      isPaused = true;
      touchStartX = e.touches[0].clientX;
      touchInitialOffset = currentOffset;
    }, { passive: true });

    sliderViewport.addEventListener("touchmove", (e) => {
      const diff = touchStartX - e.touches[0].clientX;
      let temp = touchInitialOffset + diff;
      if (temp >= singleSetWidth) temp -= singleSetWidth;
      else if (temp < 0) temp += singleSetWidth;
      currentOffset = temp;
      sliderTrack.style.transform = `translate3d(-${currentOffset.toFixed(2)}px, 0, 0)`;
    }, { passive: true });

    sliderViewport.addEventListener("touchend", () => {
      isPaused = false;
      lastTime = null;
    }, { passive: true });

    window.addEventListener("resize", () => {
      updateDimensions();
    });

    window.addEventListener("load", () => {
      updateDimensions();
    });

    document.addEventListener("visibilitychange", () => {
      if (document.hidden) {
        isPaused = true;
      } else {
        lastTime = null;
        isPaused = false;
      }
    });

    window.addEventListener("blur", () => {
      isPaused = false;
      lastTime = null;
    });

    setupSeamlessClones();
    updateDimensions();
    bindItemHoverListeners();
    startTicker();

    // Ensure any legacy localStorage cached mock reviews are wiped
    try {
      localStorage.removeItem("client_homepage_reviews");
    } catch (e) {}
  };

  initClientRatingsSystem();

  // Apothecary Footer Provenance Clock & Ascend Action
  const initApothecaryFooter = () => {
    // 1. Kathmandu Live Provenance Clock (UTC+5:45)
    const clockEl = document.getElementById("footer-kathmandu-clock");
    if (clockEl) {
      const updateClock = () => {
        const now = new Date();
        const utcMs = now.getTime() + (now.getTimezoneOffset() * 60000);
        // Nepal is UTC+5 hours 45 mins (+5.75 hours)
        const nptDate = new Date(utcMs + (5.75 * 3600000));
        let hours = nptDate.getHours();
        const mins = String(nptDate.getMinutes()).padStart(2, "0");
        const ampm = hours >= 12 ? "PM" : "AM";
        hours = hours % 12 || 12;
        clockEl.textContent = `${hours}:${mins} ${ampm} NPT`;
      };
      updateClock();
      setInterval(updateClock, 30000);
    }

    // 2. Back-to-Hero Section Upper Arrow Action
    const ascendBtn = document.getElementById("footer-ascend-btn");
    if (ascendBtn) {
      ascendBtn.addEventListener("click", () => {
        const heroSection = document.getElementById("hero");
        if (heroSection) {
          heroSection.scrollIntoView({ behavior: "smooth", block: "start" });
        } else {
          window.scrollTo({
            top: 0,
            behavior: "smooth"
          });
        }
      });
    }
  };

  // 3D Theatre Cinema Screen Tilt Interaction
  const init3DTheatreTilt = () => {
    const stage = document.getElementById("theatre-screen-stage");
    const bezel = document.getElementById("theatre-screen-bezel");
    if (!stage || !bezel) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    let rafId = null;

    stage.addEventListener("mousemove", (e) => {
      if (rafId) cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(() => {
        const rect = stage.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;

        // Subtle 3D cinema tilt
        const rotX = 2.8 - (y * 5.5);
        const rotY = x * 6.5;

        bezel.style.transform = `perspective(1400px) rotateX(${rotX.toFixed(2)}deg) rotateY(${rotY.toFixed(2)}deg) scale(0.99)`;
      });
    });

    stage.addEventListener("mouseleave", () => {
      if (rafId) cancelAnimationFrame(rafId);
      bezel.style.transform = "perspective(1400px) rotateX(2.8deg) rotateY(0deg) scale(0.985)";
    });
  };

  init3DTheatreTilt();

  initApothecaryFooter();

  // Nav Account Dropdown Interaction (Smooth hover bridge & click handler)
  const initNavAccountDropdown = () => {
    const accountWraps = document.querySelectorAll(".nav-user-account-wrap");
    accountWraps.forEach((wrap) => {
      const btn = wrap.querySelector(".nav-account-btn");
      const dropdown = wrap.querySelector(".nav-account-dropdown");
      if (!dropdown) return;

      let closeTimer = null;

      const showDropdown = () => {
        if (closeTimer) {
          clearTimeout(closeTimer);
          closeTimer = null;
        }
        wrap.classList.add("is-active");
        if (btn) btn.setAttribute("aria-expanded", "true");
      };

      const hideDropdown = (delay = 250) => {
        if (closeTimer) clearTimeout(closeTimer);
        closeTimer = setTimeout(() => {
          wrap.classList.remove("is-active");
          if (btn) btn.setAttribute("aria-expanded", "false");
        }, delay);
      };

      wrap.addEventListener("mouseenter", showDropdown);
      wrap.addEventListener("mouseleave", () => hideDropdown(250));

      if (btn) {
        btn.addEventListener("click", (e) => {
          // If on touch device or toggling open
          if (window.matchMedia("(pointer: coarse)").matches || !wrap.classList.contains("is-active")) {
            e.preventDefault();
            if (wrap.classList.contains("is-active")) {
              hideDropdown(0);
            } else {
              showDropdown();
            }
          }
        });
      }
    });

    // Close when clicking outside
    document.addEventListener("click", (e) => {
      if (!e.target.closest(".nav-user-account-wrap")) {
        document.querySelectorAll(".nav-user-account-wrap.is-active").forEach((w) => {
          w.classList.remove("is-active");
          const b = w.querySelector(".nav-account-btn");
          if (b) b.setAttribute("aria-expanded", "false");
        });
      }
    });

    // Close when Escape key is pressed
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        document.querySelectorAll(".nav-user-account-wrap.is-active").forEach((w) => {
          w.classList.remove("is-active");
          const b = w.querySelector(".nav-account-btn");
          if (b) b.setAttribute("aria-expanded", "false");
        });
      }
    });
  };

  initNavAccountDropdown();
});


