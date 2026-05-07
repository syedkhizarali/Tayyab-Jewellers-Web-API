import { useState, useEffect, useRef, useContext } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import {
  FiSearch, FiShoppingBag, FiHeart, FiUser, FiMenu, FiX,
  FiLogOut, FiPackage, FiMapPin, FiSettings, FiChevronDown, FiPhone,
} from 'react-icons/fi';
import { AuthContext }    from '../../context/AuthContext';
import { CartContext }    from '../../context/CartContext';
import { WishlistContext } from '../../context/WishlistContext';
import { getLatestRates } from '../../api/rates';

/* ── colour tokens ── */
const G       = '#C9A84C';
const GD      = '#8B6914';
const BG      = '#0A0A0A';
const CR      = '#F0EAD6';
const MU      = '#9A8866';
const BG_CARD = '#1A1A1A';
const BORDER  = 'rgba(201,168,76,0.18)';

/* ── Diamond gem SVG logo ── */
function DiamondLogo({ size = 46 }) {
  const c  = '#C9A84C';
  const h  = Math.round(size * 1.02);
  return (
    <svg width={size} height={h} viewBox="0 0 100 102" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Outer diamond */}
      <path d="M50 3 L97 50 L50 99 L3 50 Z" stroke={c} strokeWidth="1.9" strokeLinejoin="round"/>

      {/* Girdle / equator line */}
      <line x1="3" y1="50" x2="97" y2="50" stroke={c} strokeWidth="1.4"/>

      {/* Crown upper table */}
      <line x1="27" y1="26" x2="73" y2="26" stroke={c} strokeWidth="0.9"/>

      {/* Crown star facets */}
      <line x1="50" y1="3"  x2="27" y2="26" stroke={c} strokeWidth="0.85"/>
      <line x1="50" y1="3"  x2="73" y2="26" stroke={c} strokeWidth="0.85"/>
      <line x1="50" y1="3"  x2="50" y2="26" stroke={c} strokeWidth="0.75"/>
      <line x1="27" y1="26" x2="3"  y2="50" stroke={c} strokeWidth="0.8"/>
      <line x1="73" y1="26" x2="97" y2="50" stroke={c} strokeWidth="0.8"/>
      <line x1="27" y1="26" x2="50" y2="50" stroke={c} strokeWidth="0.7"/>
      <line x1="73" y1="26" x2="50" y2="50" stroke={c} strokeWidth="0.7"/>
      <line x1="50" y1="26" x2="27" y2="50" stroke={c} strokeWidth="0.6"/>
      <line x1="50" y1="26" x2="73" y2="50" stroke={c} strokeWidth="0.6"/>

      {/* Pavilion lower facet lines */}
      <line x1="27" y1="50" x2="50" y2="99" stroke={c} strokeWidth="0.75"/>
      <line x1="73" y1="50" x2="50" y2="99" stroke={c} strokeWidth="0.75"/>

      {/* ── Tulip / flower decoration ── */}
      {/* Vertical stem */}
      <line x1="50" y1="54" x2="50" y2="91" stroke={c} strokeWidth="1.2"/>

      {/* Centre upward bud */}
      <path
        d="M50,54 C47,54 42,58 45,63 C47,67 50,70 50,70 C50,70 53,67 55,63 C58,58 53,54 50,54Z"
        stroke={c} strokeWidth="1.05" fill="none"
      />

      {/* Left petal */}
      <path
        d="M50,70 C44,66 36,66 33,72 C30,78 38,84 50,79"
        stroke={c} strokeWidth="1.05" fill="none" strokeLinecap="round"
      />

      {/* Right petal */}
      <path
        d="M50,70 C56,66 64,66 67,72 C70,78 62,84 50,79"
        stroke={c} strokeWidth="1.05" fill="none" strokeLinecap="round"
      />

      {/* Small lower leaves */}
      <path d="M50,83 C50,83 43,78 40,83" stroke={c} strokeWidth="0.85" fill="none" strokeLinecap="round"/>
      <path d="M50,83 C50,83 57,78 60,83" stroke={c} strokeWidth="0.85" fill="none" strokeLinecap="round"/>
    </svg>
  );
}

