# inFAMOUS Premium Website Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the current static React/Vite landing page into a premium, mobile-first, conversion-focused inFAMOUS Gaming Cafe website with contextual WhatsApp booking, richer venue discovery, accessible interactions, and production-grade verification.

**Architecture:** Preserve the static React 19 + TypeScript + Vite architecture and existing canonical contact/rate data. Add small data-driven public-content modules, route all conversion entry points through a single contextual `BookingDialog`, keep external-link construction centralized in `links.ts`, and build the premium experience as focused React components composed by `App.tsx`. Styling remains CSS-first with no new runtime UI framework or backend dependency.

**Tech Stack:** React 19, TypeScript 7, Vite 8, lucide-react, Vitest, Testing Library, CSS, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-08-25-infamous-premium-upgrade-design.md`

## Global Constraints

- Remain a static-site deployment; do not add a database, CMS, auth, payments, live inventory, customer accounts, loyalty wallets, tournament management, or editorial/admin backend.
- Preserve the approved phone number, address, rates, Instagram destination, Maps destination, and existing external URLs unless supplied replacements exist in the repository.
- Do not introduce fabricated venue photography, review quotes, reviewer names/counts, hardware specifications, inventory counts, game-title availability, discounts, packages, or unsupported opening hours.
- Retain the dark gaming identity, lime `#c8ff2e`, red/orange `#ff1717`, and pure-black header while reducing excessive card/template treatment.
- Support keyboard interaction, visible `:focus-visible`, reduced motion, semantic landmarks, approximately 44×44 px touch targets, accessible dialog focus management, and associated form validation.
- Deliberately support 320×568, 360×800, 390×844, 430×932, 768×1024, 1024×768, 1366×768, and 1440×900 without horizontal page overflow or sticky-UI collisions.
- Keep animations CSS-first where possible and add no unnecessary JavaScript dependency.
- Preserve relative static asset paths compatible with GitHub Pages and a later custom domain.
- `npm test` and `npm run build` must pass with no TypeScript errors before completion.

---

## File Structure

### New files

- `src/booking.ts` — booking intent model, local-date input minimum, and reusable activity option derivation.
- `src/experienceData.ts` — arena-experience copy, tags, and icon keys.
- `src/faqData.ts` — approved practical FAQ copy only.
- `src/galleryData.ts` — authentic-media slots/placeholders; no fabricated venue photos.
- `src/components/ArenaExplorer.tsx` — premium experience browser and contextual booking entry points.
- `src/components/VisitSteps.tsx` — three-step no-backend booking explanation.
- `src/components/Gallery.tsx` — venue-proof section that handles absent real images cleanly.
- `src/components/GroupSessions.tsx` — squads/birthdays/groups WhatsApp conversion section.
- `src/components/Faq.tsx` — accessible disclosure/accordion section.
- `src/booking.test.ts` — booking date/intent utilities.

### Significantly revised files

- `src/App.tsx` — page order and contextual booking state.
- `src/components/SiteHeader.tsx` — accessible mobile navigation.
- `src/components/Hero.tsx` — premium hero and contextual arena actions.
- `src/components/RateCard.tsx` — mobile-first rate finder with contextual booking.
- `src/components/SocialProof.tsx` — verified-theme proof layout.
- `src/components/Visit.tsx` — final visit/contact conversion section.
- `src/components/MobileActions.tsx` — Book + Call + Directions.
- `src/components/BookingForm.tsx` — accessible contextual `BookingDialog` behavior.
- `src/siteData.ts` — approved venue/trust copy only; remove unsupported operational claim if unverified.
- `src/links.ts` — richer booking payload fields and safe URL composition.
- `src/styles.css` — complete premium visual/responsive system.
- `src/App.test.tsx` — interaction/regression coverage for the new page architecture.
- `src/siteData.test.ts` — canonical data and booking URL coverage.
- `src/staticFiles.test.ts` — metadata/build asset contract and optimized-asset assertions.
- `src/styles.test.ts` — mobile/action/accessibility CSS contract.
- `index.html` — final SEO/structured-data copy using approved facts only.
- `README.md` — current build/run/deploy and gallery-replacement guidance.

---

