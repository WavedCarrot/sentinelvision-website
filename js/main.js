/* ═══════════════════════════════════════════════════════════
   SentinelVision Pro — Website JavaScript
   ═══════════════════════════════════════════════════════════ */

// ── Navbar scroll effect ─────────────────────────────────
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 40);
  }, { passive: true });
}

// ── Mobile hamburger menu ─────────────────────────────────
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('nav-links');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = navLinks.classList.toggle('open');
    hamburger.classList.toggle('open', isOpen);
    hamburger.setAttribute('aria-expanded', String(isOpen));
  });
  // Close menu when a link is clicked
  navLinks.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      navLinks.classList.remove('open');
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    });
  });
  // Close on tap outside
  document.addEventListener('click', (e) => {
    if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
      navLinks.classList.remove('open');
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    }
  });
}

// ── Active nav link highlight ─────────────────────
(function() {
  const page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(function(a) {
    const href = (a.getAttribute('href') || '').split('?')[0];
    if (href === page) a.classList.add('nav-active');
  });
})();

// ── FAQ accordion ────────────────────────────────────────
document.querySelectorAll('.faq-question').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq-item');
    const isOpen = item.classList.contains('open');
    // Close all
    document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
    // Toggle clicked
    if (!isOpen) item.classList.add('open');
  });
});

// ── Pricing page: duration toggle ────────────────────────
// Prices per duration index (0=1mo, 1=3mo, 2=12mo)
const INDIVIDUAL_TOTALS = [700, 1950, 6000]; // sum of all 5 individual features (zone+loitering, weapon, people, vehicle, object)
const BUNDLE_PRICES     = [500, 1400, 4500];
const BUNDLE_SAVINGS    = INDIVIDUAL_TOTALS.map((t, i) => t - BUNDLE_PRICES[i]); // [100, 250, 600]
const DUR_LABELS        = ['1 month', '3 months', '12 months'];

let activeDurIndex = 0;

function updatePricingCards(durIndex) {
  activeDurIndex = durIndex;

  document.querySelectorAll('.price-amount[data-prices]').forEach(el => {
    const prices = el.dataset.prices.split(',').map(Number);
    el.querySelector('.amount').textContent = prices[durIndex].toLocaleString('en-ZA');
    // Update /per label
    const per = el.querySelector('.per');
    if (per) per.textContent = durIndex === 0 ? '/month' : `/${DUR_LABELS[durIndex]}`;
  });

  // Update bundle saving message
  const savingEl = document.getElementById('bundle-saving');
  if (savingEl) {
    const saved = BUNDLE_SAVINGS[durIndex];
    savingEl.textContent =
      durIndex === 0
        ? `Save R${saved}/month vs buying individually`
        : `Save R${saved.toLocaleString('en-ZA')} vs buying individually`;
  }
}

document.querySelectorAll('.dur-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.dur-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    updatePricingCards(parseInt(btn.dataset.dur, 10));
  });
});

// ── Order form: price calculator ─────────────────────────
const PRICES = {
  'Zone Detection &amp; Loitering — R150/month':                [150,  400, 1200],
  'Weapon Detection — R200/month':                      [200,  550, 1800],
  'People Counting &amp; Analytics — R150/month':       [150,  400, 1200],
  'Vehicle Detection — R100/month':                     [100,  300,  900],
  'Object Detection — R100/month':                      [100,  300,  900],
  'Full Feature Bundle — R500/month':                   [500, 1400, 4500],
};

const LICENSE_NAMES = {
  'Zone Detection &amp; Loitering — R150/month':                'Zone Detection &amp; Loitering',
  'Weapon Detection — R200/month':                  'Weapon Detection (Beta)',
  'People Counting &amp; Analytics — R150/month':  'People Counting & Analytics',
  'Vehicle Detection — R100/month':                 'Vehicle Detection',
  'Object Detection — R100/month':                  'Object Detection',
  'Full Feature Bundle — R500/month':               'Full Feature Bundle',
};

const DUR_INDEX = { '1 month': 0, '3 months': 1, '12 months': 2 };

