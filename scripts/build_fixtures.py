"""Build BrightMart's reproducible, entirely fictional retail company.
Reviewed fixture claims are anchored to exact readable passages, never canned answers.
Run this script to regenerate JSON records, manifest, human-readable handbook and UI guide.
"""

import json
from collections import Counter
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "fixtures/brightmart"
BASE_ENTITIES = [
    {
        "id": "project:easy-checkout",
        "kind": "Project",
        "label": "Easy Checkout",
        "aliases": ["Checkout Launch", "checkout launch", "Launch"],
    },
    {
        "id": "project:sales-dashboard",
        "kind": "Project",
        "label": "Sales Dashboard",
        "aliases": ["Dashboard", "Launch"],
    },
    {
        "id": "project:delivery-tracking",
        "kind": "Project",
        "label": "Delivery Tracking",
        "aliases": ["Delivery"],
    },
    {"id": "service:checkout", "kind": "Service", "label": "Checkout Service", "aliases": []},
    {"id": "service:payments", "kind": "Service", "label": "Payment Gateway", "aliases": ["Payments"]},
    {"id": "service:reporting", "kind": "Service", "label": "Reporting Service", "aliases": []},
    {"id": "service:messages", "kind": "Service", "label": "Customer Messages", "aliases": []},
    {"id": "team:payments", "kind": "Team", "label": "Payments", "aliases": []},
    {"id": "team:integrations", "kind": "Team", "label": "Integrations", "aliases": []},
    {"id": "team:data", "kind": "Team", "label": "Data Systems", "aliases": []},
    {"id": "person:maya", "kind": "Person", "label": "Maya Rao", "aliases": ["Maya"]},
    {"id": "person:dev", "kind": "Person", "label": "Dev Shah", "aliases": ["Dev"]},
    {"id": "person:leah", "kind": "Person", "label": "Leah Chen", "aliases": ["Leah"]},
    {"id": "person:omar", "kind": "Person", "label": "Omar Ali", "aliases": ["Omar"]},
    {"id": "person:nina", "kind": "Person", "label": "Nina Park", "aliases": ["Nina"]},
    {"id": "person:eli", "kind": "Person", "label": "Eli Morgan", "aliases": ["Eli"]},
    {
        "id": "customer:green-basket",
        "kind": "Customer",
        "label": "Green Basket Stores",
        "aliases": ["Green Basket"],
    },
    {"id": "customer:daily-essentials", "kind": "Customer", "label": "Daily Essentials", "aliases": []},
    {"id": "ticket:T-101", "kind": "Ticket", "label": "T-101", "aliases": []},
    {"id": "ticket:T-102", "kind": "Ticket", "label": "T-102", "aliases": []},
    {"id": "ticket:T-103", "kind": "Ticket", "label": "T-103", "aliases": []},
    {"id": "ticket:T-104", "kind": "Ticket", "label": "T-104", "aliases": []},
    {"id": "ticket:T-105", "kind": "Ticket", "label": "T-105", "aliases": []},
    {"id": "ticket:T-106", "kind": "Ticket", "label": "T-106", "aliases": []},
    {"id": "ticket:T-107", "kind": "Ticket", "label": "T-107", "aliases": []},
    {"id": "ticket:T-108", "kind": "Ticket", "label": "T-108", "aliases": []},
    {"id": "decision:D-101", "kind": "Decision", "label": "D-101", "aliases": []},
    {"id": "decision:D-102", "kind": "Decision", "label": "D-102", "aliases": []},
    {"id": "decision:D-103", "kind": "Decision", "label": "D-103", "aliases": []},
    {"id": "decision:D-104", "kind": "Decision", "label": "D-104", "aliases": []},
    {"id": "commitment:C-101", "kind": "Commitment", "label": "C-101", "aliases": []},
    {"id": "commitment:C-102", "kind": "Commitment", "label": "C-102", "aliases": []},
    {"id": "commitment:C-103", "kind": "Commitment", "label": "C-103", "aliases": []},
]
CORE = [
    [
        "directory:brightmart",
        "directory",
        "BrightMart · team directory",
        ["all_employees"],
        "2026-10-14T04:00:00Z",
        "Synthetic organization directory. All registry names and aliases are shared with employees.",
        [
            ["person:maya", "MEMBER_OF", "team:payments", None, "Maya Rao is a member of Payments."],
            ["person:dev", "MEMBER_OF", "team:integrations", None, "Dev Shah is a member of Integrations."],
            ["person:leah", "MEMBER_OF", "team:payments", None, "Leah Chen is a member of Payments."],
            ["person:omar", "MEMBER_OF", "team:data", None, "Omar Ali is a member of Data Systems."],
            ["person:nina", "MEMBER_OF", "team:integrations", None, "Nina Park is a member of Integrations."],
            ["person:eli", "MEMBER_OF", "team:data", None, "Eli Morgan is a member of Data Systems."],
        ],
    ],
    [
        "doc:checkout-architecture",
        "document",
        "Easy Checkout · architecture",
        ["engineering"],
        "2026-10-14T04:00:00Z",
        "Payment confirmation relies on confirmed bank payments. Dependency changes require a release review.",
        [
            [
                "project:easy-checkout",
                "USES",
                "service:checkout",
                None,
                "Easy Checkout uses Checkout Service.",
            ],
            [
                "service:checkout",
                "DEPENDS_ON",
                "service:payments",
                None,
                "Checkout Service depends on Payment Gateway.",
            ],
            [
                "service:checkout",
                "OWNED_BY",
                "team:payments",
                None,
                "Checkout Service has primary owner Payments.",
            ],
            ["person:maya", "WORKED_ON", "service:checkout", None, "Maya Rao worked on Checkout Service."],
            ["person:leah", "WORKED_ON", "project:easy-checkout", None, "Leah Chen worked on Easy Checkout."],
        ],
    ],
    [
        "doc:payments-runbook",
        "document",
        "Payment Gateway · operational runbook",
        ["engineering"],
        "2026-08-20T04:00:00Z",
        "Runbook from the previous operating cycle. Confirm ownership before paging a team.",
        [
            [
                "service:payments",
                "OWNED_BY",
                "team:payments",
                None,
                "Payment Gateway has primary owner Payments.",
            ],
            ["person:maya", "WORKED_ON", "service:payments", None, "Maya Rao worked on Payment Gateway."],
        ],
    ],
    [
        "doc:green-basket-rollout",
        "document",
        "Green Basket Stores · rollout commitment",
        ["engineering"],
        "2026-10-14T04:00:00Z",
        "The promised rollout includes payment confirmation. This is synthetic customer information.",
        [
            ["commitment:C-101", "REQUIRES", "project:easy-checkout", None, "C-101 requires Easy Checkout."],
            [
                "commitment:C-101",
                "MADE_TO",
                "customer:green-basket",
                None,
                "C-101 is made to Green Basket Stores.",
            ],
            ["commitment:C-101", "DUE_ON", None, "2026-10-18", "C-101 is due on 2026-10-18."],
        ],
    ],
    [
        "doc:checkout-brief",
        "document",
        "Easy Checkout · project brief",
        ["all_employees"],
        "2026-10-14T04:00:00Z",
        "Easy Checkout is our faster online checkout project. Alias: Checkout Launch. Its technical dependencies are "
        "documented in engineering records.",
        [["person:leah", "WORKED_ON", "project:easy-checkout", None, "Leah Chen worked on Easy Checkout."]],
    ],
    [
        "doc:dashboard-overview",
        "document",
        "Sales Dashboard · project overview",
        ["all_employees"],
        "2026-10-14T04:00:00Z",
        "",
        [
            [
                "project:sales-dashboard",
                "USES",
                "service:reporting",
                None,
                "Sales Dashboard uses Reporting Service.",
            ],
            [
                "service:reporting",
                "OWNED_BY",
                "team:data",
                None,
                "Reporting Service has primary owner Data Systems.",
            ],
            [
                "commitment:C-102",
                "REQUIRES",
                "project:sales-dashboard",
                None,
                "C-102 requires Sales Dashboard.",
            ],
            [
                "commitment:C-102",
                "MADE_TO",
                "customer:daily-essentials",
                None,
                "C-102 is made to Daily Essentials.",
            ],
            ["commitment:C-102", "DUE_ON", None, "2026-10-30", "C-102 is due on 2026-10-30."],
        ],
    ],
    [
        "doc:leadership-note",
        "document",
        "Leadership · commercial planning",
        ["leadership"],
        "2026-10-14T04:00:00Z",
        "CONFIDENTIAL_BRIGHTMART_COPPER_731. Fictional leadership-only commercial planning marker.",
        [
            [
                "project:easy-checkout",
                "OWNED_BY",
                "person:leah",
                None,
                "Easy Checkout has primary owner Leah Chen.",
            ]
        ],
    ],
    [
        "chat:handoff",
        "chat",
        "Engineering handoff · Payment Gateway",
        ["engineering"],
        "2026-10-14T04:00:00Z",
        "Exported conversation, 14 October. The earlier runbook has not been reconciled with this handoff claim.",
        [
            [
                "service:payments",
                "OWNED_BY",
                "team:integrations",
                None,
                "Payment Gateway now has primary owner Integrations.",
            ],
            ["person:dev", "WORKED_ON", "service:payments", None, "Dev Shah worked on Payment Gateway."],
        ],
    ],
    [
        "chat:payments-help",
        "chat",
        "Payment Gateway · implementation help",
        ["engineering"],
        "2026-10-14T04:00:00Z",
        "Maya and Dev shared their implementation experience. Contribution is not formal ownership.",
        [
            ["person:maya", "WORKED_ON", "service:payments", None, "Maya Rao worked on Payment Gateway."],
            ["person:dev", "WORKED_ON", "service:payments", None, "Dev Shah worked on Payment Gateway."],
            ["person:nina", "WORKED_ON", "service:checkout", None, "Nina Park worked on Checkout Service."],
        ],
    ],
    [
        "chat:checkout-planning",
        "chat",
        "Checkout Launch · release planning",
        ["engineering"],
        "2026-10-14T04:00:00Z",
        "Planning discussion: investigate dependencies and the customer promise before release review.",
        [
            ["person:leah", "WORKED_ON", "project:easy-checkout", None, "Leah Chen worked on Easy Checkout."],
            ["person:maya", "WORKED_ON", "project:easy-checkout", None, "Maya Rao worked on Easy Checkout."],
            ["person:dev", "WORKED_ON", "service:checkout", None, "Dev Shah worked on Checkout Service."],
        ],
    ],
    [
        "chat:dashboard-planning",
        "chat",
        "Dashboard · planning notes",
        ["all_employees"],
        "2026-10-14T04:00:00Z",
        "",
        [
            [
                "person:omar",
                "WORKED_ON",
                "project:sales-dashboard",
                None,
                "Omar Ali worked on Sales Dashboard.",
            ],
            ["person:eli", "WORKED_ON", "service:reporting", None, "Eli Morgan worked on Reporting Service."],
        ],
    ],
    [
        "chat:ambiguous-alias",
        "chat",
        "Shared Launch alias · naming discussion",
        ["all_employees"],
        "2026-10-14T04:00:00Z",
        "Both Easy Checkout and Sales Dashboard are sometimes called Launch. Ask which project is intended.\n\n",
        [],
    ],
    [
        "ticket:T-101",
        "ticket",
        "T-101 · Payment confirmation check",
        ["engineering"],
        "2026-10-17T03:30:00Z",
        "",
        [
            ["ticket:T-101", "BLOCKS", "service:payments", None, "T-101 blocks Payment Gateway."],
            ["ticket:T-101", "STATUS", None, "blocked", "T-101 has status blocked."],
        ],
    ],
    [
        "ticket:T-102",
        "ticket",
        "T-102 · Checkout smoke tests",
        ["engineering"],
        "2026-10-17T03:30:00Z",
        "",
        [
            ["ticket:T-102", "BLOCKS", "service:checkout", None, "T-102 blocks Checkout Service."],
            ["ticket:T-102", "STATUS", None, "done", "T-102 has status done."],
        ],
    ],
    [
        "ticket:T-103",
        "ticket",
        "T-103 · Analytics backfill",
        ["all_employees"],
        "2026-10-17T03:30:00Z",
        "",
        [
            ["ticket:T-103", "BLOCKS", "service:reporting", None, "T-103 blocks Reporting Service."],
            ["ticket:T-103", "STATUS", None, "open", "T-103 has status open."],
        ],
    ],
    [
        "ticket:T-104",
        "ticket",
        "T-104 · Notification delivery",
        ["engineering"],
        "2026-10-17T03:30:00Z",
        "",
        [
            ["ticket:T-104", "BLOCKS", "service:messages", None, "T-104 blocks Customer Messages."],
            ["ticket:T-104", "STATUS", None, "in_progress", "T-104 has status in_progress."],
        ],
    ],
    [
        "ticket:T-105",
        "ticket",
        "T-105 · Old payment cleanup",
        ["engineering"],
        "2026-10-17T03:30:00Z",
        "",
        [
            ["ticket:T-105", "BLOCKS", "service:payments", None, "T-105 blocks Payment Gateway."],
            ["ticket:T-105", "STATUS", None, "cancelled", "T-105 has status cancelled."],
        ],
    ],
    [
        "ticket:T-106",
        "ticket",
        "T-106 · Payment reconciliation review",
        ["engineering"],
        "2026-10-17T03:30:00Z",
        "",
        [
            ["ticket:T-106", "BLOCKS", "service:payments", None, "T-106 blocks Payment Gateway."],
            ["ticket:T-106", "STATUS", None, "done", "T-106 has status done."],
            ["person:maya", "WORKED_ON", "ticket:T-106", None, "Maya Rao worked on T-106."],
            ["person:dev", "WORKED_ON", "ticket:T-106", None, "Dev Shah worked on T-106."],
        ],
    ],
    [
        "ticket:T-107",
        "ticket",
        "T-107 · Notification metrics",
        ["engineering"],
        "2026-10-17T03:30:00Z",
        "",
        [
            ["ticket:T-107", "BLOCKS", "service:messages", None, "T-107 blocks Customer Messages."],
            ["ticket:T-107", "STATUS", None, "done", "T-107 has status done."],
        ],
    ],
    [
        "ticket:T-108",
        "ticket",
        "T-108 · Untriaged delivery check",
        ["engineering"],
        "2026-10-17T03:30:00Z",
        "",
        [["ticket:T-108", "BLOCKS", "service:messages", None, "T-108 blocks Customer Messages."]],
    ],
    [
        "decision:D-101",
        "decision",
        "D-101 · Payment confirmation requirement",
        ["engineering"],
        "2026-10-14T04:00:00Z",
        "",
        [
            [
                "decision:D-101",
                "ABOUT",
                "project:easy-checkout",
                None,
                "D-101 is about Easy Checkout: payment confirmation is required; unconfirmed payments is ruled out because Green "
                "Basket Stores requires confirmed payment before an order is accepted for the promised rollout.",
            ]
        ],
    ],
    [
        "decision:D-102",
        "decision",
        "D-102 · Checkout payment validation",
        ["engineering"],
        "2026-10-14T04:00:00Z",
        "",
        [
            [
                "decision:D-102",
                "ABOUT",
                "service:checkout",
                None,
                "D-102 is about Checkout Service: validate payment reference before issuing a order confirmation.",
            ]
        ],
    ],
    [
        "decision:D-103",
        "decision",
        "D-103 · Analytics backfill",
        ["all_employees"],
        "2026-10-14T04:00:00Z",
        "",
        [
            [
                "decision:D-103",
                "ABOUT",
                "project:sales-dashboard",
                None,
                "D-103 is about Sales Dashboard: complete the backfill before the analytics review.",
            ]
        ],
    ],
    [
        "decision:D-104",
        "decision",
        "D-104 · Payment audit trail",
        ["engineering"],
        "2026-06-01T04:00:00Z",
        "",
        [
            [
                "decision:D-104",
                "ABOUT",
                "service:payments",
                None,
                "D-104 is about Payment Gateway: keep a payment audit trail for operational investigation.",
            ]
        ],
    ],
]
entities = list(BASE_ENTITIES)
sources = []


