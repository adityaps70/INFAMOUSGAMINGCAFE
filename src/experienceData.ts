export type ExperienceIconKey =
  | "monitor"
  | "gamepad"
  | "headset"
  | "target"
  | "steering"
  | "users";

export type ExperienceItem = {
  title: string;
  eyebrow: string;
  body: string;
  icon: ExperienceIconKey;
  tags: readonly string[];
  bookingActivity?: string;
  bookingNotes?: string;
};

export const experienceItems: readonly ExperienceItem[] = [
  {
    title: "PC Gaming",
    eyebrow: "Lock in",
    body: "Settle in for focused solo sessions, quick matches, or a longer grind with your crew.",
    icon: "monitor",
    tags: ["competitive", "focused", "solo + squads"],
    bookingActivity: "PC Gaming",
  },
  {
    title: "PlayStation",
    eyebrow: "Pass the controller",
    body: "Controller-first sessions built for couch rivalry, co-op plans, and easy group play.",
    icon: "gamepad",
    tags: ["social", "competitive", "controller"],
    bookingNotes: "PlayStation session enquiry",
  },
  {
    title: "VR + Simulation",
    eyebrow: "Step inside",
    body: "Switch up the usual screen time with immersive VR and simulator-style experiences.",
    icon: "headset",
    tags: ["immersive", "different", "experience"],
    bookingActivity: "VR / Simulation",
  },
  {
    title: "Cue + Table Games",
    eyebrow: "Off-screen rivalry",
    body: "Break up a gaming session with pool, snooker, or table tennis and keep the competition going.",
    icon: "target",
    tags: ["social", "casual", "competitive"],
    bookingNotes: "Cue or table-game session enquiry",
  },
  {
    title: "Arcade Controls",
    eyebrow: "Take the controls",
    body: "Try steering and flight-simulator sessions when you want a different kind of challenge.",
    icon: "steering",
    tags: ["simulation", "hands-on", "casual"],
    bookingNotes: "Steering or flight simulator enquiry",
  },
  {
    title: "Social Games",
    eyebrow: "Keep the crew together",
    body: "Mix in foosball, UNO, chess, carrom, and other easy-going ways to spend time together.",
    icon: "users",
    tags: ["group", "casual", "hangout"],
    bookingNotes: "Social games session enquiry",
  },
] as const;