function updateOrderPrice() {
  const licenseSelect = document.getElementById('o-license');
  const pdAmount      = document.getElementById('pd-amount');
  const pdName        = document.getElementById('pd-name');
  const hiddenPrice   = document.getElementById('hidden-price');
  const hiddenSummary = document.getElementById('hidden-summary');
  if (!licenseSelect || !pdAmount) return;

  const licVal  = licenseSelect.value;
  const durEl   = document.querySelector('input[name="duration"]:checked');
  const durVal  = durEl ? durEl.value : '1 month';
  const durIdx  = DUR_INDEX[durVal] ?? 0;
  const priceArr = PRICES[licVal];

  if (!priceArr || !licVal) {
    pdAmount.innerHTML = '<span class="pd-none">Select license &amp; duration</span>';
    pdName.textContent = '';
    if (hiddenPrice)   hiddenPrice.value = '';
    if (hiddenSummary) hiddenSummary.value = '';
    return;
  }

  const price    = priceArr[durIdx];
  const name     = LICENSE_NAMES[licVal] || licVal;
  const summary  = `${name} — ${durVal} — R${price.toLocaleString('en-ZA')}`;

  pdAmount.innerHTML = `<span style="font-size:2.8rem;font-weight:900">R${price.toLocaleString('en-ZA')}</span>`;
  pdName.textContent = `${name} / ${durVal}`;
  if (hiddenPrice)   hiddenPrice.value   = `R${price.toLocaleString('en-ZA')}`;
  if (hiddenSummary) hiddenSummary.value = summary;
}

const licenseSelect = document.getElementById('o-license');
if (licenseSelect) {
  licenseSelect.addEventListener('change', updateOrderPrice);
  // Pre-select from URL param: ?license=full_bundle
  const urlParam = new URLSearchParams(window.location.search).get('license');
  if (urlParam) {
    const map = {
      'zone_detection':     'Zone Detection &amp; Loitering — R150/month',
      'loitering_detection':'Zone Detection &amp; Loitering — R150/month',
      'weapon_detection':   'Weapon Detection — R200/month',
      'people_counting':    'People Counting &amp; Analytics — R150/month',
      'vehicle_detection':  'Vehicle Detection — R100/month',
      'object_detection':   'Object Detection — R100/month',
      'full_bundle':        'Full Feature Bundle — R500/month',
    };
    if (map[urlParam]) {
      licenseSelect.value = map[urlParam];
      updateOrderPrice();
    }
  }
}

document.querySelectorAll('input[name="duration"]').forEach(radio => {
  radio.addEventListener('change', updateOrderPrice);
});

// ── Toast notification ────────────────────────────────
let _toastEl = null, _toastTimer = null;
function showWebToast(msg, type) {
  if (!_toastEl) {
    _toastEl = document.createElement('div');
    _toastEl.className = 'web-toast';
    _toastEl.innerHTML = '<span class="web-toast-icon"></span><span class="web-toast-msg" style="flex:1"></span>';
    document.body.appendChild(_toastEl);
  }
  if (_toastTimer) clearTimeout(_toastTimer);
  _toastEl.className = 'web-toast toast-' + (type || 'success');
  _toastEl.querySelector('.web-toast-icon').innerHTML = type === 'error'
    ? '<i class="fas fa-exclamation-circle"></i>'
    : '<i class="fas fa-check-circle"></i>';
  _toastEl.querySelector('.web-toast-msg').textContent = msg;
  requestAnimationFrame(() => requestAnimationFrame(() => _toastEl.classList.add('show')));
  _toastTimer = setTimeout(() => _toastEl.classList.remove('show'), 4500);
}

