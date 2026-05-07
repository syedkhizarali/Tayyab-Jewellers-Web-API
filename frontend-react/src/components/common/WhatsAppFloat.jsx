import { useEffect, useState } from 'react';
import { FaWhatsapp } from 'react-icons/fa';

export default function WhatsAppFloat() {
  const whatsapp = import.meta.env.VITE_WHATSAPP_NUMBER || '+92 3154844005';
  const msg = encodeURIComponent("Hi, I'm interested in your jewellery collection at Tayyab Jewellers.");
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const footer = document.querySelector('footer');
    if (!footer) return;

    const obs = new IntersectionObserver(
      ([entry]) => setVisible(!entry.isIntersecting),
      { threshold: 0.05 }
    );
    obs.observe(footer);
    return () => obs.disconnect();
  }, []);

  if (!visible) return null;

  return (
    <div className="whatsapp-float">
      <a
        href={`https://wa.me/${whatsapp}?text=${msg}`}
        target="_blank"
        rel="noreferrer"
        className="whatsapp-float-btn"
        aria-label="Chat on WhatsApp"
      >
        <div className="whatsapp-pulse" />
        <FaWhatsapp size={26} />
      </a>
    </div>
  );
}
