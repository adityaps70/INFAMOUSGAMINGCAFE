import {
  ArrowUpRight,
  CircleDot,
  Gamepad2,
  Gauge,
  Headphones,
  MonitorPlay,
  Users,
} from "lucide-react";
import type { BookingIntent } from "../booking";
import { experienceItems } from "../experienceData";

const icons = {
  monitor: MonitorPlay,
  gamepad: Gamepad2,
  headset: Headphones,
  target: CircleDot,
  steering: Gauge,
  users: Users,
} as const;

type ArenaExplorerProps = {
  onBook: (intent?: BookingIntent) => void;
};

export default function ArenaExplorer({ onBook }: ArenaExplorerProps) {
  return (
    <section className="section arena-explorer" id="play" aria-labelledby="arena-title">
      <div className="section-heading arena-heading">
        <p className="section-kicker">Choose your arena</p>
        <h2 id="arena-title">One venue. More ways to play.</h2>
        <p>
          Start with what you feel like doing, then send the cafe your preferred time and group size.
        </p>
      </div>

      <div className="arena-experience-grid">
        {experienceItems.map((item, index) => {
          const Icon = icons[item.icon];
          const intent: BookingIntent = item.bookingActivity
            ? { activity: item.bookingActivity }
            : { notes: item.bookingNotes };

          return (
            <article className="arena-experience-card" key={item.title}>
              <div className="arena-card-topline">
                <span>0{index + 1}</span>
                <Icon aria-hidden="true" />
              </div>
              <p className="arena-eyebrow">{item.eyebrow}</p>
              <h3>{item.title}</h3>
              <p>{item.body}</p>
              <ul className="arena-tags" aria-label={`${item.title} session style`}>
                {item.tags.map((tag) => (
                  <li key={tag}>{tag}</li>
                ))}
              </ul>
              <button
                type="button"
                className="arena-card-action"
                onClick={() => onBook(intent)}
                aria-label={`Check availability for ${item.title}`}
              >
                Check availability
                <ArrowUpRight aria-hidden="true" />
              </button>
            </article>
          );
        })}
      </div>
    </section>
  );
}