// ── Web3Forms AJAX submission ─────────────────────────────
function setupForm(formId, resultId, submitId) {
  const form   = document.getElementById(formId);
  const result = document.getElementById(resultId);
  const submit = document.getElementById(submitId);
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Honeypot check — silently discard bot submissions
    const hp = form.querySelector('input[name="website_url"]');
    if (hp && hp.value.trim() !== '') return;

    if (submit) {
      submit.disabled = true;
      submit.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    }

    try {
      const data     = new FormData(form);
      const response = await fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        body: data,
      });
      const json = await response.json();

      if (json.success) {
        result.className = 'form-result success';
        if (formId === 'order-form') {
          result.innerHTML =
            '<i class="fas fa-check-circle"></i> <strong>Order received!</strong> ' +
            'We will email you payment details shortly. Please check your inbox.';
          showWebToast('Order received! Check your inbox for payment details.', 'success');
        } else {
          result.innerHTML =
            '<i class="fas fa-check-circle"></i> <strong>Message sent!</strong> ' +
            'We\'ll get back to you soon.';
          showWebToast('Message sent! We\'ll get back to you soon.', 'success');
        }
        form.reset();
        if (formId === 'order-form') {
          const pdAmount = document.getElementById('pd-amount');
          const pdName   = document.getElementById('pd-name');
          if (pdAmount) pdAmount.innerHTML = '<span class="pd-none">Select license &amp; duration</span>';
          if (pdName)   pdName.textContent = '';
        }
      } else {
        throw new Error(json.message || 'Submission failed');
      }
    } catch (err) {
      result.className = 'form-result error';
      result.innerHTML =
        '<i class="fas fa-exclamation-circle"></i> Something went wrong. ' +
        'Please email us directly at <a href="mailto:info.sentinelvision@gmail.com">info.sentinelvision@gmail.com</a>';
      showWebToast('Something went wrong. Please try again.', 'error');
    } finally {
      if (submit) {
        submit.disabled = false;
        submit.innerHTML = formId === 'order-form'
          ? '<i class="fas fa-paper-plane"></i> Submit Order'
          : '<i class="fas fa-paper-plane"></i> Send Message';
      }
    }
  });
}

setupForm('order-form',    'order-result',    'o-submit');
setupForm('contact-form',  'contact-result',  'c-submit');
setupForm('quote-form',    'quote-result');
setupForm('update-form',   'update-result');
setupForm('download-form', 'download-result');

// ── Reviews ───────────────────────────────────────────────
const SEED_REVIEWS = [];

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function starsHtml(rating) {
  let html = '';
  for (let i = 1; i <= 5; i++) {
    if (i <= Math.floor(rating)) html += '<i class="fas fa-star"></i>';
    else if (i === Math.ceil(rating) && rating % 1 >= 0.5) html += '<i class="fas fa-star-half-alt"></i>';
    else html += '<i class="far fa-star"></i>';
  }
  return html;
}

function renderReviews() {
  const grid = document.getElementById('reviews-grid');
  if (!grid) return;
  const stored = JSON.parse(localStorage.getItem('sv_reviews') || '[]');
  const all = [...SEED_REVIEWS, ...stored];
  if (all.length === 0) {
    grid.innerHTML = '<p class="reviews-empty">No reviews yet — be the first to share your experience!</p>';
    return;
  }
  grid.innerHTML = all.map(r => `
    <div class="testimonial-card${r.seed ? '' : ' review-new'}">
      <div class="testimonial-stars">${starsHtml(r.stars)}</div>
      <p class="testimonial-text">${escapeHtml(r.text)}</p>
      <div class="testimonial-author">
        <div class="testimonial-avatar">${escapeHtml(r.name.charAt(0).toUpperCase())}</div>
        <div>
          <div class="testimonial-name">${escapeHtml(r.name)}</div>
          ${r.role ? `<div class="testimonial-role">${escapeHtml(r.role)}</div>` : ''}
        </div>
      </div>
      ${r.seed ? '' : '<div class="review-community-badge"><i class="fas fa-check-circle"></i> Community Review</div>'}
    </div>
  `).join('');
}

