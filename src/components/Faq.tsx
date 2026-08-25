import { ChevronDown } from "lucide-react";
import { faqItems } from "../faqData";

export default function Faq() {
  return (
    <section className="section faq-section" id="faq" aria-labelledby="faq-title">
      <div className="section-heading faq-heading">
        <p className="section-kicker">Know before you go</p>
        <h2 id="faq-title">Questions before you play.</h2>
        <p>Practical answers without pretending this static site knows live venue availability.</p>
      </div>

      <div className="faq-list">
        {faqItems.map((item, index) => (
          <details key={item.question} open={index === 0}>
            <summary>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <strong>{item.question}</strong>
              <ChevronDown aria-hidden="true" />
            </summary>
            <p>{item.answer}</p>
          </details>
        ))}
      </div>
    </section>
  );
}
