import { ArrowUpRight, Camera, Check, Star } from "lucide-react";
import { instagramUrl } from "../links";
import { reviewThemes, siteData } from "../siteData";

export default function SocialProof() {
  return (
    <section className="section vibes-section" id="vibes" aria-labelledby="vibes-title">
      <div className="vibes-score" aria-label={`${siteData.rating} ${siteData.ratingSource}`}>
        <span>{siteData.rating}</span>
        <div>
          <div className="star-row" aria-hidden="true">
            {Array.from({ length: 5 }).map((_, index) => (
              <Star key={index} fill="currentColor" />
            ))}
          </div>
          <small>{siteData.ratingSource}</small>
        </div>
      </div>

      <div className="vibes-copy">
        <p className="section-kicker">Why players come back</p>
        <h2 id="vibes-title">A better place to spend the session.</h2>
        <p>
          The strongest feedback themes are simple: helpful people, plenty of ways to play,
          and a setting that works whether you are new or already a regular.
        </p>
        <ul className="review-themes">
          {reviewThemes.map((theme) => (
            <li key={theme}>
              <Check aria-hidden="true" />
              {theme}
            </li>
          ))}
        </ul>
        <a
          className="instagram-action"
          href={instagramUrl}
          target="_blank"
          rel="noreferrer"
          aria-label="Follow on Instagram"
        >
          <Camera aria-hidden="true" />
          @infamousgaming_cafe
          <ArrowUpRight aria-hidden="true" />
        </a>
      </div>
    </section>
  );
}
