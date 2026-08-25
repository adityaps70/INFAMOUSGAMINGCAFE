import rawRateGroups from "./rates.json";

export type RateItem = {
  name: string;
  halfHour: number;
  fullHour: number;
};

export type RateGroup = {
  category: string;
  items: RateItem[];
};

export const rateGroups = rawRateGroups satisfies RateGroup[];
export const additionalPlayerNote = "Additional charges apply for more than two players.";

