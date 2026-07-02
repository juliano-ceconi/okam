/* ============================================
   OKAM — Landing Page Interactivity
   Canvas background, scroll reveal, terminal typing
   ============================================ */

(function () {
    'use strict';

    // --- Particle Canvas Background ---
    const canvas = document.getElementById('bg-canvas');
    const ctx = canvas.getContext('2d');
    let particles = [];
    let animationId;

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    function createParticles() {
        const count = Math.min(Math.floor(window.innerWidth / 15), 80);
        particles = [];
        for (let i = 0; i < count; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.3,
                vy: (Math.random() - 0.5) * 0.3,
                radius: Math.random() * 1.5 + 0.5,
                opacity: Math.random() * 0.4 + 0.1
            });
        }
    }

    function drawParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw connections
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < 150) {
                    const opacity = (1 - dist / 150) * 0.08;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(88, 166, 255, ${opacity})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }

        // Draw particles
        for (const p of particles) {
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(88, 166, 255, ${p.opacity})`;
            ctx.fill();
        }

        animationId = requestAnimationFrame(drawParticles);
    }

    resizeCanvas();
    createParticles();
    drawParticles();

    window.addEventListener('resize', () => {
        resizeCanvas();
        createParticles();
    });

    // --- Mobile Nav Toggle ---
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        // Close nav on link click
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });
    }

    // --- Scroll Reveal ---
    const revealElements = document.querySelectorAll(
        '.section-label, .section-title, .section-description, ' +
        '.pain-card, .approach-comparison, .component-card, ' +
        '.terminal, .cta-title, .cta-subtitle, .cta-actions'
    );

    revealElements.forEach(el => {
        el.classList.add('reveal');
    });

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const delay = entry.target.dataset.delay || 0;
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, parseInt(delay));
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

    revealElements.forEach(el => revealObserver.observe(el));

    // --- Terminal Typing Effect ---
    const terminalSection = document.getElementById('quickstart');
    const terminalLines = document.querySelectorAll('.terminal-line');

    function typeCommand(element) {
        const text = element.dataset.text;
        if (!text) return Promise.resolve();

        return new Promise(resolve => {
            let i = 0;
            element.textContent = '';
            const interval = setInterval(() => {
                element.textContent += text[i];
                i++;
                if (i >= text.length) {
                    clearInterval(interval);
                    resolve();
                }
            }, 25);
        });
    }

    async function animateTerminal() {
        for (const line of terminalLines) {
            line.classList.add('visible');

            const cmd = line.querySelector('.terminal-command');
            if (cmd && cmd.dataset.text) {
                await typeCommand(cmd);
                await new Promise(r => setTimeout(r, 200));
            } else {
                await new Promise(r => setTimeout(r, 300));
            }
        }
    }

    let terminalAnimated = false;
    const terminalObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !terminalAnimated) {
                terminalAnimated = true;
                setTimeout(animateTerminal, 400);
                terminalObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    if (terminalSection) {
        terminalObserver.observe(terminalSection);
    }

    // --- Smooth Scroll for Nav Links ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // --- Nav Background on Scroll ---
    const nav = document.querySelector('.nav');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.style.borderBottomColor = 'rgba(99, 110, 123, 0.3)';
        } else {
            nav.style.borderBottomColor = 'rgba(99, 110, 123, 0.15)';
        }
    });

})();
