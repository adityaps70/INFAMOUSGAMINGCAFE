import { galleryItems } from "../galleryData";

export default function Gallery() {
  return (
    <section className="section gallery-section" id="gallery" aria-labelledby="gallery-title">
      <div className="gallery-heading section-heading">
        <p className="section-kicker">Inside the venue</p>
        <h2 id="gallery-title">Inside inFAMOUS.</h2>
        <p>
          A real look inside the cafe — from PC and VR corners to console seating,
          billiards, table tennis, and event moments.
        </p>
      </div>

      <div className="gallery-grid">
        {galleryItems.map((item, index) => (
          <figure className={`gallery-tile gallery-tile-${index + 1}`} key={item.title}>
            <div className="gallery-media">
              <img
                src={item.imageSrc}
                alt={item.imageAlt ?? item.title}
                loading="lazy"
                width="960"
                height="720"
              />
              <span className="gallery-scanline" aria-hidden="true" />
              <span className="gallery-frame-id" aria-hidden="true">
                inFAMOUS // {String(index + 1).padStart(2, "0")}
              </span>
            </div>
            <figcaption>
              <strong>{item.title}</strong>
              <span>{item.caption}</span>
            </figcaption>
          </figure>
        ))}
      </div>
    </section>
  );
}
