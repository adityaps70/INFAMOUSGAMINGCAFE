import { rateGroups } from "./rates";

export type BookingIntent = {
  activity?: string;
  requestType?: "standard" | "group";
  notes?: string;
};

export function getLocalDateInputMin(date = new Date()): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

export const activityOptions = [
  ...new Set(rateGroups.flatMap((group) => group.items.map((item) => item.name))),
  "VR / Simulation",
] as const;
