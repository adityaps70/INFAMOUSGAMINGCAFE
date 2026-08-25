import { ArrowUpRight, Camera, MapPin, MessageCircle, Phone, Radio } from "lucide-react";
import { buildTelUrl, buildWhatsAppUrl, instagramUrl, mapsUrl } from "../links";
import { siteData } from "../siteData";

export default function Visit() {
  return (
    <section className="section visit-section" id="visit" aria-labelledby="visit-title">
      <div className="visit-heading">
        <p className="section-kicker">Make the next move</p>
        <h2 id="visit-title">Ready when your crew is.</h2>
        <p>Choose your mode, check current availability, and get directions without hunting around.</p>
      </div>

      <div className="visit-grid">
        <div className="visit-detail visit-address">
          <MapPin aria-hidden="true" />
          <span>Find us</span>
          <p>{siteData.address}</p>
          <a href={mapsUrl} target="_blank" rel="noreferrer">
            Open directions <ArrowUpRight aria-hidden="true" />
          </a>
        </div>

        <div className="visit-detail">
          <Radio aria-hidden="true" />
          <span>Before you leave</span>
          <p>{siteData.availabilityNote}</p>
          <small>This static site does not display live slot inventory.</small>
        </div>

        <div className="visit-detail">
          <Phone aria-hidden="true" />
          <span>Talk to us</span>
          <a className="visit-phone" href={buildTelUrl()}>
            {siteData.phoneDisplay}
          </a>
          <a href={buildWhatsAppUrl()} target="_blank" rel="noreferrer">
            WhatsApp us <MessageCircle aria-hidden="true" />
          </a>
        </div>

        <div className="visit-detail">
          <Camera aria-hidden="true" />
          <span>See the action</span>
          <p>@infamousgaming_cafe</p>
          <a href={instagramUrl} target="_blank" rel="noreferrer">
            Instagram <ArrowUpRight aria-hidden="true" />
          </a>
        </div>
      </div>
    </section>
  );
}