def entity(id, kind, label, aliases=()):
    entities.append(dict(id=id, kind=kind, label=label, aliases=list(aliases)))
    return id


projects = [e["id"] for e in entities if e["kind"] == "Project"]
for slug, label in [
    ("quick-refunds", "Quick Refunds"),
    ("stock-alerts", "Stock Alerts"),
    ("store-pickup", "Store Pickup"),
    ("customer-rewards", "Customer Rewards"),
    ("seller-dashboard", "Seller Dashboard"),
    ("help-center", "Help Center"),
    ("fresh-subscriptions", "Fresh Subscriptions"),
]:
    projects.append(entity("project:" + slug, "Project", label))
services = [e["id"] for e in entities if e["kind"] == "Service"]
for slug, label in [
    ("delivery-board", "Delivery Board"),
    ("route-planner", "Route Planner"),
    ("refunds", "Refund Service"),
    ("inventory", "Stock Counter"),
    ("catalog", "Product Catalog"),
    ("loyalty", "Rewards Wallet"),
    ("seller-portal", "Seller Portal"),
    ("support", "Help Desk"),
    ("billing", "Subscription Billing"),
    ("warehouse", "Warehouse Updates"),
    ("pickup", "Pickup Scheduler"),
    ("search", "Product Search"),
]:
    services.append(entity("service:" + slug, "Service", label))
