import { Aperture, Gamepad2, Headphones, Users } from "lucide-react";
import { galleryItems } from "../galleryData";

const placeholderIcons = [Aperture, Gamepad2, Headphones, Users] as const;

export default function Gallery() {
  return (
    <section className="section gallery-section" id="gallery" aria-labelledby="gallery-title">
      <div className="gallery-heading section-heading">
        <p className="section-kicker">Session preview</p>
        <h2 id="gallery-title">Inside inFAMOUS.</h2>
        <p>
          Screen time, controller play, immersive modes, and crew energy — different ways to
          shape a session without overcomplicating the plan.
        </p>
      </div>

      <div className="gallery-grid">
        {galleryItems.map((item, index) => {
          const Icon = placeholderIcons[index % placeholderIcons.length];
          return (
            <figure className={`gallery-tile gallery-tile-${index + 1}`} key={item.title}>
              {item.imageSrc ? (
                <img
                  src={item.imageSrc}
                  alt={item.imageAlt ?? item.title}
                  loading="lazy"
                  width="960"
                  height="720"
                />
              ) : (
                <div className="gallery-placeholder" aria-label={`${item.title} branded session visual`}>
                  <span className="gallery-scanline" aria-hidden="true" />
                  <Icon aria-hidden="true" />
                  <span>inFAMOUS // {String(index + 1).padStart(2, "0")}</span>
                </div>
              )}
              <figcaption>
                <strong>{item.title}</strong>
                <span>{item.caption}</span>
              </figcaption>
            </figure>
          );
        })}
      </div>
    </section>
  );
}
