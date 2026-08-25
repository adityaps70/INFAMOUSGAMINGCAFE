# inFAMOUS Gaming Cafe — Premium Conversion-First Website Upgrade

Date: 2026-08-25
Status: Approved direction (Option A), implementation pending spec review

## 1. Goal

Upgrade the existing React/Vite static website into a premium, conversion-first gaming venue experience that feels credible, fast, modern, and complete on desktop and mobile, while preserving the intentionally low-maintenance static architecture.

The primary business outcome is to increase qualified visits and booking enquiries by making it easy for a visitor to understand what they can play, what it costs, why the venue is worth visiting, and how to book or reach the cafe.

## 2. Non-goals for this phase

This phase will not introduce:

- customer accounts or Google sign-in;
- a database or CMS;
- real-time station inventory;
- online payments;
- loyalty wallets;
- tournament management;
- an editorial/admin backend.

The code should remain structured so a data/CMS layer can be attached later without redesigning the public experience.

## 3. Current architecture and constraints

The current project is a React 19 + TypeScript + Vite static site. It already contains:

- hero and navigation;
- experience cards;
- rate explorer using local JSON data;
- social proof section;
- visit/contact information;
- WhatsApp booking modal;
- phone, Instagram, Maps and WhatsApp deep links;
- GitHub Pages deployment workflow;
- Vitest + Testing Library tests;
- responsive CSS and reduced-motion support.

The approved business phone, address, rate data, and existing external destinations remain the source of truth unless the owner supplies replacements.

## 4. Experience architecture

The upgraded page flow will be:

1. **Hero / Immediate decision** — what the venue is, strongest experiences, trust proof, and primary booking CTA.
2. **Choose Your Arena** — visually richer experience browser for PC, PlayStation, VR/simulation, cue/table games, social games and cafe/group sessions.
3. **How a Visit Works** — simple three-step journey: choose, enquire/confirm, arrive/play.
4. **Rate Finder** — fast category + item browsing with mobile-first controls and contextual booking CTA.
5. **Social Proof / Why inFAMOUS** — venue strengths and review themes without inventing testimonials.
6. **Gallery / Venue Proof** — polished layout with graceful placeholders only if authentic venue media is unavailable; no fabricated venue photography.
7. **Squads / Birthdays / Groups** — dedicated group-enquiry conversion section using WhatsApp prefill.
8. **FAQ** — practical questions that reduce booking friction.
9. **Visit / Contact** — address, phone, availability note, Instagram and directions.
10. **Persistent Mobile Actions** — Book, Call and Directions optimized for thumb reach and safe-area insets.

## 5. Visual direction

Retain the existing dark gaming identity, lime accent and red/orange energy, but reduce the current “template/card grid” feeling.

Design principles:

- strong black/near-black canvas;
- controlled neon accents rather than glow everywhere;
- large editorial typography and asymmetric composition;
- subtle grid/scanner/arena motifs;
- generous spacing and clearer hierarchy;
- motion used for feedback and atmosphere, never required for comprehension;
- no fake hardware specifications or unverifiable claims;
- real venue imagery preferred; placeholders must be clearly neutral and easy to replace.

## 6. Component design

### 6.1 SiteHeader

- desktop navigation remains visible;
- mobile navigation becomes an accessible menu or compact section navigator;
- booking CTA remains prominent;
- sticky behavior must not cover anchor targets;
- current-section feedback may be used only if lightweight and robust.

### 6.2 Hero

- stronger headline and supporting value proposition;
- primary booking CTA, secondary call/directions path;
- compact rating/certification proof;
- redesigned arena selector/panel that feels interactive without pretending to show live station availability;
- above-the-fold layout must remain legible at 320 px width and short mobile viewport heights.

### 6.3 ArenaExplorer

Replace the simple six-card grid with a richer, data-driven experience browser. Each experience may expose:

- title;
- short benefit-oriented description;
- category icon;
- compact tags such as competitive, group, immersive, casual;
- a contextual “check availability” action.

No unsupported game titles, hardware models, or inventory counts will be introduced.

### 6.4 VisitSteps

Three concise steps:

1. choose a mode;
2. send preferred date/time and group size;
3. receive WhatsApp confirmation and arrive.

This section exists to make the no-backend booking model feel deliberate rather than incomplete.

### 6.5 RateFinder

Keep the approved local rate JSON as canonical data.

Desktop:

- category tabs/segmented controls;
- clear rate table or price cards;
- strong active state;
- booking CTA that can carry the selected activity into the booking modal.

Mobile:

- no cramped desktop table dependency;
- horizontal category selector or dropdown with keyboard support;
- item rows/cards with half-hour and full-hour pricing clearly separated;
- no horizontal page overflow.

### 6.6 Gallery

Create a gallery system whose content is driven by a simple local data array.

If authentic venue photos are not included in the project, the implementation must not fabricate them. The section can use branded visual placeholders or be configured to hide unavailable slots cleanly until real media is added.

Images must use responsive sizing, explicit dimensions/aspect ratios where possible, lazy loading below the fold, and optimized file formats.

### 6.7 GroupSessions

Dedicated conversion section for:

- squads;
- birthdays/celebrations;
- college/friend groups;
- casual mini-events.

The CTA opens the same booking experience with the request type preselected/prefilled. It must not promise packages or discounts that have not been approved.

### 6.8 SocialProof

Use only verified rating value already present in project data and owner-approved review themes. Do not manufacture review quotes, reviewer names or counts.

The section should communicate:

- helpful staff;
- broad mix of gaming/activities;
- comfortable social/group environment;
- suitable experience for both newer and regular players.

### 6.9 FAQ

Data-driven accessible accordion covering practical topics such as:

- whether booking is required;
- how booking confirmation works;
- rates and extra-player note;
- group sessions;
- how to reach the venue;
- whether visitors can message for current availability.

Avoid asserting unsupported opening hours, food menu details, age limits or game inventory.

### 6.10 BookingDialog

Upgrade the current modal with:

- minimum date set to today in local browser date;
- validation for required fields;
- selected activity prefill when launched contextually;
- group/occasion prefill where relevant;
- clear session summary before submission;
- focus moved into dialog on open;
- focus trap while open;
- Escape closes;
- overlay click closes only when intentional;
- focus returns to launch control after close;
- body scroll lock restored correctly;
- keyboard navigation through all controls;
- mobile sheet layout where appropriate;
- explicit wording that WhatsApp enquiry is not an instant confirmed reservation.

Submission continues to build a WhatsApp URL and opens it safely in a new tab/window.

### 6.11 MobileActions

Upgrade to Book + Call + Directions where screen width allows, with:

- 44 px minimum interactive targets;
- safe-area bottom padding;
- no overlap with dialog content or footer;
- labels visible rather than icon-only ambiguity.

## 7. Data model

Keep editable public content in small local data modules rather than embedding copy throughout components.

Suggested modules:

- `siteData.ts` — identity/contact/trust metadata;
- `rates.json` — canonical rates;
- `experienceData.ts` or expanded `siteData.ts` — arena experiences/tags;
- `faqData.ts` — FAQ;
- `galleryData.ts` — authentic venue media references;
- `links.ts` — external URL builders and booking payload construction.

No server state is required.

## 8. Accessibility requirements

The upgrade must meet practical WCAG-oriented interaction standards:

- semantic landmarks and heading order;
- keyboard-accessible navigation, tabs, accordion and dialog;
- visible `:focus-visible` states;
- meaningful button/link names;
- no color-only state communication;
- sufficient text contrast;
- reduced-motion mode respected;
- dialog focus management;
- touch targets approximately 44×44 px or larger;
- form labels and validation messaging associated programmatically;
- decorative icons hidden from assistive technology.

## 9. Responsive requirements

Explicitly test at minimum:

- 320×568;
- 360×800;
- 390×844;
- 430×932;
- 768×1024;
- 1024×768;
- 1366×768;
- 1440×900.

Acceptance conditions:

- no horizontal page scroll;
- no clipped CTA labels;
- no overlapping sticky UI;
- booking dialog fully usable with virtual-keyboard-sized viewport constraints;
- rate finder readable without pinch zoom;
- nav usable on touch and keyboard;
- text does not overflow cards or controls;
- anchor navigation positions content below sticky header.