teams = [e["id"] for e in entities if e["kind"] == "Team"]
for slug, label in [
    ("delivery", "Delivery Operations"),
    ("shopping", "Shopping Experience"),
    ("customer-care", "Customer Care"),
    ("retail-ops", "Store Operations"),
    ("reliability", "Site Reliability"),
]:
    teams.append(entity("team:" + slug, "Team", label))
people = [e["id"] for e in entities if e["kind"] == "Person"]
for name in [
    "Aarav Mehta",
    "Isha Patel",
    "Rohan Das",
    "Ananya Sen",
    "Kabir Khan",
    "Meera Nair",
    "Arjun Iyer",
    "Sara Thomas",
    "Vikram Joshi",
    "Diya Kapoor",
    "Neel Gupta",
    "Tara Bose",
    "Aditya Rao",
    "Zoya Malik",
    "Rehan Shah",
    "Anika Jain",
    "Kiran Menon",
    "Pooja Desai",
    "Amit Verma",
    "Sana Sheikh",
    "Raj Malhotra",
    "Nisha Reddy",
    "Varun Sethi",
    "Riya Bhat",
    "Yash Kulkarni",
    "Aditi Roy",
    "Manav Suri",
    "Simran Kaur",
    "Siddharth Pai",
    "Kavya Rao",
    "Ibrahim Noor",
    "Priya Dutta",
    "Harsh Arora",
    "Lina Fernandes",
]:
    people.append(entity("person:" + name.lower().replace(" ", "-"), "Person", name))