### Task 1: Booking Intent and Canonical Public Data

**Files:**
- Create: `src/booking.ts`
- Create: `src/booking.test.ts`
- Create: `src/experienceData.ts`
- Create: `src/faqData.ts`
- Create: `src/galleryData.ts`
- Modify: `src/siteData.ts`
- Modify: `src/links.ts`
- Modify: `src/siteData.test.ts`

**Interfaces:**
- Produces: `type BookingIntent = { activity?: string; requestType?: "standard" | "group"; notes?: string }`.
- Produces: `getLocalDateInputMin(date?: Date): string` returning `YYYY-MM-DD` in local-calendar terms.
- Produces: `activityOptions: readonly string[]` generated from canonical rate items plus `"VR / Simulation"`.
- Produces: `buildBookingWhatsAppUrl(details: BookingDetails): string`, where `BookingDetails` gains optional `requestType?: "standard" | "group"` and continues omitting blank notes.
- Produces: `experienceItems`, `faqItems`, and `galleryItems` data consumed by later presentation components.

- [ ] **Step 1: Write failing utility/data tests**

Add explicit tests similar to:

```ts
it("formats the browser-local booking minimum", () => {
  expect(getLocalDateInputMin(new Date(2026, 7, 25, 23, 30))).toBe("2026-08-25");
});

it("labels a group booking without inventing a package", () => {
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

it("does not publish unsupported inventory or hardware claims", () => {
  expect(JSON.stringify(experienceItems)).not.toMatch(/RTX|station count|available now/i);
});
```

- [ ] **Step 2: Run the focused tests and verify they fail**

Run: `npm test -- --run src/booking.test.ts src/siteData.test.ts`

Expected: FAIL because the new exports/types do not exist yet.

- [ ] **Step 3: Implement the minimal shared data and helpers**

Use a local-calendar formatter rather than UTC `toISOString()`:

```ts
export function getLocalDateInputMin(date = new Date()): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}
```

Move rich experience/FAQ/gallery content out of component files. Gallery entries without supplied images must use a neutral branded placeholder descriptor rather than a fake photo URL.

- [ ] **Step 4: Run focused tests and verify they pass**

Run: `npm test -- --run src/booking.test.ts src/siteData.test.ts`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/booking.ts src/booking.test.ts src/experienceData.ts src/faqData.ts src/galleryData.ts src/siteData.ts src/links.ts src/siteData.test.ts
git commit -m "feat: add contextual booking and public content data"
```

---

### Task 2: Accessible Contextual Booking Dialog

**Files:**
- Modify: `src/components/BookingForm.tsx`
- Modify: `src/App.test.tsx`

**Interfaces:**
- Consumes: `BookingIntent`, `activityOptions`, `getLocalDateInputMin`, `buildBookingWhatsAppUrl`.
- Produces: `BookingFormProps = { open: boolean; intent: BookingIntent; onClose: () => void }`.
- Behavior: selected activity/request type prefills form content; opening focuses the dialog; Tab/Shift+Tab stay within it; Escape and intentional backdrop click close; closing restores focus to the launcher; body scroll is restored.

- [ ] **Step 1: Add failing booking-dialog interaction tests**

Cover the required behavior with tests equivalent to:

```ts
await user.click(screen.getByRole("button", { name: /check availability for playstation/i }));
const dialog = screen.getByRole("dialog", { name: /book a gaming session/i });
expect(within(dialog).getByLabelText("Game or activity")).toHaveValue("PlayStation 5");
expect(within(dialog).getByLabelText("Booking date")).toHaveAttribute("min", expect.stringMatching(/^\d{4}-\d{2}-\d{2}$/));
expect(dialog).toContainElement(document.activeElement);

await user.keyboard("{Escape}");
expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
expect(document.activeElement).toBe(launcher);
```

Also assert group entry prefills the group request and that incomplete required input does not call `window.open`.

- [ ] **Step 2: Run the focused component tests and verify failure**

Run: `npm test -- --run src/App.test.tsx`

Expected: FAIL on missing contextual open/prefill and focus-management behavior.

- [ ] **Step 3: Implement dialog behavior without adding a dialog library**

Use refs and one effect:

```ts
const dialogRef = useRef<HTMLElement>(null);
const returnFocusRef = useRef<HTMLElement | null>(null);

