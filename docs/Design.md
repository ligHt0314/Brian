# Company Brain — Product and Interaction Design

Version: 1.0 · Prepared: 15 October 2026 · Implement against the DTOs in [Architecture.md](Architecture.md).

## 1. Design intent

Make an investigation easy to understand: the user should see the answer, the unresolved issues, and the evidence behind each conclusion. Give the product the feel of a calm operational workspace. Use readable typography, restrained color, and real source metadata. The graph has a specific purpose: explain the relationships supporting the selected finding.

Working name: **Company Brain**. Workspace: **Orbit Labs**. Main action: **Investigate**. Supporting promise: “Understand what changed and who it affects.” This is product copy, not a claim that all company knowledge has been captured.

## 2. Information architecture

| Route | Purpose | Primary action |
|---|---|---|
| `/` | Redirect to active investigation workspace | Start an investigation |
| `/investigate` | Question, answer, findings, evidence, graph | Ask / Rerun |
| `/investigate?run=<id>` | Authorized saved run; revalidate before showing | Rerun with current evidence |
| `/sources` | Indexed records, freshness, ingestion status | Import source |
| `/sources/<id>` | Authorized source revisions and excerpts | Inspect revision |
| `/reviews` | Internal review tasks | Open a task |
| `/history` | Private investigation history | Reopen / Rerun |

A narrow sidebar contains the four main destinations. The header shows workspace, scenario clock when enabled, and the demo identity. Source importing and fixture updates appear only for identities with that capability. Diagnostic tools stay behind an operator menu.

## 3. Desktop layout

Target viewport: 1440 × 900. Minimum supported interactive width: 360 px.

```text
┌──────────────┬─────────────────────────────────────────────────────────┐
│ Company      │ Orbit Labs                 Demo data • Engineer        │
│ Brain        ├─────────────────────────────────────────────────────────┤
│              │ Investigate Atlas SSO                                 │
│ Investigate  │ [What could block this launch?                 ] [Ask]│
│ Sources      │ Scope: indexed sources you can access                 │
│ Reviews      ├─────────────────────────────┬───────────────────────────┤
│ History      │ One known blocker          │ Evidence path             │
│              │ and an ownership conflict  │ Atlas → Auth → Directory  │
│              │                             │                    ↑      │
│              │ T-42 blocks Directory [1]  │                   T-42    │
│              │ Meridian commitment [2]    │                           │
│              │ Ownership disputed [3][4] │ [Path list] [Graph]       │
│              │                             │                           │
│              │ [Prepare review task]      │ Select an edge for source │
└──────────────┴─────────────────────────────┴───────────────────────────┘
```

Sidebar: 208 px. Main content: max-width 1440 px, 24 px padding. Investigation results use a 60/40 split with a minimum 420 px answer area. Evidence drawer opens from the right at 440 px wide; it can overlay the graph without obscuring the question. The default result tab is the readable path list. The graph is available beside it and is selected during the demo when useful.

At 768–1100 px, place the graph below the answer. Below 768 px, use a compact navigation row, stack content, and show evidence as a full-width dialog. Tables become cards where necessary. Horizontal scrolling is restricted to the graph canvas and code diagnostics, not the whole page.

## 4. Visual tokens

```css
:root {
  --bg: #f6f7f9;
  --surface: #ffffff;
  --surface-muted: #eef1f5;
  --text: #172033;
  --text-secondary: #4b586d;
  --border: #d9dfe8;
  --accent: #2556d8;
  --accent-soft: #e9efff;
  --success: #166534;
  --success-soft: #edf8f0;
  --warning: #92400e;
  --warning-soft: #fff6df;
  --danger: #b42318;
  --danger-soft: #fff0ee;
  --focus: #2556d8;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
}
```

Use a system sans-serif stack to avoid remote-font dependency. Body 15–16 px with 1.5 line height; page title 28 px/1.2; section title 18 px; metadata 13 px. Use monospace only for record IDs and operator diagnostics. Spacing scale: 4, 8, 12, 16, 24, 32, 48 px. Buttons at least 40 px high and touch targets at least 44 × 44 px where needed. Use one icon family consistently.