function toggleReviewForm() {
  const wrap = document.getElementById('review-form-wrap');
  const btn  = document.getElementById('review-toggle-btn');
  const open = wrap.style.display === 'none';
  wrap.style.display = open ? 'block' : 'none';
  btn.innerHTML = open
    ? '<i class="fas fa-times"></i> Cancel'
    : '<i class="fas fa-pen"></i> Write a Review';
  if (open) wrap.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

document.addEventListener('DOMContentLoaded', () => {
  renderReviews();

  // ── Word-limit counters (runs on every page) ──────────────
  function countWords(str) {
    return str.trim() === '' ? 0 : str.trim().split(/\s+/).length;
  }
  document.querySelectorAll('textarea[data-wordlimit]').forEach(function(ta) {
    const limit = parseInt(ta.getAttribute('data-wordlimit'), 10);
    const counter = document.createElement('small');
    counter.className = 'word-counter';
    counter.style.cssText = 'display:block;text-align:right;margin-top:3px;font-size:0.78rem;color:var(--muted,#888);transition:color 0.2s';
    counter.textContent = '0 / ' + limit + ' words';
    ta.parentNode.insertBefore(counter, ta.nextSibling);

    // Create a persistent error element (hidden until needed)
    const err = document.createElement('small');
    err.style.cssText = 'display:none;color:#ef4444;margin-top:2px;font-size:0.78rem;';
    err.textContent = 'Please keep your message under ' + limit + ' words.';
    counter.parentNode.insertBefore(err, counter.nextSibling);

    function updateCounter() {
      const words = countWords(ta.value);
      counter.textContent = words + ' / ' + limit + ' words';
      if (words > limit) {
        counter.style.color = '#ef4444';
        ta.style.borderColor = '#ef4444';
        err.style.display = 'block';
      } else {
        counter.style.color = words >= limit * 0.9 ? '#f59e0b' : 'var(--muted,#888)';
        ta.style.borderColor = '';
        err.style.display = 'none';
      }
    }

    ta.addEventListener('input', updateCounter);

    const form = ta.closest('form');
    if (form) {
      form.addEventListener('submit', function(e) {
        if (countWords(ta.value) > limit) {
          e.preventDefault();
          e.stopImmediatePropagation();
          counter.style.color = '#ef4444';
          err.style.display = 'block';
          ta.focus();
        }
      }, true);
    }
  });

  const starInput = document.getElementById('star-input');
  if (!starInput) return;
  const starIcons = starInput.querySelectorAll('i');
  let selectedStars = 5;

  function highlightStars(n) {
    starIcons.forEach((s, i) => s.classList.toggle('active', i < n));
  }
  highlightStars(5);

  starIcons.forEach((star, idx) => {
    star.addEventListener('mouseover', () => highlightStars(idx + 1));
    star.addEventListener('mouseout',  () => highlightStars(selectedStars));
    star.addEventListener('click', () => {
      selectedStars = idx + 1;
      document.getElementById('review-rating').value = selectedStars;
      highlightStars(selectedStars);
    });
  });

  const reviewForm   = document.getElementById('review-form');
  const reviewResult = document.getElementById('review-result');
  const reviewSubmit = document.getElementById('review-submit');

  if (!reviewForm) return;

  reviewForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    reviewSubmit.disabled = true;
    reviewSubmit.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';

    const name  = reviewForm.querySelector('[name="reviewer_name"]').value.trim();
    const role  = reviewForm.querySelector('[name="reviewer_role"]').value.trim();
    const text  = reviewForm.querySelector('[name="review_text"]').value.trim();
    const stars = parseInt(document.getElementById('review-rating').value) || 5;

    // Save to localStorage so it shows immediately
    const stored = JSON.parse(localStorage.getItem('sv_reviews') || '[]');
    stored.unshift({ stars, text: `"${text}"`, name, role, seed: false });
    localStorage.setItem('sv_reviews', JSON.stringify(stored));
    renderReviews();

    // Notify owner via Web3Forms
    try {
      const data = new FormData(reviewForm);
      await fetch('https://api.web3forms.com/submit', { method: 'POST', body: data });
    } catch (_) {}

    reviewResult.className = 'form-result success';
    reviewResult.innerHTML = '<i class="fas fa-check-circle"></i> <strong>Thank you!</strong> Your review has been posted.';
    reviewForm.reset();
    highlightStars(5);
    selectedStars = 5;
    document.getElementById('review-rating').value = 5;
    reviewSubmit.disabled = false;
    reviewSubmit.innerHTML = '<i class="fas fa-paper-plane"></i> Submit Review';

    setTimeout(() => {
      document.getElementById('review-form-wrap').style.display = 'none';
      document.getElementById('review-toggle-btn').innerHTML = '<i class="fas fa-pen"></i> Write a Review';
      reviewResult.innerHTML = '';
    }, 3000);
  });
});
