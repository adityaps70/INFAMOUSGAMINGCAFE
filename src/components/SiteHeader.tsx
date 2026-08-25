import { Menu, MessageCircle, X } from "lucide-react";
import { useState } from "react";
import type { BookingIntent } from "../booking";

type SiteHeaderProps = {
  onBook: (intent?: BookingIntent) => void;
};

const navItems = [
  { href: "#play", label: "Play" },
  { href: "#rates", label: "Rates" },
  { href: "#vibes", label: "Vibes" },
  { href: "#visit", label: "Visit" },
] as const;

export default function SiteHeader({ onBook }: SiteHeaderProps) {
  const [mobileOpen, setMobileOpen] = useState(false);

  const closeMobile = () => setMobileOpen(false);
  const handleBook = () => {
    closeMobile();
    onBook();
  };

  return (
    <header className="site-header">
      <a className="wordmark" href="#top" aria-label="inFAMOUS Gaming Cafe home">
        <img src="./logo.png" alt="inFAMOUS Gaming Cafe logo" />
      </a>

      <nav className="main-nav" aria-label="Main navigation">
        {navItems.map((item) => (
          <a key={item.href} href={item.href}>
            {item.label}
          </a>
        ))}
      </nav>

      <button
        type="button"
        className="header-action"
        onClick={handleBook}
        aria-label="Book a session"
      >
        <MessageCircle aria-hidden="true" size={17} strokeWidth={2.4} />
        <span>Book a session</span>
      </button>

      <button
        type="button"
        className="nav-toggle"
        aria-label={mobileOpen ? "Close navigation" : "Open navigation"}
        aria-expanded={mobileOpen}
        aria-controls="mobile-navigation"
        onClick={() => setMobileOpen((current) => !current)}
      >
        {mobileOpen ? <X aria-hidden="true" /> : <Menu aria-hidden="true" />}
      </button>

      {mobileOpen ? (
        <nav
          className="mobile-nav"
          id="mobile-navigation"
          aria-label="Mobile navigation"
        >
          {navItems.map((item) => (
            <a key={item.href} href={item.href} onClick={closeMobile}>
              {item.label}
            </a>
          ))}
          <button type="button" onClick={handleBook}>
            <MessageCircle aria-hidden="true" />
            Book a session
          </button>
        </nav>
      ) : null}
    </header>
  );
}