customers = [e["id"] for e in entities if e["kind"] == "Customer"]
for slug, label in [
    ("sunrise", "Sunrise Supermarkets"),
    ("family", "Family Pantry"),
    ("city", "City Corner Shops"),
    ("fresh", "Fresh Farms Co-op"),
    ("happy", "Happy Home Grocers"),
    ("neighbour", "Neighbourhood Mart"),
    ("value", "Value Basket"),
    ("organic", "Organic Lane"),
]:
    customers.append(entity("customer:" + slug, "Customer", label))
for n in range(109, 161):
    entity(f"ticket:T-{n}", "Ticket", f"T-{n}")
for n in range(105, 125):
    entity(f"decision:D-{n}", "Decision", f"D-{n}")
for n in range(104, 113):
    entity(f"commitment:C-{n}", "Commitment", f"C-{n}")
labels = {e["id"]: e["label"] for e in entities}
verbs = {
    "USES": "uses",
    "DEPENDS_ON": "depends on",
    "BLOCKS": "blocks",
    "REQUIRES": "requires",
    "MADE_TO": "is made to",
    "OWNED_BY": "has primary owner",
    "MEMBER_OF": "is a member of",
    "WORKED_ON": "worked on",
    "ABOUT": "is about",
    "STATUS": "has status",
    "DUE_ON": "is due on",
}


