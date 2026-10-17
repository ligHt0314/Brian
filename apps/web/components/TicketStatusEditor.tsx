"use client";
import { useEffect, useState } from "react";
import {
  ArrowRight,
  LoaderCircle,
  ShieldCheck,
  TicketCheck,
} from "lucide-react";
import { api, post, type Source } from "@/lib/api/client";
import type { components } from "@/lib/api/schema";
type Ticket = components["schemas"]["TicketDetails"];
const statuses = [
  { value: "open", label: "Open" },
  { value: "in_progress", label: "In progress" },
  { value: "blocked", label: "Blocked" },
  { value: "done", label: "Done" },
  { value: "cancelled", label: "Cancelled" },
];
export default function TicketStatusEditor({
  sources,
  initialSource,
  onSave,
}: {
  sources: Source[];
  initialSource?: string;
  onSave: (id: string) => Promise<void>;
}) {
  const tickets = sources.filter((s) => s.kind === "ticket");
  const [source, setSource] = useState(initialSource || tickets[0]?.id || "");
  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [status, setStatus] = useState("done");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  useEffect(() => {
    let active = true;
    setTicket(null);
    setError("");
    if (source)
      api<Ticket>(`/sources/${encodeURIComponent(source)}/ticket`)
        .then((t) => {
          if (active) {
            setTicket(t);
            setStatus(t.status || "open");
          }
        })
        .catch((e) => {
          if (active)
            setError(e instanceof Error ? e.message : "Unable to load ticket.");
        });
    return () => {
      active = false;
    };
  }, [source]);
  const save = async () => {
    if (!ticket) return;
    setBusy(true);
    setError("");
    try {
      const result = await post<components["schemas"]["JobReceipt"]>(
        `/sources/${encodeURIComponent(source)}/ticket-status`,
        { expected_revision_id: ticket.expected_revision_id, status },
      );
      await onSave(result.job_ids[0]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unable to update ticket.");
    } finally {
      setBusy(false);
    }
  };
  return (
    <div className="ticketStatusForm">
      <p className="muted">
        Keep the source record up to date. Existing relationships and source
        history are preserved.
      </p>
      <label>
        Ticket
        <select
          aria-label="Ticket to update"
          value={source}
          disabled={busy}
          onChange={(e) => setSource(e.target.value)}
        >
          {tickets.map((t) => (
            <option key={t.id} value={t.id}>
              {t.title}
            </option>
          ))}
        </select>
      </label>
      {!ticket && source && !error && (
        <p className="muted">
          <LoaderCircle size={16} className="spin" /> Loading ticket…
        </p>
      )}
      {ticket && (
        <>
          <div className="ticketCurrent">
            <TicketCheck size={20} />
            <div>
              <strong>{ticket.title}</strong>
              <span>
                Current status:{" "}
                {statuses.find((s) => s.value === ticket.status)?.label ||
                  "Needs confirmation"}
              </span>
            </div>
          </div>
          <label>
            New status
            <select
              aria-label="New ticket status"
              value={status}
              disabled={busy}
              onChange={(e) => setStatus(e.target.value)}
            >
              {statuses.map((s) => (
                <option key={s.value} value={s.value}>
                  {s.label}
                </option>
              ))}
            </select>
          </label>
          <p className="ticketSaveNote">
            <ShieldCheck size={16} /> Saving creates a source revision. Rerun
            affected investigations to use the updated evidence.
          </p>
        </>
      )}
      {error && (
        <div className="errorBanner" role="alert">
          {error}
        </div>
      )}
      <button
        className="primary"
        disabled={busy || !ticket || ticket.status === status}
        onClick={save}
      >
        {busy ? (
          <LoaderCircle size={16} className="spin" />
        ) : (
          <ArrowRight size={16} />
        )}{" "}
        {busy ? "Saving…" : "Save status"}
      </button>
    </div>
  );
}
