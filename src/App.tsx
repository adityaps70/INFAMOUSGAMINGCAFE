import { useState } from "react";
import type { BookingIntent } from "./booking";
import BookingForm from "./components/BookingForm";
import Hero from "./components/Hero";
import Faq from "./components/Faq";
import Gallery from "./components/Gallery";
import GroupSessions from "./components/GroupSessions";
import ArenaExplorer from "./components/ArenaExplorer";
import MobileActions from "./components/MobileActions";
import RateCard from "./components/RateCard";
import SiteHeader from "./components/SiteHeader";
import SocialProof from "./components/SocialProof";
import Visit from "./components/Visit";
import VisitSteps from "./components/VisitSteps";

export default function App() {
  const [bookingState, setBookingState] = useState<{
    open: boolean;
    intent: BookingIntent;
  }>({ open: false, intent: {} });

  const openBooking = (intent: BookingIntent = {}) => {
    setBookingState({ open: true, intent });
  };

  const closeBooking = () => {
    setBookingState((current) => ({ ...current, open: false }));
  };

  return (
    <div className="site-shell">
      <SiteHeader onBook={openBooking} />
      <main>
        <Hero onBook={openBooking} />
        <ArenaExplorer onBook={openBooking} />
        <VisitSteps />
        <RateCard onBook={openBooking} />
        <SocialProof />
        <Gallery />
        <GroupSessions onBook={openBooking} />
        <Faq />
        <Visit />
      </main>
      <footer className="site-footer">
        <span>inFAMOUS Gaming Cafe</span>
        <span>Sharda Nagar // Lucknow</span>
      </footer>
      <MobileActions onBook={openBooking} />
      <BookingForm
        open={bookingState.open}
        intent={bookingState.intent}
        onClose={closeBooking}
      />
    </div>
  );
}
