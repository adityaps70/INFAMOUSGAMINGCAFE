import { CheckCircle2, MessageCircle, MousePointer2 } from "lucide-react";

const steps = [
  {
    number: "01",
    title: "Choose your mode",
    body: "Browse the arena or rate finder and decide what you want to play.",
    icon: MousePointer2,
  },
  {
    number: "02",
    title: "Send your preference",
    body: "Share your preferred date, time, session length, and group size through WhatsApp.",
    icon: MessageCircle,
  },
  {
    number: "03",
    title: "Confirm, then arrive",
    body: "Wait for the cafe reply confirming availability, then head over for your session.",
    icon: CheckCircle2,
  },
] as const;

export default function VisitSteps() {
  return (
    <section className="section visit-steps-section" id="how-it-works" aria-labelledby="steps-title">
      <div className="section-heading compact-heading">
        <p className="section-kicker">No complicated checkout</p>
        <h2 id="steps-title">How your session works.</h2>
        <p>Three clear steps. No account, payment gateway, or fake instant reservation.</p>
      </div>

      <ol className="visit-steps">
        {steps.map(({ number, title, body, icon: Icon }) => (
          <li key={number}>
            <span className="step-number">{number}</span>
            <Icon aria-hidden="true" />
            <div>
              <h3>{title}</h3>
              <p>{body}</p>
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}
