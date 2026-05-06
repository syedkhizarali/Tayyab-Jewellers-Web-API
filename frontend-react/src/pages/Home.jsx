import { useEffect, useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import { FiArrowRight, FiShield, FiTruck, FiRefreshCw, FiAward, FiCheckCircle } from 'react-icons/fi';
import { FaWhatsapp } from 'react-icons/fa';
import GoldRateBanner from '../components/common/GoldRateBanner';
import ProductCard from '../components/products/ProductCard';
import { SkeletonCard } from '../components/common/LoadingSpinner';
import { getProducts } from '../api/products';

const CATEGORIES = [
  { name: 'Bridal Sets',  slug: 'bridal',    img: 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=600&q=80' },
  { name: 'Gold Rings',   slug: 'rings',      img: 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=600&q=80' },
  { name: 'Necklaces',    slug: 'necklaces',  img: 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600&q=80' },
  { name: 'Bangles',      slug: 'bangles',    img: 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600&q=80' },
  { name: 'Earrings',     slug: 'earrings',   img: 'https://images.unsplash.com/photo-1635767798638-3e25273a8236?w=600&q=80' },
  { name: 'Gemstones',    slug: 'gemstones',  img: 'https://images.unsplash.com/photo-1596944924616-7b38e7cfac36?w=600&q=80' },
];

const TESTIMONIALS = [
  { name: 'Ayesha Khan',    city: 'Lahore',    stars: 5, text: 'Absolutely stunning bridal set. The craftsmanship is beyond anything I\'ve seen in Lahore. My family was amazed at the quality.' },
  { name: 'Fatima Malik',   city: 'Karachi',   stars: 5, text: 'Ordered custom gold bangles for my daughter\'s wedding. Delivered on time and exactly as designed. Will always come back.' },
  { name: 'Sana Akhtar',    city: 'Islamabad', stars: 5, text: 'The 22K necklace I purchased is pure perfection. Hallmark certified and the weight is exact. Highly recommended.' },
  { name: 'Hira Baig',      city: 'Faisalabad',stars: 5, text: 'WhatsApp support was amazing. They helped me choose the perfect ring set within my budget. Great experience overall.' },
  { name: 'Zainab Raza',    city: 'Multan',    stars: 5, text: 'Custom earrings delivered in just 10 days. The finish is exquisite and the gold purity is exactly as promised.' },
];

const TRUST = [
  { icon: <FiAward size={22} />,     title: 'Hallmark Certified',     desc: 'Every piece comes with official hallmark certification guaranteeing gold purity.' },
  { icon: <FiShield size={22} />,    title: 'Pure Gold Guaranteed',   desc: 'We deal only in 18K, 21K, 22K, and 24K verified pure gold.' },
  { icon: <FiTruck size={22} />,     title: 'Nationwide Delivery',    desc: 'Secure, insured delivery to every corner of Pakistan.' },
  { icon: <FiRefreshCw size={22} />, title: 'Free Resize Service',    desc: 'All rings come with free lifetime resize. Your satisfaction is our promise.' },
];

function useReveal() {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) { el.classList.add('visible'); obs.disconnect(); }
    }, { threshold: 0.12 });
    obs.observe(el);
    return () => obs.disconnect();
  }, []);
  return ref;
}

function RevealSection({ children, className = '', style = {} }) {
  const ref = useReveal();
  return <div ref={ref} className={`section-reveal ${className}`} style={style}>{children}</div>;
}