Color must accompany text/icons: “Conflicting sources,” “Stale source,” “Blocked,” “Source updated.” Validate actual text/background contrast during implementation; the token list alone is not accessibility certification. Avoid a green “Launch ready” badge because the indexed scope cannot establish that conclusion.

## 5. Investigation composer

Contains a project/entity selector, a multiline input, Ask button, and optional example questions. Example prompts invoke the real API and remain editable:

- “What could block Atlas SSO, and which customer commitment is affected?”
- “Who owns Directory Sync, and who has worked on it?”
- “What may be affected if Directory Sync becomes unavailable?”
- “Why did we rule out password fallback for Atlas SSO?”

Submit with the button or Cmd/Ctrl+Enter. Enter inserts a newline. During a run, retain the question and show real stages: “Finding the project,” “Following dependencies,” “Checking sources,” “Preparing findings.” Do not animate fake completion percentages.

If entity resolution is ambiguous, render selectable candidates with kind and an authorized distinguishing label. Clicking a candidate resubmits with its entity ID. If a follow-up reuses a session entity, show “Using Atlas SSO from this conversation” with a clear option to change it.

## 6. Answer anatomy

Order content as follows:

1. Result state and short supported summary.
2. Scope line: generated time, source update range, and “Based on the indexed sources you can access.”
3. Ranked findings cards.
4. Ownership/conflict cards.
5. Relevant decisions and supporting context.
6. Review action, if applicable.
7. Collapsed execution details with actual duration and query count.

A finding card includes a concise factual heading, affected project/customer when permitted, reason, citations, and “Show path.” A statement that depends on several claims must link all required evidence. Citation numbers are stable within one answer and map to evidence DTOs, not browser array indexes guessed by a component.

Keep factual observations, conditional impacts, and uncertainty distinguishable in copy. Example: “If Directory Sync is unavailable, Atlas SSO may be affected through Auth Gateway.” Do not convert reachability into a definite outage or delivery failure.

## 7. Evidence drawer

Clicking a citation, path step, or graph edge opens the same EvidenceDrawer. Display source title and type, exact excerpt with highlighted span, source updated time, indexed time, revision, evidence method, stale/current state, and related supported assertion. A source may contain multiple passages; the drawer starts at the cited one.

Use an internal authorized evidence route for fixtures. Show “Open original” only when a validated original URL exists. Do not invent Slack/Jira URLs for imported JSON. The metadata must identify imports honestly, such as “Chat export” or “Ticket export.”

If evidence becomes inaccessible, close its content and display “This evidence is no longer available to this session. Rerun the investigation.” Do not keep a stale sensitive excerpt mounted behind an error overlay. Historical revisions display a prominent “Historical revision” label and cannot masquerade as current evidence.

## 8. Relationship graph and accessible path list

Default to only the selected finding's path. Nodes use semantic shape/icon plus label: project, service, ticket, customer, commitment, person/team, decision. Edges show the human-readable predicate and preserve direction. For example T-42 **blocks** Directory Sync; the arrow must not point the opposite way just to make a layout neat.

Layout left-to-right with fixed type columns or a small deterministic layout function. Do not add a layout engine unless the fixed layout becomes inadequate. Selected path is blue; unrelated visible paths muted; conflicts amber; blocker tickets carry a red status icon. Selection highlights all citations supporting an edge. Display corroborating sources as a count only after permission filtering.

Keep at most 30 nodes and 50 edges. For truncation show “Showing the selected paths; more relationships may exist.” Zoom controls, reset view, and a textual path list are mandatory. Keyboard users can inspect each path as an ordered sequence of labeled links; graph drag/pan is not the only means of navigating evidence.

The UI must render backend-supplied edge/claim IDs. It cannot infer a relationship from spatial proximity or join arbitrary nodes because they share a label.

## 9. Conflict card and review action

ConflictCard shows the subject, disputed property, two or more assertions, source dates, source types, and evidence links. Example: “Directory Sync ownership needs confirmation,” with Platform from a runbook and Integrations from a chat. Explain that both claims are present in accessible current records. Do not automatically privilege the newest record.

