export type FaqItem = {
  question: string;
  answer: string;
};

export const faqItems: readonly FaqItem[] = [
  {
    question: "Do I need to book before visiting?",
    answer:
      "Walk-in plans may work, but messaging or calling first is the safest way to check current availability for the activity and time you want.",
  },
  {
    question: "How does a booking request work?",
    answer:
      "Choose your activity, preferred date and time, session length, and number of players. The site prepares the details for WhatsApp; your slot is confirmed only after the cafe replies.",
  },
  {
    question: "Where can I see the current rates?",
    answer:
      "Use the Rate Finder on this page. It shows the approved half-hour and full-hour rates by category, plus the published note for additional players.",
  },
  {
    question: "Can I plan a session for a group or celebration?",
    answer:
      "Yes. Use the group-session enquiry and share your preferred date, time, group size, and occasion. The cafe can then reply with what is practical for that request.",
  },
  {
    question: "How do I reach inFAMOUS Gaming Cafe?",
    answer:
      "The cafe is in Sharda Nagar, Lucknow. Use the Directions buttons on this page to open the current Google Maps destination.",
  },
  {
    question: "How do I check what is available right now?",
    answer:
      "Send a WhatsApp booking request or call the cafe. This website does not pretend to show live station or activity inventory.",
  },
] as const;