def fact(s, p, o=None, scalar=None, text=None):
    return dict(
        subject_id=s,
        predicate=p,
        object_id=o,
        scalar=scalar,
        quote=text or f"{labels[s]} {verbs[p]} {labels.get(o, scalar)}.",
    )


def source(id, kind, title, facts, groups=("engineering",), updated="2026-10-16T04:00:00Z", intro=""):
    body = (intro + "\n\n" if intro else "") + "\n\n".join(f["quote"] for f in facts)
    claims = []
    pos = 0
    for f in facts:
        start = body.index(f["quote"], pos)
        pos = start + len(f["quote"])
        claims.append(dict(f, start=start, end=pos, scope="primary", extraction_score=1.0))
    sources.append(
        dict(
            envelope=dict(
                schema_version="1.0",
                source_id=id,
                kind=kind,
                title=title,
                source_updated_at=updated,
                acl_groups=list(groups),
                body=body,
            ),
            claims=claims,
        )
    )


for id, kind, title, groups, updated, intro, facts in CORE:
    source(
        id,
        kind,
        title,
        [fact(s, p, o, scalar, quote) for s, p, o, scalar, quote in facts],
        groups,
        updated,
        intro,
    )
# Rewrite the canonical decision into ordinary shopping language, preserving exact quoted provenance.
for record in list(sources):
    if record["envelope"]["source_id"] == "decision:D-101":
        sources.remove(record)
        source(
            "decision:D-101",
            "decision",
            "D-101 · Confirm payment before accepting an order",
            [
                fact(
                    "decision:D-101",
                    "ABOUT",
                    projects[0],
                    text="D-101 is about Easy Checkout: unconfirmed payments are ruled out because Green Basket Stores requires confirmed payment before an order is accepted. This prevents shoppers seeing an order confirmation when the bank has not accepted the payment.",
                )
            ],
        )
        break
