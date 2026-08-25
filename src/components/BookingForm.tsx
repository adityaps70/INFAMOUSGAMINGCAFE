import { CalendarDays, MessageCircle, Users, X } from "lucide-react";
import {
  useEffect,
  useRef,
  useState,
  type ChangeEvent,
  type FormEvent,
  type KeyboardEvent as ReactKeyboardEvent,
  type MouseEvent,
} from "react";
import {
  activityOptions,
  getLocalDateInputMin,
  type BookingIntent,
} from "../booking";
import { buildBookingWhatsAppUrl } from "../links";

type BookingFormProps = {
  open: boolean;
  intent?: BookingIntent;
  onClose: () => void;
};

type BookingFormState = {
  name: string;
  game: string;
  date: string;
  time: string;
  duration: string;
  players: string;
  notes: string;
};

const initialState: BookingFormState = {
  name: "",
  game: "",
  date: "",
  time: "",
  duration: "Full hour",
  players: "1",
  notes: "",
};

const focusableSelector = [
  "button:not([disabled])",
  "a[href]",
  "input:not([disabled])",
  "select:not([disabled])",
  "textarea:not([disabled])",
  '[tabindex]:not([tabindex="-1"])',
].join(",");

export default function BookingForm({ open, intent = {}, onClose }: BookingFormProps) {
  const dialogRef = useRef<HTMLElement>(null);
  const returnFocusRef = useRef<HTMLElement | null>(null);
  const [formState, setFormState] = useState<BookingFormState>(initialState);

  useEffect(() => {
    if (!open) return;

    setFormState({
      ...initialState,
      game: intent.activity ?? "",
      notes: intent.notes ?? "",
      players: intent.requestType === "group" ? "" : "1",
    });

    returnFocusRef.current = document.activeElement as HTMLElement | null;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    dialogRef.current?.focus();

    return () => {
      document.body.style.overflow = previousOverflow;
      returnFocusRef.current?.focus();
    };
  }, [intent.activity, intent.notes, intent.requestType, open]);

  if (!open) return null;

  const updateField = (
    event: ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>,
  ) => {
    const { name, value } = event.currentTarget;
    setFormState((current) => ({ ...current, [name]: value }));
  };

  const handleKeyDown = (event: ReactKeyboardEvent<HTMLElement>) => {
    if (event.key === "Escape") {
      event.preventDefault();
      onClose();
      return;
    }

    if (event.key !== "Tab" || !dialogRef.current) return;

    const focusable = Array.from(
      dialogRef.current.querySelectorAll<HTMLElement>(focusableSelector),
    ).filter((element) => !element.hasAttribute("disabled"));

    if (!focusable.length) {
      event.preventDefault();
      dialogRef.current.focus();
      return;
    }

    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    const active = document.activeElement;

    if (event.shiftKey && (active === first || active === dialogRef.current)) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && active === last) {
      event.preventDefault();
      first.focus();
    }
  };

  const handleOverlayClick = (event: MouseEvent<HTMLDivElement>) => {
    if (event.target === event.currentTarget) onClose();
  };

  const openNativePicker = (event: MouseEvent<HTMLInputElement>) => {
    const input = event.currentTarget as HTMLInputElement & { showPicker?: () => void };

    if (typeof input.showPicker !== "function") return;

    try {
      input.showPicker();
    } catch {
      input.focus();
    }
  };

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!event.currentTarget.checkValidity()) {
      event.currentTarget.reportValidity();
      return;
    }

    const bookingUrl = buildBookingWhatsAppUrl({
      name: formState.name,
      game: formState.game,
      date: formState.date,
      time: formState.time,
      duration: formState.duration,
      players: formState.players,
      notes: formState.notes,
      requestType: intent.requestType,
    });

    window.open(bookingUrl, "_blank", "noopener,noreferrer");
  };

  const summaryActivity = formState.game || "Choose an activity";
  const summaryTiming =
    formState.date && formState.time
      ? `${formState.date} at ${formState.time}`
      : "Add your preferred date and time";
  const summaryPlayers = formState.players
    ? `${formState.players} player${formState.players === "1" ? "" : "s"}`
    : "Add group size";

  return (
    <div className="booking-overlay" onMouseDown={handleOverlayClick}>
      <section
        className="booking-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="booking-title"
        aria-describedby="booking-description"
        ref={dialogRef}
        tabIndex={-1}
        onKeyDown={handleKeyDown}
      >
        <div className="booking-heading">
          <div>
            <p className="section-kicker">
              {intent.requestType === "group" ? "Group session enquiry" : "Build your session"}
            </p>
            <h2 id="booking-title">Book a gaming session</h2>
            <p id="booking-description">
              Add your preference once. We’ll prepare a WhatsApp message for the cafe to confirm.
            </p>
          </div>
          <button
            className="booking-close"
            type="button"
            onClick={onClose}
            aria-label="Close booking form"
          >
            <X aria-hidden="true" />
          </button>
        </div>

        <form className="booking-form" onSubmit={handleSubmit}>
          <label>
            <span>Your name</span>
            <input
              name="name"
              type="text"
              autoComplete="name"
              value={formState.name}
              onChange={updateField}
              required
            />
          </label>

          <label>
            <span>Game or activity</span>
            <select
              name="game"
              value={formState.game}
              onChange={updateField}
              required
            >
              <option value="" disabled>
                Select your mode
              </option>
              {activityOptions.map((game) => (
                <option value={game} key={game}>
                  {game}
                </option>
              ))}
            </select>
          </label>

          <label>
            <span>Booking date</span>
            <span className="field-with-icon">
              <CalendarDays aria-hidden="true" />
              <input
                name="date"
                type="date"
                min={getLocalDateInputMin()}
                value={formState.date}
                onChange={updateField}
                onClick={openNativePicker}
                required
              />
            </span>
          </label>

          <label>
            <span>Preferred time</span>
            <input
              name="time"
              type="time"
              value={formState.time}
              onChange={updateField}
              onClick={openNativePicker}
              required
            />
          </label>

          <label>
            <span>Session duration</span>
            <select
              name="duration"
              value={formState.duration}
              onChange={updateField}
              required
            >
              <option>Half hour</option>
              <option>Full hour</option>
              <option>More than one hour</option>
            </select>
          </label>

          <label>
            <span>Number of players</span>
            <span className="field-with-icon">
              <Users aria-hidden="true" />
              <input
                name="players"
                type="number"
                min="1"
                value={formState.players}
                onChange={updateField}
                required
              />
            </span>
          </label>

          <label className="booking-notes">
            <span>Anything else?</span>
            <textarea
              name="notes"
              rows={3}
              value={formState.notes}
              onChange={updateField}
              placeholder="Game preference, occasion, or other request"
            />
          </label>

          <aside className="booking-summary" aria-label="Session request summary">
            <span>Request summary</span>
            <strong>{summaryActivity}</strong>
            <p>
              {summaryTiming} · {formState.duration} · {summaryPlayers}
            </p>
          </aside>

          <div className="booking-submit-row">
            <p>This sends an enquiry. Your session is confirmed only after the cafe replies.</p>
            <button className="button button-primary" type="submit">
              <MessageCircle aria-hidden="true" />
              Continue on WhatsApp
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}
