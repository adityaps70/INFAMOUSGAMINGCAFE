export const siteData = {
  name: "inFAMOUS Gaming Cafe",
  shortName: "inFAMOUS",
  rating: "4.6",
  ratingSource: "Google rating",
  certification: "NVIDIA GeForce certified",
  phoneDisplay: "+91 99183 32386",
  phoneDigits: "919918332386",
  address:
    "A-1/114, Ratan Khand, Ruchi Khand 1, Sharda Nagar, Lucknow, Uttar Pradesh 226012",
  availabilityNote: "Message or call for current availability.",
  whatsappMessage:
    "Hi inFAMOUS Gaming Cafe, I'd like to book a gaming session. Please share current availability and rates.",
} as const;

export type SiteData = typeof siteData;

export const reviewThemes = [
  "Helpful staff and an easy first-visit experience",
  "A broad mix of on-screen and off-screen ways to play",
  "A social setting that works for friends and regular players",
] as const;