uses = dict(
    zip(
        projects,
        [
            services[0],
            services[2],
            "service:delivery-board",
            "service:refunds",
            "service:inventory",
            "service:pickup",
            "service:loyalty",
            "service:seller-portal",
            "service:support",
            "service:billing",
        ],
    )
)
dependencies = {
    "service:checkout": "service:payments",
    "service:delivery-board": "service:route-planner",
    "service:route-planner": "service:warehouse",
    "service:refunds": "service:payments",
    "service:inventory": "service:catalog",
    "service:pickup": "service:inventory",
    "service:loyalty": "service:messages",
    "service:seller-portal": "service:catalog",
    "service:support": "service:messages",
    "service:billing": "service:payments",
    "service:reporting": "service:warehouse",
    "service:search": "service:catalog",
}
explain = {
    "service:checkout": "the part of the website where a shopper places an order",
    "service:payments": "the connection that asks the bank to accept a payment",
    "service:reporting": "the tool that adds up sales for store managers",
    "service:messages": "the tool that sends order and delivery messages",
    "service:delivery-board": "the screen staff use to see where deliveries are",
    "service:route-planner": "the tool that chooses a delivery route",
    "service:refunds": "the tool that returns money after an approved cancellation",
    "service:inventory": "the counter that tracks how many items are available",
    "service:catalog": "the list of products, prices and product details",
    "service:loyalty": "the balance of a shopper’s reward points",
    "service:seller-portal": "the workspace used by partner stores",
    "service:support": "the workspace used to help shoppers",
    "service:billing": "the tool that charges repeat grocery subscriptions",
    "service:warehouse": "the feed that reports packing and stock movements",
    "service:pickup": "the tool that reserves a collection time at a store",
    "service:search": "the tool shoppers use to find products",
}
project_summary = [
    "Make it easier to place and pay for an online grocery order.",
    "Help store managers understand their sales.",
    "Show shoppers and staff where a delivery is.",
    "Return money promptly after an approved cancellation.",
    "Warn stores before popular items run out.",
    "Let shoppers collect their order from a store.",
    "Give repeat shoppers reward points.",
    "Help partner stores manage their online business.",
    "Help shoppers get an answer when something goes wrong.",
    "Let shoppers receive a regular grocery box.",
]
for i, p in enumerate(projects[3:], 3):
    source(
        "doc:" + p.split(":")[1] + "-brief",
        "document",
        labels[p] + " · plain-language project brief",
        [fact(people[6 + i], "WORKED_ON", p)],
        ("all_employees",),
        intro=project_summary[i] + " This project is part of the fictional BrightMart demonstration.",
    )
    facts = [fact(p, "USES", uses[p])]
    if uses[p] in dependencies:
        facts.append(fact(uses[p], "DEPENDS_ON", dependencies[uses[p]]))
    source(
        "doc:" + p.split(":")[1] + "-plan",
        "document",
        labels[p] + " · delivery plan",
        facts,
        intro="Business purpose: "
        + project_summary[i]
        + " The facts below show which systems the project needs.",
    )
for i, s in enumerate(services[4:], 4):
    facts = [fact(s, "OWNED_BY", teams[i % 8])]
    if s in dependencies:
        facts.append(fact(s, "DEPENDS_ON", dependencies[s]))
    source(
        "doc:" + s.split(":")[1] + "-runbook",
        "document",
        labels[s] + " · working guide",
        facts,
        intro=labels[s]
        + " means "
        + explain[s]
        + ". An owner is the team responsible for keeping this system working.",
    )
for i, s in enumerate(services):
    facts = [fact(people[(i + 12) % 40], "WORKED_ON", s)]
    # A documented collaboration is not another ownership claim.
    source(
        "chat:" + s.split(":")[1] + "-weekly",
        "chat",
        labels[s] + " · weekly handover",
        facts,
        intro="Fictional exported team discussion. The people below contributed to this system; that alone does not make them its owner.",
    )
for i, p in enumerate(people):
    # Keep canonical contributors scoped to their existing work; add credible independent project history.
    s = services[4 + i % 12]
    source(
        "doc:work-" + p.split(":")[1],
        "document",
        labels[p] + " · contribution notes",
        [fact(p, "WORKED_ON", s), fact(p, "WORKED_ON", projects[2 + i % 8])],
        intro="A record of work performed, not a claim about seniority, availability or ownership. "
        + labels[s]
        + " is "
        + explain[s]
        + ".",
    )
