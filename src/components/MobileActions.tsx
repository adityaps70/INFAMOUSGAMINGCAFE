import { MapPin, MessageCircle, Phone } from "lucide-react";
import type { BookingIntent } from "../booking";
import { buildTelUrl, mapsUrl } from "../links";

type MobileActionsProps = {
  onBook: (intent?: BookingIntent) => void;
};

export default function MobileActions({ onBook }: MobileActionsProps) {
  return (
    <nav className="mobile-actions" aria-label="Quick booking actions">
      <button type="button" onClick={() => onBook()}>
        <MessageCircle aria-hidden="true" />
        Book
      </button>
      <a href={buildTelUrl()}>
        <Phone aria-hidden="true" />
        Call
      </a>
      <a href={mapsUrl} target="_blank" rel="noreferrer">
        <MapPin aria-hidden="true" />
        Directions
      </a>
    </nav>
  );
}
