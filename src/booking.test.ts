import { describe, expect, it } from "vitest";
import { activityOptions, getLocalDateInputMin } from "./booking";

describe("booking utilities", () => {
  it("formats the browser-local booking minimum without UTC drift", () => {
    expect(getLocalDateInputMin(new Date(2026, 7, 25, 23, 30))).toBe("2026-08-25");
  });

  it("derives booking activities from the approved rate card plus VR", () => {
    expect(activityOptions).toContain("PlayStation 5");
    expect(activityOptions).toContain("PC Gaming");
    expect(activityOptions).toContain("Flight Simulator");
    expect(activityOptions).toContain("VR / Simulation");
    expect(new Set(activityOptions).size).toBe(activityOptions.length);
  });
});