issues = [
    "Delivery location stops updating",
    "Refund reference missing from bank response",
    "Item quantity differs from store count",
    "Collection slot can be double-booked",
    "Reward points applied twice",
    "Product price update arrives late",
    "Help request not assigned",
    "Repeat order charges fail",
    "Route uses an unavailable road",
    "Packing update arrives out of order",
    "Product search misses common names",
    "Order text message arrives late",
]
# Background tickets are relevant to other stories; they do not all block the checkout launch.
targets = [
    "service:delivery-board",
    "service:refunds",
    "service:inventory",
    "service:pickup",
    "service:loyalty",
    "service:seller-portal",
    "service:support",
    "service:billing",
    "service:route-planner",
    "service:warehouse",
    "service:search",
    "service:messages",
]
statuses = [
    "blocked",
    "open",
    "in_progress",
    "done",
    "done",
    "cancelled",
    "done",
    "open",
    "done",
    "done",
    "in_progress",
    "done",
]
for i, n in enumerate(range(109, 161)):
    target = targets[i % 12]
    status = statuses[i % 12]
    source(
        f"ticket:T-{n}",
        "ticket",
        f"T-{n} · {issues[i % 12]} (check {i // 12 + 1})",
        [
            fact(f"ticket:T-{n}", "BLOCKS", target),
            fact(f"ticket:T-{n}", "STATUS", scalar=status),
            fact(people[(i + 6) % 40], "WORKED_ON", f"ticket:T-{n}"),
        ],
        intro="A fictional work item. Status done or cancelled means it is not an active blocker; open, in_progress or blocked still needs attention.",
        updated="2026-10-17T03:30:00Z",
    )
rationales = [
    ("Show the last delivery update time", "so shoppers know when a location might be out of date"),
    ("Ask the bank for a refund reference", "so customer care can trace the money"),
    ("Check stock before taking a collection booking", "so stores do not promise an item that has sold out"),
    ("Use one reward entry per completed order", "so a retry cannot award the points twice"),
    (
        "Explain failed subscription payments",
        "so shoppers can fix payment details without placing duplicate orders",
    ),
    ("Keep a history of changed product prices", "so stores can explain the price accepted for an order"),
    ("Send one notification per order event", "so retries do not send shoppers the same message repeatedly"),
    ("Keep human review for disputed refunds", "so a missing detail does not cause an automatic rejection"),
]
for i, n in enumerate(range(105, 125)):
    p = projects[2 + i % 8]
    title, why = rationales[i % 8]
    source(
        f"decision:D-{n}",
        "decision",
        f"D-{n} · {title}",
        [fact(f"decision:D-{n}", "ABOUT", p, text=f"D-{n} is about {labels[p]}: {title.lower()} {why}.")],
        intro="A fictional recorded product decision. The quotation explains the reason; it is not a claim that this policy applies to every project.",
    )
for i, n in enumerate(range(104, 113)):
    p = projects[1 + i % 9]
    customer = customers[1 + i % 9]
    source(
        f"doc:promise-C-{n}",
        "document",
        labels[customer] + " · " + labels[p] + " promise",
        [
            fact(f"commitment:C-{n}", "REQUIRES", p),
            fact(f"commitment:C-{n}", "MADE_TO", customer),
            fact(f"commitment:C-{n}", "DUE_ON", scalar=f"2026-10-{20 + i:02}"),
        ],
        intro="A fictional customer promise: the project must be available before this rollout can be considered complete. A dependency risk is not proof the date will be missed.",
    )
for i, t in enumerate(teams):
    source(
        "doc:team-" + t.split(":")[1],
        "document",
        labels[t] + " · team handbook",
        [fact(people[i], "MEMBER_OF", t)],
        ("all_employees",),
        intro="Fictional team guide. Read the directory for the full team membership; read system working guides for ownership evidence.",
    )
for i in range(3):
    source(
        f"doc:leadership-{i + 1}",
        "document",
        f"Leadership · internal planning note {i + 1}",
        [],
        ("leadership",),
        intro=f"CONFIDENTIAL_BRIGHTMART_PRIVATE_{i + 1}. Fictional leadership planning note, intentionally restricted for the permission demonstration. No real commercial information is present.",
    )
