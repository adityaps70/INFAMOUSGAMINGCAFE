import {
  Gamepad2,
  Headphones,
  MapPin,
  MessageCircle,
  MonitorPlay,
  Phone,
  Star,
  Users,
} from "lucide-react";
import type { BookingIntent } from "../booking";
import { buildTelUrl, mapsUrl } from "../links";
import { siteData } from "../siteData";

const heroCopy = {
  eyebrow: "Sharda Nagar, Lucknow",
  titleLead: "Play your way.",
  titleAccent: "Own the session.",
  body: "PC, PlayStation, VR, simulators, cue games, table games, and easy group plans — all from one place.",
  primary: "Book on WhatsApp",
  call: "Call now",
  directions: "Get directions",
} as const;

const arenaModes: readonly {
  label: string;
  meta: string;
  icon: typeof MonitorPlay;
  intent: BookingIntent;
}[] = [
  {
    label: "PC GAMING",
    meta: "FOCUS MODE",
    icon: MonitorPlay,
    intent: { activity: "PC Gaming" },
  },
  {
    label: "PLAYSTATION",
    meta: "CONTROLLER MODE",
    icon: Gamepad2,
    intent: { notes: "PlayStation session enquiry" },
  },
  {
    label: "VR + SIM",
    meta: "IMMERSIVE MODE",
    icon: Headphones,
    intent: { activity: "VR / Simulation" },
  },
  {
    label: "GROUPS",
    meta: "CREW MODE",
    icon: Users,
    intent: { requestType: "group", notes: "Group session enquiry" },
  },
];

type HeroProps = {
  onBook: (intent?: BookingIntent) => void;
};

export default function Hero({ onBook }: HeroProps) {
  return (
    <section className="hero" id="top" aria-labelledby="hero-title">
      <div className="hero-copy">
        <p className="eyebrow">
          <span className="live-dot" aria-hidden="true" />
          {heroCopy.eyebrow}
        </p>

        <h1 id="hero-title">
          <span>{heroCopy.titleLead}</span>
          <span className="title-accent">{heroCopy.titleAccent}</span>
        </h1>

        <p className="hero-body">{heroCopy.body}</p>

        <div className="proof-row" aria-label="Venue highlights">
          <span className="proof-chip rating-chip">
            <Star aria-hidden="true" size={15} fill="currentColor" />
            <strong>{siteData.rating}</strong>
            {siteData.ratingSource}
          </span>
          <span className="proof-chip certification-chip">
            <span aria-hidden="true" className="cert-mark">
              N
            </span>
            {siteData.certification}
          </span>
        </div>

        <div className="hero-actions">
          <button
            type="button"
            className="button button-primary"
            onClick={() => onBook()}
          >
            <MessageCircle aria-hidden="true" />
            {heroCopy.primary}
          </button>
          <a className="button button-secondary" href={buildTelUrl()}>
            <Phone aria-hidden="true" />
            {heroCopy.call}
          </a>
          <a
            className="text-action"
            href={mapsUrl}
            target="_blank"
            rel="noreferrer"
          >
            <MapPin aria-hidden="true" />
            {heroCopy.directions}
          </a>
        </div>
      </div>

      <div className="arena-panel" aria-label="Ways to start a session at inFAMOUS">
        <img
          className="hero-brand-logo"
          src="./logo.png"
          alt="inFAMOUS Gaming Cafe original logo"
        />
        <div className="panel-topline">
          <span>SESSION SELECT</span>
          <span className="panel-status">ENQUIRE → CONFIRM</span>
        </div>

        <div className="arena-grid">
          {arenaModes.map(({ label, meta, icon: Icon, intent }, index) => (
            <button
              className={`arena-mode arena-mode-${index + 1}`}
              key={label}
              type="button"
              onClick={() => onBook(intent)}
              aria-label={`Start a ${label.toLowerCase()} booking enquiry`}
            >
              <span className="mode-number">0{index + 1}</span>
              <Icon aria-hidden="true" strokeWidth={1.6} />
              <span>
                <strong>{label}</strong>
                <small>{meta}</small>
              </span>
            </button>
          ))}
        </div>

        <div className="panel-footer">
          <span>SHARDA NAGAR // LUCKNOW</span>
          <span>CHOOSE → MESSAGE → CONFIRM</span>
        </div>
      </div>
    </section>
  );
}
