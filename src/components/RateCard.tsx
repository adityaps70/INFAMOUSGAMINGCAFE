import { ArrowUpRight, MessageCircle } from "lucide-react";
import { useState, type KeyboardEvent } from "react";
import type { BookingIntent } from "../booking";
import { additionalPlayerNote, rateGroups } from "../rates";

function formatPrice(value: number) {
  return `₹${value}`;
}

type RateCardProps = {
  onBook: (intent?: BookingIntent) => void;
};

export default function RateCard({ onBook }: RateCardProps) {
  const [activeGroupIndex, setActiveGroupIndex] = useState(0);
  const activeGroup = rateGroups[activeGroupIndex];

  const activateTab = (index: number, focus = false) => {
    const nextIndex = (index + rateGroups.length) % rateGroups.length;
    setActiveGroupIndex(nextIndex);
    if (focus) {
      requestAnimationFrame(() => document.getElementById(`rate-tab-${nextIndex}`)?.focus());
    }
  };

  const handleTabKeyDown = (event: KeyboardEvent<HTMLButtonElement>, index: number) => {
    let nextIndex: number | null = null;

    if (event.key === "ArrowRight") nextIndex = index + 1;
    if (event.key === "ArrowLeft") nextIndex = index - 1;
    if (event.key === "Home") nextIndex = 0;
    if (event.key === "End") nextIndex = rateGroups.length - 1;

    if (nextIndex === null) return;
    event.preventDefault();
    activateTab(nextIndex, true);
  };

  return (
    <section className="section rates-section" id="rates" aria-labelledby="rates-title">
      <div className="rates-intro">
        <div className="section-heading">
          <p className="section-kicker">Know before you go</p>
          <h2 id="rates-title">Find your rate.</h2>
          <p>Switch categories, compare session lengths, then carry your choice straight into booking.</p>
        </div>
        <button
          className="button button-primary rates-action"
          type="button"
          onClick={() => onBook()}
        >
          <MessageCircle aria-hidden="true" />
          Check availability
        </button>
      </div>

      <div className="rate-explorer">
        <div className="rate-tabs" role="tablist" aria-label="Rate categories">
          {rateGroups.map((group, groupIndex) => (
            <button
              type="button"
              role="tab"
              aria-selected={activeGroupIndex === groupIndex}
              aria-controls="active-rate-panel"
              id={`rate-tab-${groupIndex}`}
              tabIndex={activeGroupIndex === groupIndex ? 0 : -1}
              onClick={() => activateTab(groupIndex)}
              onKeyDown={(event: KeyboardEvent<HTMLButtonElement>) => handleTabKeyDown(event, groupIndex)}
              key={group.category}
            >
              <span aria-hidden="true">0{groupIndex + 1}</span>
              {group.category}
            </button>
          ))}
        </div>

        <div
          className="rate-table-wrap compact-rate-panel"
          id="active-rate-panel"
          role="tabpanel"
          aria-labelledby={`rate-tab-${activeGroupIndex}`}
        >
          <span className="rate-index">0{activeGroupIndex + 1}</span>
          <table className="rate-table">
            <caption>{activeGroup.category}</caption>
            <thead>
              <tr>
                <th scope="col">Item</th>
                <th scope="col">Half hour</th>
                <th scope="col">Full hour</th>
                <th scope="col"><span className="visually-hidden">Booking action</span></th>
              </tr>
            </thead>
            <tbody>
              {activeGroup.items.map((item) => (
                <tr key={item.name}>
                  <th scope="row">{item.name}</th>
                  <td data-label="Half hour">{formatPrice(item.halfHour)}</td>
                  <td data-label="Full hour">{formatPrice(item.fullHour)}</td>
                  <td className="rate-book-cell">
                    <button
                      type="button"
                      className="rate-book-button"
                      onClick={() => onBook({ activity: item.name })}
                      aria-label={`Book ${item.name}`}
                    >
                      Book
                      <ArrowUpRight aria-hidden="true" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="rate-note">
        <p>{additionalPlayerNote}</p>
        <button
          type="button"
          onClick={() =>
            onBook({ requestType: "group", notes: "Group session enquiry" })
          }
        >
          Ask about group sessions
          <ArrowUpRight aria-hidden="true" />
        </button>
      </div>
    </section>
  );
}
