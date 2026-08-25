import { describe, expect, it } from "vitest";
import {
  buildBookingWhatsAppUrl,
  buildTelUrl,
  buildWhatsAppUrl,
  instagramUrl,
  mapsUrl,
} from "./links";
import { rateGroups } from "./rates";
import { siteData } from "./siteData";
import { experienceItems } from "./experienceData";

describe("business contact data", () => {
  it("keeps the approved phone number in display and machine formats", () => {
    expect(siteData.phoneDisplay).toBe("+91 99183 32386");
    expect(siteData.phoneDigits).toBe("919918332386");
    expect(buildTelUrl()).toBe("tel:+919918332386");
  });

  it("builds the approved booking message without a backend", () => {
    const url = buildWhatsAppUrl();
    expect(url).toContain("https://wa.me/919918332386?text=");
    expect(decodeURIComponent(url.split("text=")[1])).toBe(
      "Hi inFAMOUS Gaming Cafe, I'd like to book a gaming session. Please share current availability and rates.",
    );
  });

  it("turns completed booking details into a pre-filled WhatsApp request", () => {
    const url = buildBookingWhatsAppUrl({
      name: "Aman",
      game: "PlayStation 5",
      date: "2026-08-29",
      time: "18:30",
      duration: "Full hour",
      players: "2",
      notes: "Two controllers please",
    });

    expect(url).toContain("https://wa.me/919918332386?text=");
    expect(decodeURIComponent(url.split("text=")[1])).toBe(
      "Hi inFAMOUS Gaming Cafe, I'd like to book a session.\n\nName: Aman\nGame: PlayStation 5\nDate: 2026-08-29\nPreferred time: 18:30\nDuration: Full hour\nPlayers: 2\nNotes: Two controllers please\n\nPlease confirm availability.",
    );
  });


  it("labels a group enquiry without inventing a package", () => {
    const url = buildBookingWhatsAppUrl({
      name: "Aman",
      game: "PC Gaming",
      date: "2026-08-29",
      time: "18:30",
      duration: "Full hour",
      players: "6",
      requestType: "group",
    });

    expect(decodeURIComponent(url)).toContain("Request type: Group session");
  });

  it("keeps public experience copy free of fabricated inventory and hardware claims", () => {
    expect(JSON.stringify(experienceItems)).not.toMatch(/RTX|station count|available now|units available/i);
  });

  it("uses the verified public destinations", () => {
    expect(instagramUrl).toBe("https://www.instagram.com/infamousgaming_cafe/");
    expect(mapsUrl).toContain("google.com/maps/search/");
    expect(decodeURIComponent(mapsUrl)).toContain("inFAMOUS Gaming Cafe Lucknow");
  });

  it("keeps every owner-confirmed half-hour and full-hour rate", () => {
    expect(rateGroups).toEqual([
      {
        category: "Gaming Room",
        items: [
          { name: "PlayStation 5", halfHour: 200, fullHour: 400 },
          { name: "PlayStation 4", halfHour: 99, fullHour: 179 },
          { name: "PC Gaming", halfHour: 99, fullHour: 179 },
          { name: "Table Tennis", halfHour: 100, fullHour: 180 },
        ],
      },
      {
        category: "Billiards",
        items: [
          { name: "Snooker", halfHour: 99, fullHour: 179 },
          { name: "Pool - Red/Blue", halfHour: 60, fullHour: 100 },
          { name: "Pool - Green", halfHour: 80, fullHour: 150 },
        ],
      },
      {
        category: "Arcade",
        items: [
          { name: "Foosball", halfHour: 49, fullHour: 89 },
          { name: "Steering Wheel", halfHour: 149, fullHour: 299 },
          { name: "Flight Simulator", halfHour: 149, fullHour: 299 },
        ],
      },
      {
        category: "Card / Board Games",
        items: [
          { name: "UNO", halfHour: 49, fullHour: 89 },
          { name: "Chess", halfHour: 49, fullHour: 89 },
          { name: "Carrom", halfHour: 49, fullHour: 89 },
        ],
      },
    ]);
  });
});
