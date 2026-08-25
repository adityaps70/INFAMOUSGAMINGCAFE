import { siteData } from "./siteData";

export const instagramUrl = "https://www.instagram.com/infamousgaming_cafe/";
export const mapsUrl =
  "https://www.google.com/maps/search/?api=1&query=inFAMOUS%20Gaming%20Cafe%20Lucknow";

export function buildWhatsAppUrl(message: string = siteData.whatsappMessage): string {
  return `https://wa.me/${siteData.phoneDigits}?text=${encodeURIComponent(message)}`;
}

export type BookingDetails = {
  name: string;
  game: string;
  date: string;
  time: string;
  duration: string;
  players: string;
  notes?: string;
  requestType?: "standard" | "group";
};

export function buildBookingWhatsAppUrl(details: BookingDetails): string {
  const lines = [
    "Hi inFAMOUS Gaming Cafe, I'd like to book a session.",
    "",
    `Name: ${details.name.trim()}`,
  ];

  if (details.requestType === "group") {
    lines.push("Request type: Group session");
  }

  lines.push(
    `Game: ${details.game.trim()}`,
    `Date: ${details.date.trim()}`,
    `Preferred time: ${details.time.trim()}`,
    `Duration: ${details.duration.trim()}`,
    `Players: ${details.players.trim()}`,
  );

  const notes = details.notes?.trim();
  if (notes) {
    lines.push(`Notes: ${notes}`);
  }

  lines.push("", "Please confirm availability.");
  return buildWhatsAppUrl(lines.join("\n"));
}

export function buildTelUrl(): string {
  return `tel:+${siteData.phoneDigits}`;
}