export default function Navbar() {
  const { user, logout, isAdmin } = useContext(AuthContext);
  const { cartCount, setIsOpen }  = useContext(CartContext);
  const { items: wl }             = useContext(WishlistContext);
  const navigate  = useNavigate();
  const location  = useLocation();

  const [scrolled,    setScrolled]    = useState(false);
  const [mobileOpen,  setMobileOpen]  = useState(false);
  const [searchOpen,  setSearchOpen]  = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [userDrop,    setUserDrop]    = useState(false);
  const [collectOpen, setCollectOpen] = useState(false);
  const [liveRate,    setLiveRate]    = useState(null);

  const searchRef  = useRef(null);
  const userRef    = useRef(null);
  const collectRef = useRef(null);

  const phone        = import.meta.env.VITE_PHONE_NUMBER    || '+923154844005';
  const phoneDisplay = import.meta.env.VITE_PHONE_DISPLAY   || '+92 315 484 4005';

  useEffect(() => {
    const fn = () => setScrolled(window.scrollY > 40);
    window.addEventListener('scroll', fn, { passive: true });
    return () => window.removeEventListener('scroll', fn);
  }, []);

  useEffect(() => {
    setMobileOpen(false); setUserDrop(false); setCollectOpen(false);
  }, [location.pathname]);

  useEffect(() => {
    const fetch = async () => {
      try {
        const rates = await getLatestRates();
        const r = rates.find(x => x.karat === 22) || rates[0];
        if (r) setLiveRate(r.price_per_tola);
      } catch { /* silent */ }
    };
    fetch();
    const id = setInterval(fetch, 5 * 60 * 1000);
    return () => clearInterval(id);
  }, []);

  useEffect(() => { if (searchOpen && searchRef.current) searchRef.current.focus(); }, [searchOpen]);

  useEffect(() => {
    const fn = (e) => {
      if (userRef.current    && !userRef.current.contains(e.target))    setUserDrop(false);
      if (collectRef.current && !collectRef.current.contains(e.target)) setCollectOpen(false);
    };
    document.addEventListener('mousedown', fn);
    return () => document.removeEventListener('mousedown', fn);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/products?query=${encodeURIComponent(searchQuery.trim())}`);
      setSearchOpen(false); setSearchQuery('');
    }
  };

  const handleLogout = () => { logout(); setUserDrop(false); navigate('/'); };

  const collectLinks = [
    { label: 'Bridal Sets', to: '/products?category=bridal'    },
    { label: 'Gold Rings',  to: '/products?category=rings'     },
    { label: 'Bangles',     to: '/products?category=bangles'   },
    { label: 'Necklaces',   to: '/products?category=necklaces' },
    { label: 'Earrings',    to: '/products?category=earrings'  },
    { label: 'Tikka',       to: '/products?category=tikka'     },
  ];

  const isActive = (p) => location.pathname === p;

  return (
    <>
      {/* ── Ticker strip ── */}
      <div style={{
        background: '#111', borderBottom: `1px solid ${BORDER}`,
        padding: '7px 0', fontSize: 11, fontFamily: 'Cinzel, serif',
        letterSpacing: '0.5px', color: MU, overflow: 'hidden',
      }}>
        <div className="container">
          <div className="ticker-track">
            {[...Array(2)].map((_, i) => (
              <span key={i} style={{ display: 'flex', gap: 40, alignItems: 'center', whiteSpace: 'nowrap' }}>
                <span>22K Gold &mdash; <strong style={{ color: G }}>{liveRate ? `PKR ${Number(liveRate).toLocaleString('en-PK')}` : '—'}</strong>/tola</span>
                <span style={{ color: G }}>✦</span>
                <span>Pure Gold Guaranteed — Hallmark Certified</span>
                <span style={{ color: G }}>✦</span>
                <span>Free Resize on All Rings</span>
                <span style={{ color: G }}>✦</span>
                <span>Cash on Delivery Available Nationwide</span>
                <span style={{ color: G }}>✦</span>
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* ── Main Navbar ── */}
      <nav style={{
        background: scrolled ? 'rgba(10,10,10,0.97)' : BG,
        backdropFilter: scrolled ? 'blur(12px)' : 'none',
        WebkitBackdropFilter: scrolled ? 'blur(12px)' : 'none',
        padding: scrolled ? '10px 0' : '14px 0',
        position: 'sticky', top: 0, zIndex: 1000,
        transition: 'all 0.35s ease',
        borderBottom: `1px solid ${scrolled ? BORDER : 'rgba(201,168,76,0.06)'}`,
        boxShadow: scrolled ? '0 4px 24px rgba(0,0,0,0.6)' : 'none',
      }}>
        <div className="container">
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>

            {/* ── Logo ── */}
            <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: 10, textDecoration: 'none', flexShrink: 0, marginRight: 12 }}>
              <DiamondLogo size={44} />
              <div>
                <div style={{ fontFamily: 'Cinzel,serif', fontWeight: 700, fontSize: '1.08rem', letterSpacing: '2.5px', color: G, lineHeight: 1.15 }}>TAYYAB</div>
                <div style={{ fontFamily: 'Cinzel,serif', fontWeight: 400, fontSize: '0.68rem', letterSpacing: '3.5px', color: CR, lineHeight: 1.15 }}>JEWELLERS</div>
              </div>
            </Link>

            {/* ── Desktop nav links: Home, Collections, About Us, Contact ── */}
            <div className="nb-links">
              <NavItem label="Home"     to="/"       active={isActive('/')}      />

              {/* Collections dropdown */}
              <div ref={collectRef} style={{ position: 'relative' }}>
                <button
                  onClick={() => setCollectOpen(p => !p)}
                  style={{
                    display: 'flex', alignItems: 'center', gap: 4,
                    background: 'none', border: 'none', cursor: 'pointer',
                    fontFamily: 'Jost,sans-serif', fontSize: 13, fontWeight: 500,
                    color: collectOpen ? G : CR, padding: '7px 14px', borderRadius: 8,
                    transition: 'color 0.2s',
                  }}
                >
                  Collections
                  <FiChevronDown size={13} style={{ transition: 'transform 0.2s', transform: collectOpen ? 'rotate(180deg)' : 'none' }} />
                </button>
                {collectOpen && (
                  <div style={{
                    position: 'absolute', top: 'calc(100% + 8px)', left: 0,
                    background: BG_CARD, border: `1px solid ${BORDER}`,
                    borderRadius: 10, boxShadow: '0 8px 32px rgba(0,0,0,0.6)',
                    minWidth: 180, padding: '8px 0', zIndex: 1001,
                  }}>
                    {collectLinks.map(l => (
                      <Link key={l.to} to={l.to}
                        style={{ display: 'block', padding: '9px 18px', fontFamily: 'Jost,sans-serif', fontSize: 13, color: CR, textDecoration: 'none', transition: 'all 0.15s' }}
                        onMouseEnter={e => { e.currentTarget.style.background = 'rgba(201,168,76,0.08)'; e.currentTarget.style.color = G; }}
                        onMouseLeave={e => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = CR; }}
                      >{l.label}</Link>
                    ))}
                  </div>
                )}
              </div>

              <NavItem label="About Us" to="/about"  active={isActive('/about')} />
              <NavItem label="Contact"  to="/about"  active={false}              />

              {/* ── Phone number button ── */}
              <a
                href={`tel:${phone}`}
                style={{
                  display: 'inline-flex', alignItems: 'center', gap: 6,
                  padding: '8px 18px', borderRadius: 50,
                  background: `linear-gradient(135deg,${G},${GD})`,
                  color: BG, fontFamily: 'Jost,sans-serif', fontWeight: 700,
                  fontSize: 12, textDecoration: 'none',
                  boxShadow: `0 3px 14px rgba(201,168,76,0.35)`,
                  transition: 'all 0.25s', letterSpacing: 0.3, whiteSpace: 'nowrap',
                  marginLeft: 6,
                }}
                onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-1px)'; e.currentTarget.style.boxShadow = '0 6px 22px rgba(201,168,76,0.5)'; }}
                onMouseLeave={e => { e.currentTarget.style.transform = 'none'; e.currentTarget.style.boxShadow = '0 3px 14px rgba(201,168,76,0.35)'; }}
              >
                <FiPhone size={12} /> {phoneDisplay}
              </a>

              {/* ── Custom Order button ── */}
              <Link to="/custom-order"
                style={{
                  display: 'inline-flex', alignItems: 'center', gap: 6,
                  padding: '9px 20px', borderRadius: 50,
                  background: `linear-gradient(135deg,${G},${GD})`,
                  color: BG, fontFamily: 'Jost,sans-serif', fontWeight: 700,
                  fontSize: 12, textDecoration: 'none',
                  boxShadow: `0 3px 14px rgba(201,168,76,0.35)`,
                  transition: 'all 0.25s', letterSpacing: 0.5, whiteSpace: 'nowrap',
                  marginLeft: 4,
                }}
                onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-1px)'; e.currentTarget.style.boxShadow = '0 6px 22px rgba(201,168,76,0.5)'; }}
                onMouseLeave={e => { e.currentTarget.style.transform = 'none'; e.currentTarget.style.boxShadow = '0 3px 14px rgba(201,168,76,0.35)'; }}
              >
                Custom Order →
              </Link>
            </div>

            {/* ── Desktop right actions: Search, Cart, Profile ── */}
            <div className="nb-right">

              {/* Search */}
              <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
                {searchOpen && (
                  <form onSubmit={handleSearch}
                    style={{ position: 'absolute', right: 42, top: '50%', transform: 'translateY(-50%)', zIndex: 10 }}
                  >
                    <input
                      ref={searchRef}
                      value={searchQuery}
                      onChange={e => setSearchQuery(e.target.value)}
                      placeholder="Search jewellery…"
                      onBlur={() => { if (!searchQuery) setSearchOpen(false); }}
                      style={{
                        width: 200, padding: '7px 14px',
                        border: `1.5px solid ${G}`, borderRadius: 8,
                        fontSize: 13, fontFamily: 'Jost,sans-serif',
                        outline: 'none', background: BG_CARD, color: CR,
                      }}
                    />
                  </form>
                )}
                <IconBtn onClick={() => setSearchOpen(p => !p)}><FiSearch size={16} /></IconBtn>
              </div>

              {/* Cart */}
              <div style={{ position: 'relative' }}>
                <IconBtn onClick={() => setIsOpen(true)}>
                  <FiShoppingBag size={16} />
                  {cartCount > 0 && <Badge n={cartCount} />}
                </IconBtn>
              </div>

              {/* Wishlist (logged-in only) */}
              {user && (
                <div style={{ position: 'relative' }}>
                  <IconBtn onClick={() => navigate('/wishlist')}>
                    <FiHeart size={16} />
                    {wl.length > 0 && <Badge n={wl.length} />}
                  </IconBtn>
                </div>
              )}

              {/* Profile / Sign In */}
              {user ? (
                <div ref={userRef} style={{ position: 'relative' }}>
                  <button
                    onClick={() => setUserDrop(p => !p)}
                    style={{
                      width: 34, height: 34, borderRadius: '50%',
                      background: `linear-gradient(135deg,${G},${GD})`,
                      color: '#fff', border: 'none', cursor: 'pointer',
                      fontFamily: 'Cinzel,serif', fontWeight: 700, fontSize: 13,
                      boxShadow: `0 2px 8px rgba(201,168,76,0.35)`,
                    }}
                  >
                    {user.name?.charAt(0).toUpperCase()}
                  </button>

                  {userDrop && (
                    <div style={{
                      position: 'absolute', right: 0, top: 'calc(100% + 10px)',
                      background: BG_CARD, border: `1px solid ${BORDER}`,
                      borderRadius: 10, minWidth: 210,
                      boxShadow: '0 8px 32px rgba(0,0,0,0.6)', zIndex: 1001, overflow: 'hidden',
                    }}>
                      <div style={{ padding: '12px 16px 8px', fontFamily: 'Cinzel,serif', fontSize: 11, color: MU, borderBottom: `1px solid ${BORDER}`, letterSpacing: 1, textTransform: 'uppercase' }}>
                        {user.name}
                      </div>
                      {[
                        { to: '/profile',   icon: <FiUser size={14} />,    label: 'Profile'   },
                        { to: '/orders',    icon: <FiPackage size={14} />,  label: 'My Orders' },
                        { to: '/addresses', icon: <FiMapPin size={14} />,   label: 'Addresses' },
                      ].map(item => (
                        <Link key={item.to} to={item.to}
                          style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '9px 16px', fontSize: 13, fontFamily: 'Jost,sans-serif', color: CR, textDecoration: 'none', transition: 'all 0.15s' }}
                          onMouseEnter={e => { e.currentTarget.style.background = 'rgba(201,168,76,0.08)'; e.currentTarget.style.color = G; }}
                          onMouseLeave={e => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = CR; }}
                        >{item.icon}{item.label}</Link>
                      ))}
                      {isAdmin && (
                        <Link to="/admin"
                          style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '9px 16px', fontSize: 13, fontFamily: 'Jost,sans-serif', color: G, textDecoration: 'none', background: 'rgba(201,168,76,0.05)' }}
                          onMouseEnter={e => e.currentTarget.style.background = 'rgba(201,168,76,0.12)'}
                          onMouseLeave={e => e.currentTarget.style.background = 'rgba(201,168,76,0.05)'}
                        >
                          <FiSettings size={14} /> Admin Panel
                        </Link>
                      )}
                      <div style={{ height: 1, background: BORDER, margin: '4px 0' }} />
                      <button onClick={handleLogout}
                        style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '9px 16px', width: '100%', fontSize: 13, fontFamily: 'Jost,sans-serif', color: '#ff6b6b', background: 'none', border: 'none', cursor: 'pointer' }}
                        onMouseEnter={e => e.currentTarget.style.background = 'rgba(255,107,107,0.08)'}
                        onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
                      >
                        <FiLogOut size={14} /> Logout
                      </button>
                    </div>
                  )}
                </div>
              ) : (
                <Link to="/login"
                  style={{
                    display: 'inline-flex', alignItems: 'center', gap: 6,
                    padding: '8px 18px', borderRadius: 50,
                    border: `1px solid ${BORDER}`, color: CR,
                    fontFamily: 'Jost,sans-serif', fontWeight: 500, fontSize: 12,
                    textDecoration: 'none', transition: 'all 0.25s',
                  }}
                  onMouseEnter={e => { e.currentTarget.style.borderColor = G; e.currentTarget.style.color = G; }}
                  onMouseLeave={e => { e.currentTarget.style.borderColor = BORDER; e.currentTarget.style.color = CR; }}
                >
                  <FiUser size={13} /> Sign In
                </Link>
              )}
            </div>

            {/* ── Mobile: cart + hamburger ── */}
            <div className="nb-mobile">
              <div style={{ position: 'relative' }}>
                <IconBtn onClick={() => setIsOpen(true)}>
                  <FiShoppingBag size={18} />
                  {cartCount > 0 && <Badge n={cartCount} />}
                </IconBtn>
              </div>
              <IconBtn onClick={() => setMobileOpen(true)}><FiMenu size={20} /></IconBtn>
            </div>

          </div>
        </div>
      </nav>

      {/* ── Mobile full-screen overlay ── */}
      <div style={{
        position: 'fixed', inset: 0, background: 'rgba(10,10,10,0.98)',
        zIndex: 1100, display: 'flex', flexDirection: 'column', padding: '24px',
        transform: mobileOpen ? 'translateX(0)' : 'translateX(100%)',
        transition: 'transform 0.35s ease', overflowY: 'auto',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 40 }}>
          <Link to="/" onClick={() => setMobileOpen(false)} style={{ display: 'flex', alignItems: 'center', gap: 10, textDecoration: 'none' }}>
            <DiamondLogo size={36} />
            <div>
              <div style={{ fontFamily: 'Cinzel,serif', fontWeight: 700, fontSize: '1.05rem', letterSpacing: '2.5px', color: G, lineHeight: 1.15 }}>TAYYAB</div>
              <div style={{ fontFamily: 'Cinzel,serif', fontWeight: 400, fontSize: '0.65rem', letterSpacing: '3.5px', color: CR, lineHeight: 1.15 }}>JEWELLERS</div>
            </div>
          </Link>
          <button onClick={() => setMobileOpen(false)} style={{ background: 'rgba(201,168,76,0.1)', border: `1px solid ${BORDER}`, width: 36, height: 36, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', color: CR }}>
            <FiX size={18} />
          </button>
        </div>

        {[
          { label: 'Home',         to: '/'            },
          { label: 'Collections',  to: '/products'    },
          { label: 'About Us',     to: '/about'       },
          { label: 'Custom Order', to: '/custom-order'},
          { label: 'My Orders',    to: '/orders'      },
          { label: 'Wishlist',     to: '/wishlist'    },
        ].map(l => (
          <Link key={l.to} to={l.to} onClick={() => setMobileOpen(false)}
            style={{
              display: 'block', fontFamily: 'Cormorant Garamond,serif',
              fontSize: '1.8rem', fontWeight: 600, color: CR,
              padding: '14px 0', borderBottom: '1px solid rgba(201,168,76,0.1)',
              textDecoration: 'none', transition: 'color 0.2s',
            }}
            onMouseEnter={e => e.currentTarget.style.color = G}
            onMouseLeave={e => e.currentTarget.style.color = CR}
          >{l.label}</Link>
        ))}

        <a href={`tel:${phone}`}
          style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '14px 0', borderBottom: '1px solid rgba(201,168,76,0.1)', fontFamily: 'Jost,sans-serif', fontSize: '1rem', color: G, textDecoration: 'none' }}
        >
          <FiPhone size={16} /> {phoneDisplay}
        </a>

        <div style={{ marginTop: 'auto', paddingTop: 36, display: 'flex', flexDirection: 'column', gap: 12 }}>
          {user ? (
            <button onClick={() => { handleLogout(); setMobileOpen(false); }}
              style={{ padding: '12px', borderRadius: 50, border: '1.5px solid rgba(255,107,107,0.4)', background: 'none', color: '#ff6b6b', fontFamily: 'Jost,sans-serif', fontWeight: 600, fontSize: 14, cursor: 'pointer' }}>
              Logout
            </button>
          ) : (
            <>
              <Link to="/login" onClick={() => setMobileOpen(false)}
                style={{ padding: '13px', borderRadius: 50, background: `linear-gradient(135deg,${G},${GD})`, color: BG, textAlign: 'center', fontFamily: 'Jost,sans-serif', fontWeight: 700, fontSize: 14, textDecoration: 'none' }}>
                Sign In
              </Link>
              <Link to="/register" onClick={() => setMobileOpen(false)}
                style={{ padding: '12px', borderRadius: 50, border: `1.5px solid ${BORDER}`, color: CR, textAlign: 'center', fontFamily: 'Jost,sans-serif', fontWeight: 500, fontSize: 14, textDecoration: 'none' }}>
                Create Account
              </Link>
            </>
          )}
        </div>
      </div>
    </>
  );
}

/* ── Sub-components ── */
function NavItem({ label, to, active }) {
  return (
    <Link to={to}
      style={{
        fontFamily: 'Jost,sans-serif', fontSize: 13, fontWeight: 500,
        color: active ? G : CR, padding: '7px 14px',
        borderRadius: 8, textDecoration: 'none',
        borderBottom: `2px solid ${active ? G : 'transparent'}`,
        transition: 'color 0.2s', whiteSpace: 'nowrap',
      }}
      onMouseEnter={e => e.currentTarget.style.color = G}
      onMouseLeave={e => e.currentTarget.style.color = active ? G : CR}
    >
      {label}
    </Link>
  );
}

function IconBtn({ children, onClick }) {
  return (
    <button onClick={onClick}
      style={{
        width: 36, height: 36, borderRadius: '50%', background: 'none',
        border: '1.5px solid rgba(201,168,76,0.18)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        cursor: 'pointer', color: '#F0EAD6', position: 'relative',
        transition: 'all 0.2s', flexShrink: 0,
      }}
      onMouseEnter={e => { e.currentTarget.style.borderColor = '#C9A84C'; e.currentTarget.style.color = '#C9A84C'; }}
      onMouseLeave={e => { e.currentTarget.style.borderColor = 'rgba(201,168,76,0.18)'; e.currentTarget.style.color = '#F0EAD6'; }}
    >
      {children}
    </button>
  );
}

function Badge({ n }) {
  return (
    <span style={{
      position: 'absolute', top: -4, right: -4,
      background: '#C9A84C', color: '#0A0A0A',
      fontSize: 9, fontWeight: 700, minWidth: 16, height: 16,
      borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
      border: '2px solid #0A0A0A',
    }}>{n}</span>
  );
}