## 10. Performance and asset requirements

- preserve static-site deployment;
- optimize oversized logo/social assets without visible degradation;
- use responsive/lazy image loading for gallery media;
- avoid unnecessary JavaScript dependencies;
- keep animations CSS-first where possible;
- avoid render-blocking third-party scripts;
- maintain relative asset paths for GitHub Pages/custom-domain compatibility;
- build must complete with no TypeScript errors.

## 11. SEO and local conversion requirements

Retain and improve existing metadata/structured data where supported by approved facts:

- business name;
- Lucknow location/address;
- approved telephone;
- Instagram destination;
- social preview metadata;
- descriptive title and meta description;
- semantic page sections.

Do not publish conflicting third-party opening hours, phone numbers or unverifiable claims.

## 12. Testing strategy

### Automated unit/component tests

Add or extend tests for:

- every approved rate remains unchanged;
- contextual experience → booking prefill;
- group session → booking prefill;
- booking date cannot be before today;
- WhatsApp payload formatting;
- dialog open/close/focus behavior;
- Escape close;
- keyboard navigation for rate categories and FAQ;
- external link destinations;
- mobile navigation accessibility;
- content does not include prohibited/unverified claims.

### Build/static tests

Verify:

- required public assets exist;
- metadata and structured data remain valid;
- GitHub Pages workflow still runs tests before build;
- production `dist` includes required HTML/assets;
- no absolute development-only asset URLs leak into build.

### Browser verification

Run the production/dev build in a browser and manually verify:

- all main navigation links;
- all booking entry points;
- every rate category;
- WhatsApp payload generation;
- Call/Maps/Instagram links;
- dialog keyboard flow;
- gallery loading behavior;
- FAQ controls;
- mobile sticky actions;
- all defined viewport sizes;
- console errors/warnings;
- visual clipping/overflow.

## 13. Error and edge-case behavior

Because this is a static site:

- if `window.open` is blocked, the booking link should still be represented as a normal navigable action where feasible;
- missing optional gallery images must not break layout;
- empty optional notes must be excluded from the WhatsApp message;
- invalid or incomplete form input must not trigger WhatsApp;
- duplicate clicks must not create confusing UI state;
- reduced-motion users must not receive nonessential animation.

## 14. File-level implementation direction

Expected new or significantly revised areas:

- `src/App.tsx` — reordered page architecture and contextual booking state;
- `src/components/SiteHeader.tsx` — responsive nav;
- `src/components/Hero.tsx` — premium hero;
- `src/components/ExperienceGrid.tsx` or replacement `ArenaExplorer.tsx`;
- new `VisitSteps.tsx`;
- `src/components/RateCard.tsx` — mobile-first rate finder;
- new `Gallery.tsx`;
- new `GroupSessions.tsx`;
- `src/components/SocialProof.tsx` — stronger proof layout;
- new `Faq.tsx`;
- `src/components/Visit.tsx` — final conversion/visit section;
- `src/components/MobileActions.tsx` — Book/Call/Directions;
- `src/components/BookingForm.tsx` — accessible contextual booking flow;
- `src/siteData.ts` and supporting data modules;
- `src/links.ts` — richer booking payload helpers;
- `src/styles.css` — visual system and responsive behavior;
- test files — expanded coverage;
- `public/` — optimized assets and optional authentic venue images if supplied.

## 15. Definition of done

Option A is complete only when all of the following are true:

1. the redesigned page presents a coherent Explore → Choose → Trust → Price → Book → Visit journey;
2. mobile layouts are deliberately designed rather than desktop sections merely stacked;
3. every primary CTA works and leads to the intended call, map, Instagram or WhatsApp destination;
4. the booking flow is keyboard-accessible and correctly prefills contextual choices;
5. all owner-approved rates and contact data remain accurate;
6. no fabricated venue imagery, review quotes, inventory or hardware claims are introduced;
7. automated tests pass;
8. the production build passes;
9. browser verification passes at the defined viewport set without console errors or horizontal overflow;
10. the returned project remains deployable as a static GitHub Pages/custom-domain site.