Below it, show contributors separately: “People with relevant work: Maya Rao, Dev Shah,” each with contribution evidence. Label this as relevance, not confirmed ownership.

“Prepare review task” opens a preview with title, reason, referenced sources, selected assignee, and destination “Company Brain internal reviews.” The confirm button says “Create review task.” Until confirmed, show “Draft”; after success show the persistent task ID and link. Repeated clicks disable while pending and remain safe through server idempotency.

If the graph changed since preview, display “The evidence changed. Refresh this preview before creating the task.” Refresh generates a new proposal. External messaging controls are outside P0.

## 10. Sources and updates

Sources list columns: title, type, latest source update, last indexed, freshness, import state. Filters: type and import state. Search and counts include only permitted sources. Show actual imported record counts and job errors; avoid a decorative “all connected” indicator.

Import dialog: file picker, source type, source ID for updates, source timestamp, allowed group selection, and a short preview of parsed metadata. A user can only select groups permitted by their import capability. Source IDs and revision checks are normally prefilled when choosing “Update this source.”

On successful revision activation show “Updated. New investigations will use this revision.” A prior open answer shows “Sources changed since this answer” with Rerun. It must not silently replace the old answer while the user is inspecting it. After rerun, a compact changes section shows added/removed/changed findings; a resolution explanation must cite the new status evidence.

Pending extraction candidates show “Needs review” with the exact reason, such as “Unrecognized entity: Mercury.” P0 supports revising the registry/import and reimporting; it does not pretend that an unbuilt entity editing workflow exists.

## 11. State matrix

| State | User-facing behavior | Action |
|---|---|---|
| No sources | Explain that evidence is needed | Import if allowed; otherwise view demo instructions |
| Running | Real execution stage; question remains visible | Wait; stop local polling if desired |
| Supported | Facts and evidence; qualified scope | Inspect / follow up |
| Partial | Display supported findings and missing/truncated scope | Narrow question / inspect sources |
| Conflict | Display competing claims | Prepare review |
| Insufficient evidence | Explain what was searched without claiming absence | Try another entity / add a source |
| Clarification | Present permitted candidates | Select one |
| Needs refresh | Withhold unauthorized/invalidated stored answer body | Rerun |
| Model unavailable | Deterministic findings with explicit mode label | Inspect / retry |
| Graph unavailable | No fabricated answer; retryable error | Retry |
| Import failed | Prior indexed revision remains current | Inspect error / retry import |
| Access denied/missing | Same neutral unavailable message | Return to sources |

## 12. Accessibility and interaction quality

Use semantic headings, labels, buttons, and table headers. Give dialogs focus traps and return focus on close. Escape closes dialogs; visible focus rings remain on all controls. Announce stage changes politely through an aria-live region without continuously reading the entire answer. Support reduced motion and avoid flashing graph highlights. Status icons have text equivalents. Test keyboard access through question → answer citation → drawer → back to answer.

Persist only non-sensitive UI preferences in local storage. Keep session secrets in HttpOnly cookies. Clear rendered results immediately after changing persona. Disable authenticated response caching. Respect reduced-motion preferences; use at most 120–180 ms opacity/translation transitions where helpful.

## 13. Component inventory and completion checklist

Components: AppShell, WorkspaceHeader, DemoBanner, EntityPicker, QuestionComposer, RunProgress, AnswerSummary, FindingCard, ConflictCard, ContributorList, CitationButton, EvidenceDrawer, EvidencePathList, AnswerGraph, ScopeNotice, ChangesPanel, ReviewPreviewDialog, ReviewList, SourceTable, ImportDialog, JobStatus, EmptyState, RetryableError.

Before release, demonstrate the canonical journey at 1440 px and 390 px; confirm all actionable controls work; inspect empty/loading/error/permission states; verify graph and textual path agree; confirm no hidden content exists in response payloads; verify source-update labels; check keyboard navigation and contrast; remove mock metrics, fake sources, and dead controls.