useEffect(() => {
  if (!open) return;
  returnFocusRef.current = document.activeElement as HTMLElement | null;
  const previousOverflow = document.body.style.overflow;
  document.body.style.overflow = "hidden";
  requestAnimationFrame(() => dialogRef.current?.focus());
  return () => {
    document.body.style.overflow = previousOverflow;
    returnFocusRef.current?.focus();
  };
}, [open]);
```

Add `tabIndex={-1}` to the dialog, key handling for Escape and Tab trapping, `min={getLocalDateInputMin()}`, contextual defaults, clear required-field validation copy, a visible session-summary area, and the explicit statement that WhatsApp is an enquiry until confirmed by the cafe.

Backdrop close must check `event.target === event.currentTarget` so clicks inside never close the dialog.

- [ ] **Step 4: Run the focused tests and verify pass**

Run: `npm test -- --run src/App.test.tsx`

Expected: PASS for booking interaction cases completed so far.

- [ ] **Step 5: Commit**

```bash
git add src/components/BookingForm.tsx src/App.test.tsx
git commit -m "feat: make booking dialog contextual and accessible"
```

---

### Task 3: App Orchestration, Premium Header, and Hero

**Files:**
- Modify: `src/App.tsx`
- Modify: `src/components/SiteHeader.tsx`
- Modify: `src/components/Hero.tsx`
- Modify: `src/App.test.tsx`

**Interfaces:**
- Produces: `openBooking(intent?: BookingIntent): void` in `App`.
- `SiteHeader` consumes `onBook: (intent?: BookingIntent) => void` and owns only mobile-menu disclosure state.
- `Hero` consumes the same booking callback and may open generic or contextual booking intents.

- [ ] **Step 1: Add failing tests for mobile nav and hero conversion hierarchy**

```ts
expect(screen.getByRole("button", { name: /open navigation/i })).toHaveAttribute("aria-expanded", "false");
await user.click(screen.getByRole("button", { name: /open navigation/i }));
expect(screen.getByRole("navigation", { name: /mobile navigation/i })).toBeInTheDocument();

expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent(/play/i);
expect(screen.getByRole("button", { name: /book on whatsapp/i })).toBeInTheDocument();
expect(screen.getByRole("link", { name: /get directions/i })).toHaveAttribute("href", expect.stringContaining("google.com/maps"));
```

Assert no text implies live inventory (`ONLINE`, `available now`, station counts).

- [ ] **Step 2: Run focused tests and verify failure**

Run: `npm test -- --run src/App.test.tsx`

Expected: FAIL on the new mobile navigation contract and revised hero text/controls.

- [ ] **Step 3: Implement `App` booking intent state and responsive header/hero**

`App` should store:

```ts
const [bookingState, setBookingState] = useState<{ open: boolean; intent: BookingIntent }>({
  open: false,
  intent: {},
});
```

The mobile navigation toggle must expose `aria-expanded`/`aria-controls`, close after an anchor is selected, and never require JavaScript to make desktop anchor navigation usable. The hero arena panel must be framed as choices, not availability telemetry.

- [ ] **Step 4: Run focused tests and verify pass**

Run: `npm test -- --run src/App.test.tsx`

Expected: PASS for header/hero/orchestration cases.

- [ ] **Step 5: Commit**

```bash
git add src/App.tsx src/components/SiteHeader.tsx src/components/Hero.tsx src/App.test.tsx
git commit -m "feat: upgrade hero and responsive navigation"
```

---

### Task 4: Arena Explorer and Three-Step Visit Flow

**Files:**
- Create: `src/components/ArenaExplorer.tsx`
- Create: `src/components/VisitSteps.tsx`
- Delete: `src/components/ExperienceGrid.tsx`
- Modify: `src/App.tsx`
- Modify: `src/App.test.tsx`

**Interfaces:**
- `ArenaExplorer` consumes `onBook: (intent?: BookingIntent) => void` and `experienceItems`.
- `VisitSteps` is presentational and has no external state.
- Arena CTA opens `{ activity: item.bookingActivity }` where a canonical booking activity exists; generic modes may use a descriptive notes prefill instead.

- [ ] **Step 1: Add failing tests for experience discovery and contextual booking**

```ts
expect(screen.getByRole("heading", { name: /choose your arena/i })).toBeInTheDocument();
expect(screen.getByRole("heading", { name: /how your session works/i })).toBeInTheDocument();
await user.click(screen.getByRole("button", { name: /check availability for pc gaming/i }));
expect(within(screen.getByRole("dialog")).getByLabelText("Game or activity")).toHaveValue("PC Gaming");
```

Assert the explorer contains only approved experience categories and tags.

- [ ] **Step 2: Run tests and verify failure**

Run: `npm test -- --run src/App.test.tsx`

Expected: FAIL because the new sections do not exist.

- [ ] **Step 3: Build the explorer and visit steps**

Use semantic `<article>` items with icon, title, body, tags, and explicit per-card button names. Keep tags descriptive (`competitive`, `social`, `immersive`, `casual`) rather than equipment claims.

`VisitSteps` must describe exactly: choose → send preferred date/time/group size → receive WhatsApp confirmation and arrive.

- [ ] **Step 4: Run tests and verify pass**

Run: `npm test -- --run src/App.test.tsx`

Expected: PASS for experience/visit-flow cases.

- [ ] **Step 5: Commit**

```bash
git add src/App.tsx src/components/ArenaExplorer.tsx src/components/VisitSteps.tsx src/App.test.tsx
git rm src/components/ExperienceGrid.tsx
git commit -m "feat: add arena explorer and visit journey"
```

---

### Task 5: Mobile-First Rate Finder

**Files:**
- Modify: `src/components/RateCard.tsx`
- Modify: `src/App.tsx`
- Modify: `src/App.test.tsx`

**Interfaces:**
- `RateCard` consumes `onBook: (intent?: BookingIntent) => void`.
- Category controls implement roving keyboard behavior for ArrowLeft/ArrowRight/Home/End in addition to pointer clicks.
- Each rate item exposes a contextual booking action that opens `{ activity: item.name }`.

- [ ] **Step 1: Add failing tests for rate preservation, keyboard tab navigation, and contextual booking**

```ts
const gamingTab = screen.getByRole("tab", { name: "Gaming Room" });
gamingTab.focus();
await user.keyboard("{ArrowRight}");
expect(screen.getByRole("tab", { name: "Billiards" })).toHaveAttribute("aria-selected", "true");

await user.click(screen.getByRole("button", { name: /book playstation 5/i }));
expect(within(screen.getByRole("dialog")).getByLabelText("Game or activity")).toHaveValue("PlayStation 5");
```

Keep the existing exact half-hour/full-hour assertions for all canonical rate data.

- [ ] **Step 2: Run tests and verify failure**

Run: `npm test -- --run src/App.test.tsx src/siteData.test.ts`

Expected: FAIL on keyboard navigation and contextual booking.

- [ ] **Step 3: Implement rate finder behavior**

Keep semantic category tabs, add a small `activateTab(index)` helper, wrap indices for ArrowLeft/ArrowRight, and render price cells/cards so CSS can switch to stacked mobile rows without horizontal overflow. Each visible item gets a named `Book <activity>` button.

- [ ] **Step 4: Run tests and verify pass**

Run: `npm test -- --run src/App.test.tsx src/siteData.test.ts`

Expected: PASS, including unchanged rate values.

- [ ] **Step 5: Commit**

```bash
git add src/components/RateCard.tsx src/App.tsx src/App.test.tsx
git commit -m "feat: turn rates into a contextual mobile-first finder"
```

---

### Task 6: Social Proof, Gallery, Groups, FAQ, Visit, and Mobile Actions

**Files:**
- Create: `src/components/Gallery.tsx`
- Create: `src/components/GroupSessions.tsx`
- Create: `src/components/Faq.tsx`
- Modify: `src/components/SocialProof.tsx`
- Modify: `src/components/Visit.tsx`
- Modify: `src/components/MobileActions.tsx`
- Modify: `src/App.tsx`
- Modify: `src/App.test.tsx`

**Interfaces:**
- `GroupSessions` consumes `onBook: (intent?: BookingIntent) => void` and opens `{ requestType: "group", notes: "Group session enquiry" }`.
- `Faq` consumes `faqItems` and uses native `<details>/<summary>` or equivalent accessible disclosure without a new library.
- `Gallery` consumes `galleryItems`; missing image sources render branded non-photographic placeholders.
- `MobileActions` consumes `onBook` and uses canonical `buildTelUrl()` and `mapsUrl`.

- [ ] **Step 1: Add failing section and accessibility tests**

```ts
expect(screen.getByRole("heading", { name: /venue/i })).toBeInTheDocument();
expect(screen.getByRole("heading", { name: /bring the whole squad/i })).toBeInTheDocument();
expect(screen.getByRole("heading", { name: /questions before you play/i })).toBeInTheDocument();