source(
    "doc:delivery-story",
    "document",
    "Delivery Tracking · how the delivery chain works",
    [
        fact(projects[2], "USES", "service:delivery-board"),
        fact("service:delivery-board", "DEPENDS_ON", "service:route-planner"),
    ],
    intro="A shopper asks where the van is. Delivery Tracking uses the Delivery Board, which needs Route Planner information. Follow the evidence to see what a routing problem could affect.",
)
source(
    "doc:demo-welcome",
    "document",
    "Start here · the BrightMart story",
    [],
    ("all_employees",),
    intro="BrightMart is a fictional online grocery retailer. Start with Easy Checkout: a payment confirmation check is blocked, two teams disagree about the Payment Gateway owner, and Green Basket Stores has a rollout promise. Other stories cover delivery tracking, refunds, stock, collection, rewards and reports. All people and records are invented. The demonstration guide explains the questions to ask; the agent answers from indexed evidence, not this guide.",
)

# The first six memberships must keep Maya/Leah on Payments, Dev/Nina on Integrations.
assignments = {
    people[0]: teams[0],
    people[1]: teams[1],
    people[2]: teams[0],
    people[3]: teams[2],
    people[4]: teams[1],
    people[5]: teams[2],
}
for rec in sources:
    if rec["envelope"]["source_id"] == "directory:brightmart":
        sources.remove(rec)
        break
source(
    "directory:brightmart",
    "directory",
    "BrightMart · team directory",
    [fact(p, "MEMBER_OF", assignments.get(p, teams[i % 8])) for i, p in enumerate(people)],
    ("all_employees",),
    intro="Forty invented employees help ten fictional grocery-store customers sell online. Team membership identifies colleagues, not service ownership.",
)
# Team handbooks carry no conflicting membership facts.
for rec in sources:
    if rec["envelope"]["source_id"].startswith("doc:team-"):
        rec["claims"] = []
        rec["envelope"]["body"] = (
            "BrightMart fictional team handbook. "
            + rec["envelope"]["title"].split(" · ")[0]
            + " works with the other teams to support grocery shopping. The shared directory records actual team membership in this demonstration."
        )

assert len(sources) == 200, len(sources)
assert len(entities) == 180, len(entities)
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "registry.json").write_text(json.dumps(entities, indent=2) + "\n")
manifest = []
for rec in sources:
    path = rec["envelope"]["source_id"].replace(":", "_") + ".json"
    raw = json.dumps(rec, indent=2) + "\n"
    (OUT / path).write_text(raw)
    manifest.append(
        dict(source_id=rec["envelope"]["source_id"], path=path, sha256=sha256(raw.encode()).hexdigest())
    )
counts = dict(Counter(e["kind"] for e in entities))
claim_count = sum(len(r["claims"]) for r in sources)
summary = dict(
    company="BrightMart",
    seed_version="2.0",
    scenario_clock="2026-10-17T04:30:00Z",
    synthetic=True,
    entity_counts=counts,
    source_count=len(sources),
    claim_count=claim_count,
    source_counts=dict(Counter(r["envelope"]["kind"] for r in sources)),
)
(OUT / "manifest.json").write_text(json.dumps(dict(summary, sources=manifest), indent=2) + "\n")
# Every record is readable without opening JSON; claim quotations remain identical.
handbook = [
    "# BrightMart source book",
    "All people, stores and records below are fictional. Generated from the exact imported source bodies.",
    "",
]
for rec in sources:
    env = rec["envelope"]
    handbook.extend(
        [
            f"## {env['title']}",
            f"Record: {env['source_id']} · Access: {', '.join(env['acl_groups'])} · Updated: {env['source_updated_at']}",
            "",
            env["body"],
            "",
        ]
    )
# Documentation is optional; dataset regeneration must also work without docs/.
if (ROOT / "docs").is_dir():
    (ROOT / "docs/BrightMart-Sourcebook.md").write_text("\n\n".join(handbook) + "\n")
(ROOT / "apps/web/lib/workspace-catalog.json").write_text(
    json.dumps(
        dict(
            summary,
            projects=[
                dict(
                    id=p,
                    name=labels[p],
                    purpose=project_summary[i],
                    question=f"What could block {labels[p]}?",
                    system=labels[uses[p]],
                )
                for i, p in enumerate(projects)
            ],
            glossary=[dict(name=labels[s], meaning=explain[s]) for s in services],
        ),
        indent=2,
    )
    + "\n"
)
print(json.dumps(summary, indent=2))
