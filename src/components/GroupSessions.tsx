import { ArrowUpRight, CakeSlice, GraduationCap, Users } from "lucide-react";
import type { BookingIntent } from "../booking";

const groupTypes = [
  { label: "Friend squads", icon: Users },
  { label: "Birthdays + celebrations", icon: CakeSlice },
  { label: "College + casual groups", icon: GraduationCap },
] as const;

type GroupSessionsProps = {
  onBook: (intent?: BookingIntent) => void;
};

export default function GroupSessions({ onBook }: GroupSessionsProps) {
  return (
    <section className="section group-section" id="groups" aria-labelledby="groups-title">
      <div className="group-copy">
        <p className="section-kicker">Crew mode</p>
        <h2 id="groups-title">Bring the whole squad.</h2>
        <p>
          Planning more than a quick solo session? Send the cafe your preferred date, time,
          group size, and occasion so the team can tell you what works.
        </p>
        <button
          className="button button-primary group-cta"
          type="button"
          onClick={() =>
            onBook({
              requestType: "group",
              notes: "Group session enquiry",
            })
          }
        >
          Plan a group session
          <ArrowUpRight aria-hidden="true" />
        </button>
        <small>No package, discount, or slot is promised until the cafe confirms it.</small>
      </div>

      <div className="group-types" aria-label="Group session ideas">
        {groupTypes.map(({ label, icon: Icon }, index) => (
          <div key={label}>
            <span>0{index + 1}</span>
            <Icon aria-hidden="true" />
            <strong>{label}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}