await user.click(screen.getByRole("button", { name: /plan a group session/i }));
expect(screen.getByRole("dialog")).toHaveTextContent(/group session/i);

const quickActions = screen.getByRole("navigation", { name: /quick booking actions/i });
expect(within(quickActions).getByRole("link", { name: /directions/i })).toHaveAttribute("href", mapsUrl);
```

Add a prohibited-copy assertion covering invented review quotes/counts and unsupported opening-hours wording.

- [ ] **Step 2: Run tests and verify failure**

Run: `npm test -- --run src/App.test.tsx`

Expected: FAIL because the sections and third mobile action do not yet exist.

- [ ] **Step 3: Implement all remaining conversion sections**

Use only `reviewThemes` and approved rating data in social proof. For gallery placeholders, render branded blocks with accessible text such as `"Venue photo slot — replace with authentic inFAMOUS media"` only in source/development copy if appropriate; public-facing copy should remain polished, e.g. `"Inside inFAMOUS"` + visual motif, without pretending a motif is a photograph.

Use native disclosure markup for FAQ unless browser testing demonstrates a reason not to. Remove or generalize any unverified `closingNote` display; use `"Message or call for current availability"` instead.

- [ ] **Step 4: Run tests and verify pass**

Run: `npm test -- --run src/App.test.tsx`

Expected: PASS for sections, group prefill, FAQ semantics, and mobile actions.

- [ ] **Step 5: Commit**

```bash
git add src/components/Gallery.tsx src/components/GroupSessions.tsx src/components/Faq.tsx src/components/SocialProof.tsx src/components/Visit.tsx src/components/MobileActions.tsx src/App.tsx src/App.test.tsx
git commit -m "feat: complete trust and conversion sections"
```

---

### Task 7: Premium Responsive Visual System and Asset Optimization

**Files:**
- Modify: `src/styles.css`
- Modify: `src/styles.test.ts`
- Modify: `src/staticFiles.test.ts`
- Modify: `public/logo.png`
- Modify: `public/og.png`

**Interfaces:**
- Styling contract must preserve `--lime: #c8ff2e`, `--orange: #ff1717`, pure-black `.site-header`, `:focus-visible`, reduced-motion media query, `env(safe-area-inset-bottom)`, `@media (max-width: 760px)`, and `@media (min-width: 1000px)`.
- Mobile action targets must have a CSS minimum block size of at least `44px`.
- Anchor sections must account for sticky header with `scroll-margin-top`.

- [ ] **Step 1: Tighten failing stylesheet/static-asset tests around the accepted design**

Add assertions such as:

```ts
expect(css).toContain("scroll-margin-top");
expect(css).toMatch(/\.mobile-actions[\s\S]*min-height:\s*44px/);
expect(css).toContain("overflow-x: clip");
```

Change the oversized-asset assertions from “greater than” to reasonable upper bounds after measuring current visual dimensions, while keeping enough quality for the logo/social preview.

- [ ] **Step 2: Run style/static tests and verify failure**

Run: `npm test -- --run src/styles.test.ts src/staticFiles.test.ts`

Expected: FAIL on the new responsive/asset requirements before optimization.

- [ ] **Step 3: Rework CSS section-by-section and optimize PNG assets losslessly/visually safely**

Implement deliberate layouts for:

- 320–430 px: compact header/menu, hero without viewport overflow, stacked arena/rates, bottom Book/Call/Directions, sheet-like booking dialog;
- 768 px: tablet grids and no bottom-action collisions;
- 1000+ px: asymmetric editorial hero, richer arena/rates/gallery compositions;
- short desktop heights: no oversized hero that hides primary action;
- all sizes: `overflow-x: clip`, `scroll-margin-top`, focus rings, reduced motion, 44 px controls, safe-area padding.

Optimize existing PNGs with an available lossless/near-lossless encoder while preserving visible quality and dimensions required by metadata/layout.

- [ ] **Step 4: Run style/static tests and full component tests**

Run: `npm test`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/styles.css src/styles.test.ts src/staticFiles.test.ts public/logo.png public/og.png
git commit -m "style: deliver premium responsive gaming experience"
```

---

### Task 8: SEO, Documentation, Production Build, and Browser Verification

**Files:**
- Modify: `index.html`
- Modify: `README.md`
- Modify: `src/staticFiles.test.ts`
- Modify: `.github/workflows/deploy-pages.yml` only if verification shows the current workflow no longer matches package commands.

**Interfaces:**
- Production build remains `npm run build` and output remains `dist/`.
- Metadata includes approved business name, Lucknow/address, approved phone, Instagram, descriptive title/description, relative `./og.png`, and valid JSON-LD without unsupported hours.
- README documents `npm ci`, `npm test`, `npm run build`, `npm run dev`, static deployment, and how to replace gallery placeholders with authentic images.

- [ ] **Step 1: Add/adjust failing static metadata tests**

```ts
expect(html).toContain('property="og:image" content="./og.png"');
expect(html).toContain('"telephone": "+919918332386"');
expect(html).not.toMatch(/openingHours|9:30 PM/i);
expect(workflow).toContain("npm test");
expect(workflow).toContain("npm run build");
```

- [ ] **Step 2: Run static tests and verify failure if unsupported metadata remains**

Run: `npm test -- --run src/staticFiles.test.ts`

Expected: FAIL if old unsupported operational data or documentation contract remains.

- [ ] **Step 3: Update metadata and README, then install dependencies cleanly**

Run:

```bash
npm ci
npm test
npm run build
```

Expected: all tests PASS; TypeScript/Vite build succeeds; `scripts/verify-dist.mjs` succeeds.

- [ ] **Step 4: Start the built site and perform browser verification at every required viewport**

Run one local server for verification, then inspect 320×568, 360×800, 390×844, 430×932, 768×1024, 1024×768, 1366×768, and 1440×900.

At every relevant breakpoint verify:

- no horizontal page scroll;
- no clipped labels or overlapping sticky UI;
- header navigation works with pointer and keyboard;
- all booking launchers open the same dialog with correct context;
- required booking validation blocks incomplete submission;
- Escape closes and focus returns;
- rate tabs switch by click and keyboard;
- every category displays canonical rates;
- FAQ disclosures work;
- gallery placeholders/images do not shift or break layout;
- Book/Call/Directions mobile actions remain usable above safe area;
- Maps, Instagram, phone, and generated WhatsApp destinations are correct;
- no console errors or React warnings.

- [ ] **Step 5: Fix any browser-only defects and rerun the complete verification suite**

Run:

```bash
npm test
npm run build
```

Expected: PASS after any fixes; repeat browser checks for any viewport affected by a fix.

- [ ] **Step 6: Commit the production-ready state**

```bash
git add index.html README.md src/staticFiles.test.ts .github/workflows/deploy-pages.yml
git add -u
git commit -m "chore: verify premium site for production deployment"
```

---

## Final Acceptance Gate

Before calling the upgrade complete:

- [ ] `git status --short` is clean except deliberately untracked deliverables.
- [ ] `npm test` passes with zero failed tests.
- [ ] `npm run build` passes and `dist/` verification succeeds.
- [ ] All eight required viewport checks pass without horizontal overflow or console errors.
- [ ] Canonical rate assertions still match `src/rates.json` exactly.
- [ ] No unsupported hours, fake review quotes, fabricated venue photos, hardware/inventory claims, or backend/account/payment claims appear in public content.
- [ ] Every booking entry point and external CTA is manually verified.
- [ ] The final source remains a static deployable Vite project.