export default function Home() {
  const [products, setProducts]   = useState([]);
  const [loadingP, setLoadingP]   = useState(true);
  const [activeTestimonial, setActiveTestimonial] = useState(0);
  const whatsapp = import.meta.env.VITE_WHATSAPP_NUMBER || '923000000000';

  useEffect(() => {
    getProducts({ limit: 8 })
      .then(setProducts)
      .catch(() => {})
      .finally(() => setLoadingP(false));
  }, []);

  useEffect(() => {
    const id = setInterval(() => setActiveTestimonial(p => (p + 1) % TESTIMONIALS.length), 4000);
    return () => clearInterval(id);
  }, []);

  // Generate hero particles
  const particles = Array.from({ length: 18 }, (_, i) => ({
    left: `${Math.random() * 100}%`,
    top:  `${Math.random() * 100}%`,
    dur:  `${4 + Math.random() * 5}s`,
    delay:`${Math.random() * 4}s`,
  }));

  return (
    <>
      {/* ── Hero ── */}
      <section className="hero-section">
        <div className="hero-bg" />
        <div className="hero-radial" />
        <div className="hero-particles">
          {particles.map((p, i) => (
            <div key={i} className="hero-particle" style={{ left: p.left, top: p.top, '--dur': p.dur, '--delay': p.delay }} />
          ))}
        </div>
        <div className="container">
          <div className="hero-content">
            <div className="hero-eyebrow">Est. Since 1985 — Lahore, Pakistan</div>
            <h1 className="hero-title">
              Where Gold<br /><em>Becomes Legacy</em>
            </h1>
            <p className="hero-desc">
              Handcrafted jewellery of unmatched purity. From timeless bridal sets to everyday elegance — every piece tells a story that lasts generations.
            </p>
            <div className="hero-cta">
              <Link to="/products" className="luxury-btn">
                Explore Collections <FiArrowRight size={14} />
              </Link>
              <a
                href={`https://wa.me/${whatsapp}?text=Hi, I'm interested in your jewellery collection`}
                target="_blank" rel="noreferrer"
                className="whatsapp-btn"
              >
                <FaWhatsapp size={18} /> WhatsApp Us
              </a>
            </div>
            <div className="hero-stats">
              <div>
                <span className="hero-stat-num">40+</span>
                <span className="hero-stat-label">Years of Craft</span>
              </div>
              <div>
                <span className="hero-stat-num">5K+</span>
                <span className="hero-stat-label">Happy Customers</span>
              </div>
              <div>
                <span className="hero-stat-num">500+</span>
                <span className="hero-stat-label">Unique Designs</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Trust Strip ── */}
      <div className="trust-strip">
        <div className="container">
          <div className="row g-3">
            {TRUST.map((t, i) => (
              <div key={i} className="col-6 col-md-3">
                <div className="trust-item">
                  <span className="trust-icon">{t.icon}</span>
                  <div>
                    <strong>{t.title}</strong>
                    <span style={{ display: 'none' }}>{t.desc}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── Categories ── */}
      <section style={{ padding: '48px 0 24px' }}>
        <div className="container">
          <RevealSection>
            <div className="text-center mb-4">
              <span className="section-label">Browse by Category</span>
              <h2 className="section-title">Our Collections</h2>
            </div>
          </RevealSection>
          <RevealSection>
            <div className="row g-3">
              {CATEGORIES.map((cat, i) => (
                <div key={cat.slug} className={i < 2 ? 'col-6 col-md-4' : 'col-6 col-md-2'}>
                  <Link to={`/products?category=${cat.slug}`} className="category-card">
                    <img src={cat.img} alt={cat.name} className="cat-img" loading="lazy" />
                    <div className="cat-overlay" />
                    <div className="cat-content">
                      <span className="cat-name">{cat.name}</span>
                      <span className="cat-link">View Collection →</span>
                    </div>
                  </Link>
                </div>
              ))}
            </div>
          </RevealSection>
        </div>
      </section>

      {/* ── Featured Products ── */}
      <section style={{ padding: '24px 0 48px', background: 'var(--black-soft)' }}>
        <div className="container">
          <RevealSection>
            <div className="d-flex align-items-end justify-content-between mb-4 flex-wrap gap-3">
              <div>
                <span className="section-label">Handpicked For You</span>
                <h2 className="section-title mb-0">Featured Pieces</h2>
              </div>
              <Link to="/products" className="ghost-btn">View All <FiArrowRight size={13} /></Link>
            </div>
          </RevealSection>
          <div className="product-grid">
            {loadingP
              ? [...Array(4)].map((_, i) => <SkeletonCard key={i} />)
              : products.slice(0, 8).map(p => <ProductCard key={p.id} product={p} />)
            }
          </div>
          {!loadingP && products.length === 0 && (
            <div className="empty-state">
              <p style={{ fontFamily: 'Cormorant Garamond, serif', fontSize: '1.3rem' }}>Our collection is being updated.</p>
              <p style={{ fontSize: 13 }}>Check back soon or contact us on WhatsApp.</p>
            </div>
          )}
        </div>
      </section>

      {/* ── Gold Rate Banner ── */}
      <GoldRateBanner />

      {/* ── Bridal Spotlight ── */}
      <section className="bridal-section section-pad">
        <div className="container">
          <div className="row align-items-center g-5">
            <div className="col-lg-5">
              <RevealSection>
                <div className="bridal-img-wrap">
                  <img
                    src="https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800&q=80"
                    alt="Bridal Collection"
                    className="bridal-img"
                    loading="lazy"
                  />
                </div>
              </RevealSection>
            </div>
            <div className="col-lg-7">
              <RevealSection>
                <span className="section-label">Bridal Collection</span>
                <h2 className="section-title">Make Your Wedding Day Unforgettable</h2>
                <p style={{ color: 'var(--text-muted)', fontSize: 15, fontWeight: 300, marginBottom: 28, lineHeight: 1.8 }}>
                  Our bridal jewellery sets are crafted with generations of expertise. Every bride deserves to shine in pure gold that becomes a cherished heirloom.
                </p>
                <div style={{ marginBottom: 32 }}>
                  {['Custom design from your own sketch', 'Available in 18K, 21K, 22K gold', 'Complete necklace, earring & tikka sets', 'Ready in 15–20 working days', 'Delivered across all Pakistan'].map((f, i) => (
                    <div key={i} className="bridal-feature">
                      <FiCheckCircle size={16} className="bridal-feature-icon" />
                      <span style={{ fontSize: 14, color: 'var(--text-muted)' }}>{f}</span>
                    </div>
                  ))}
                </div>
                <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
                  <Link to="/products?category=bridal" className="luxury-btn">View Bridal Sets</Link>
                  <a
                    href={`https://wa.me/${whatsapp}?text=Hi, I'm interested in bridal jewellery consultation`}
                    target="_blank" rel="noreferrer"
                    className="whatsapp-btn"
                  >
                    <FaWhatsapp size={16} /> Book Consultation
                  </a>
                </div>
              </RevealSection>
            </div>
          </div>
        </div>
      </section>

      {/* ── Testimonials ── */}
      <section className="testimonials-section section-pad">
        <div className="container">
          <RevealSection>
            <div className="text-center mb-5">
              <span className="section-label">Customer Stories</span>
              <h2 className="section-title">What Our Customers Say</h2>
            </div>
          </RevealSection>
          <RevealSection>
            <div className="row g-3">
              {TESTIMONIALS.slice(0, 3).map((t, i) => (
                <div key={i} className="col-md-4">
                  <div className="testimonial-card">
                    <div className="stars">{'★'.repeat(t.stars)}</div>
                    <p className="testimonial-text">"{t.text}"</p>
                    <div className="testimonial-author">{t.name}</div>
                    <div className="testimonial-city">{t.city}</div>
                  </div>
                </div>
              ))}
            </div>
          </RevealSection>
        </div>
      </section>

      {/* ── Custom Order CTA ── */}
      <section className="section-pad">
        <div className="container">
          <RevealSection>
            <div className="cta-section">
              <span className="section-label">Bespoke Service</span>
              <h2 className="cta-title">Have a Design in Mind?</h2>
              <p className="cta-desc">
                Bring us your sketch, photo, or idea — our master craftsmen will turn it into a one-of-a-kind piece in pure gold.
              </p>
              <div style={{ display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
                <Link to="/custom-order" className="luxury-btn">Start Custom Order</Link>
                <a
                  href={`https://wa.me/${whatsapp}?text=Hi, I have a custom jewellery design I'd like to discuss`}
                  target="_blank" rel="noreferrer"
                  className="whatsapp-btn"
                >
                  <FaWhatsapp size={16} /> Chat on WhatsApp
                </a>
              </div>
            </div>
          </RevealSection>
        </div>
      </section>
    </>
  );
}
