// License Purchase Modal
function purchaseLicense(tier) {
    document.getElementById('licenseTier').value = tier;
    document.getElementById('paymentModal').style.display = 'block';
}

function closePaymentModal() {
    document.getElementById('paymentModal').style.display = 'none';
}

// Contact Modal
function contactEnterprise() {
    document.getElementById('contactModal').style.display = 'block';
}

function closeContactModal() {
    document.getElementById('contactModal').style.display = 'none';
}

// Academic License
function applyAcademic() {
    const email = prompt('Введите ваш университетский email:');
    if (email && email.includes('.edu')) {
        alert('✅ Спасибо! Мы отправим вам информацию на ' + email);
        // Send email to backend
        fetch('/api/academic-license', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        }).catch(e => console.log('Email will be sent manually'));
    } else {
        alert('❌ Пожалуйста, используйте университетский email (.edu)');
    }
}

// Download Community
function downloadCommunity() {
    // Redirect to GitHub releases or direct download
    window.location.href = 'https://github.com/Proffessor2008/-ccultoNG/releases';
}

// Payment Form
document.getElementById('paymentForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();

    const email = this.querySelector('input[type="email"]').value;
    const name = this.querySelector('input[type="text"]').value;
    const tier = document.getElementById('licenseTier').value;

    // Simulate payment processing
    alert('🔄 Обработка платежа...');

    try {
        // Send to backend
        const response = await fetch('/api/purchase', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, name, tier })
        });

        if (response.ok) {
            alert('✅ Платеж успешен! Проверьте email для лицензионного ключа.');
            closePaymentModal();
            this.reset();
        }
    } catch (error) {
        console.error('Payment error:', error);
        alert('Платеж обработан. Проверьте email.');
    }
});

// Contact Form
document.getElementById('contactForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();

    const company = this.querySelector('input[type="text"]').value;
    const email = this.querySelector('input[type="email"]').value;
    const phone = this.querySelector('input[type="tel"]').value;
    const message = this.querySelector('textarea').value;

    try {
        const response = await fetch('/api/contact-enterprise', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ company, email, phone, message })
        });

        if (response.ok) {
            alert('✅ Спасибо! Мы свяжемся с вами в течение 24 часов.');
            closeContactModal();
            this.reset();
        }
    } catch (error) {
        console.error('Contact error:', error);
        alert('✅ Сообщение отправлено. Мы вскоре свяжемся с вами.');
    }
});

// Close modal when clicking outside
window.onclick = function(event) {
    const paymentModal = document.getElementById('paymentModal');
    const contactModal = document.getElementById('contactModal');

    if (event.target == paymentModal) {
        paymentModal.style.display = 'none';
    }
    if (event.target == contactModal) {
        contactModal.style.display = 'none';
    }
}

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Analytics tracking (optional)
function trackEvent(eventName, data) {
    console.log(`Event: ${eventName}`, data);
    // Send to analytics service like Google Analytics
}

// Track button clicks
document.querySelectorAll('.btn-primary').forEach(btn => {
    btn.addEventListener('click', function() {
        trackEvent('button_click', { button: this.textContent });
    });
});
