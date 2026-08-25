import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import App from "./App";

describe("inFAMOUS landing page", () => {
  it("uses the restored original logo in the header and hero", () => {
    render(<App />);

    const header = screen.getByRole("banner");
    expect(
      within(header).getByRole("img", { name: "inFAMOUS Gaming Cafe logo" }),
    ).toHaveAttribute("src", "./logo.png");

    const hero = screen.getByRole("region", { name: /play your way/i });
    expect(
      within(hero).getByRole("img", { name: "inFAMOUS Gaming Cafe original logo" }),
    ).toHaveAttribute("src", "./logo.png");
  });

  it("introduces the venue and exposes the primary actions", () => {
    render(<App />);

    expect(screen.getByRole("heading", { level: 1, name: /play your way/i })).toBeInTheDocument();
    expect(screen.getAllByText("4.6").length).toBeGreaterThan(0);
    expect(screen.getByText(/nvidia geforce certified/i)).toBeInTheDocument();

    expect(screen.getByRole("button", { name: /book a session/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /book on whatsapp/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /call now/i })).toHaveAttribute(
      "href",
      "tel:+919918332386",
    );
    expect(screen.getByRole("link", { name: /get directions/i })).toHaveAttribute(
      "href",
      expect.stringContaining("google.com/maps"),
    );
  });

  it("provides an accessible mobile navigation disclosure and avoids fake live status", async () => {
    const user = userEvent.setup();
    render(<App />);

    const toggle = screen.getByRole("button", { name: /open navigation/i });
    expect(toggle).toHaveAttribute("aria-expanded", "false");
    await user.click(toggle);
    expect(toggle).toHaveAttribute("aria-expanded", "true");
    expect(screen.getByRole("navigation", { name: /mobile navigation/i })).toBeInTheDocument();
    expect(screen.queryByText(/^ONLINE$/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/available now|stations? available/i)).not.toBeInTheDocument();
  });

  it("covers the verified venue experience without unverified hardware claims", () => {
    render(<App />);

   expect(
  screen.getByRole("heading", { name: /one venue\. more ways to play\./i }),
).toBeInTheDocument();
    for (const label of [
      "PC Gaming",
      "PlayStation",
      "VR + Simulation",
      "Cue + Table Games",
      "Arcade Controls",
      "Social Games",
    ]) {
      expect(screen.getByRole("heading", { name: label })).toBeInTheDocument();
    }

    expect(screen.getByRole("heading", { name: /how your session works/i })).toBeInTheDocument();
    expect(screen.queryByText(/rtx 30|ps5 available|station count/i)).not.toBeInTheDocument();
  });

  it("carries an arena choice into the shared booking dialog", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByRole("button", { name: /check availability for pc gaming/i }));
    const dialog = screen.getByRole("dialog", { name: /book a gaming session/i });
    expect(within(dialog).getByLabelText("Game or activity")).toHaveValue("PC Gaming");
  });

  it("keeps rates compact and lets visitors switch pricing categories", async () => {
    const user = userEvent.setup();
    render(<App />);

    expect(screen.getByRole("heading", { name: /find your rate/i })).toBeInTheDocument();
    const gamingRoom = screen.getByRole("table", { name: "Gaming Room" });
    const playStationRow = within(gamingRoom).getByRole("row", { name: /PlayStation 5/ });
    expect(within(playStationRow).getByText("₹200")).toBeInTheDocument();
    expect(within(playStationRow).getByText("₹400")).toBeInTheDocument();

    expect(screen.queryByRole("table", { name: "Billiards" })).not.toBeInTheDocument();

    await user.click(screen.getByRole("tab", { name: "Billiards" }));
    const billiards = screen.getByRole("table", { name: "Billiards" });
    const poolRow = within(billiards).getByRole("row", { name: /Pool - Red\/Blue/ });
    expect(within(poolRow).getByText("₹60")).toBeInTheDocument();
    expect(within(poolRow).getByText("₹100")).toBeInTheDocument();
    expect(screen.queryByRole("table", { name: "Gaming Room" })).not.toBeInTheDocument();

    await user.click(screen.getByRole("tab", { name: "Arcade" }));
    const arcade = screen.getByRole("table", { name: "Arcade" });
    const simulatorRow = within(arcade).getByRole("row", { name: /Flight Simulator/ });
    expect(within(simulatorRow).getByText("₹149")).toBeInTheDocument();
    expect(within(simulatorRow).getByText("₹299")).toBeInTheDocument();
    expect(screen.getByText(/additional charges apply for more than two players/i)).toBeInTheDocument();
  });

  it("supports keyboard rate navigation and contextual item booking", async () => {
    const user = userEvent.setup();
    render(<App />);

    const gamingTab = screen.getByRole("tab", { name: "Gaming Room" });
    gamingTab.focus();
    await user.keyboard("{ArrowRight}");
    expect(screen.getByRole("tab", { name: "Billiards" })).toHaveAttribute("aria-selected", "true");

    await user.keyboard("{Home}");
    expect(screen.getByRole("tab", { name: "Gaming Room" })).toHaveAttribute("aria-selected", "true");
    await user.click(screen.getByRole("button", { name: /book playstation 5/i }));
    expect(within(screen.getByRole("dialog")).getByLabelText("Game or activity")).toHaveValue("PlayStation 5");
  });

  it("opens the top booking form and sends its details to WhatsApp", async () => {
    const user = userEvent.setup();
    const openWindow = vi.spyOn(window, "open").mockImplementation(() => null);
    render(<App />);

    expect(screen.queryByRole("dialog", { name: /book a gaming session/i })).not.toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: /book a session/i }));

    const dialog = screen.getByRole("dialog", { name: /book a gaming session/i });
    await user.type(within(dialog).getByLabelText("Your name"), "Aman");
    await user.selectOptions(within(dialog).getByLabelText("Game or activity"), "PlayStation 5");
    await user.type(within(dialog).getByLabelText("Booking date"), "2026-08-29");
    await user.type(within(dialog).getByLabelText("Preferred time"), "18:30");
    await user.selectOptions(within(dialog).getByLabelText("Session duration"), "Full hour");
    await user.clear(within(dialog).getByLabelText("Number of players"));
    await user.type(within(dialog).getByLabelText("Number of players"), "2");
    await user.type(within(dialog).getByLabelText("Anything else?"), "Two controllers please");
    await user.click(within(dialog).getByRole("button", { name: /continue on whatsapp/i }));

    expect(openWindow).toHaveBeenCalledTimes(1);
    const [url, target, features] = openWindow.mock.calls[0];
    expect(target).toBe("_blank");
    expect(features).toBe("noopener,noreferrer");
    expect(decodeURIComponent(String(url))).toContain("Name: Aman");
    expect(decodeURIComponent(String(url))).toContain("Game: PlayStation 5");
    expect(decodeURIComponent(String(url))).toContain("Players: 2");

    openWindow.mockRestore();
  });

  it("completes the trust, group, FAQ, gallery, and mobile conversion journey", async () => {
    const user = userEvent.setup();
    render(<App />);

    expect(screen.getByRole("heading", { name: /inside infamous/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /bring the whole squad/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /questions before you play/i })).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: /plan a group session/i }));
    const groupDialog = screen.getByRole("dialog", { name: /book a gaming session/i });
    expect(groupDialog).toHaveTextContent(/group session enquiry/i);
    expect(within(groupDialog).getByLabelText("Number of players")).toHaveValue(null);
    expect(within(groupDialog).getByLabelText("Number of players")).not.toHaveAttribute("max");
    await user.keyboard("{Escape}");

    const quickActions = screen.getByRole("navigation", { name: /quick booking actions/i });
    expect(within(quickActions).getByRole("link", { name: /directions/i })).toHaveAttribute(
      "href",
      expect.stringContaining("google.com/maps"),
    );
  });

  it("keeps the booking dialog keyboard-safe and prevents past-date selection", async () => {
    const user = userEvent.setup();
    const openWindow = vi.spyOn(window, "open").mockImplementation(() => null);
    render(<App />);

    const launcher = screen.getByRole("button", { name: /book a session/i });
    await user.click(launcher);

    const dialog = screen.getByRole("dialog", { name: /book a gaming session/i });
    expect(dialog).toHaveFocus();
    const dateInput = within(dialog).getByLabelText("Booking date");
    expect(dateInput.getAttribute("min")).toMatch(/^\d{4}-\d{2}-\d{2}$/);
    expect(within(dialog).getByLabelText("Number of players")).not.toHaveAttribute("max");

    await user.keyboard("{Escape}");
    expect(screen.queryByRole("dialog", { name: /book a gaming session/i })).not.toBeInTheDocument();
    expect(launcher).toHaveFocus();
    expect(openWindow).not.toHaveBeenCalled();

    openWindow.mockRestore();
  });

  it("makes the visit details and social links easy to reach", () => {
    render(<App />);

    expect(screen.getByText(/A-1\/114, Ratan Khand/i)).toBeInTheDocument();
    expect(screen.getByText("+91 99183 32386")).toBeInTheDocument();
    expect(screen.getByText(/message or call for current availability/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /follow on instagram/i })).toHaveAttribute(
      "href",
      "https://www.instagram.com/infamousgaming_cafe/",
    );
  });
});
