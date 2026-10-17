"use client";
import { useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MarkerType,
  Position,
} from "@xyflow/react";
import type { Answer } from "@/lib/api/client";
export default function AnswerGraph({
  answer,
  onEvidence,
  selectedPath,
}: {
  answer: Answer;
  onEvidence: (id: string) => void;
  selectedPath: string | null;
}) {
  const path = answer.graph.paths.find((p) => p.id === selectedPath);
  const edges = path
    ? answer.graph.edges.filter((e) => path.edge_ids.includes(e.id))
    : answer.graph.edges;
  const ids = new Set(
    edges.flatMap((e) => [e.source_entity_id, e.target_entity_id]),
  );
  const nodes = useMemo(() => {
    const columns: Record<string, number> = {
      Commitment: 0,
      Project: 1,
      Service: 2,
      Ticket: 4,
      Customer: 1,
      Decision: 0,
      Team: 4,
      Person: 4,
    };
    const counts: Record<number, number> = {};
    return answer.graph.nodes
      .filter((n) => !path || ids.has(n.id))
      .map((n, index) => {
        let col = columns[n.kind] ?? 2;
        if (
          n.kind === "Service" &&
          answer.graph.edges.some(
            (e) => e.predicate === "DEPENDS_ON" && e.target_entity_id === n.id,
          )
        )
          col = 3;
        const row = counts[col] || 0;
        counts[col] = row + 1;
        return {
          id: n.id,
          sourcePosition: Position.Right,
          targetPosition: Position.Left,
          position: path
            ? { x: (index % 2) * 240, y: Math.floor(index / 2) * 150 }
            : { x: col * 240, y: row * 125 },
          data: {
            label: (
              <div className={"graphNode " + n.kind.toLowerCase()}>
                <small>{n.kind}</small>
                <strong>{n.label}</strong>
              </div>
            ),
          },
          style: {
            width: 190,
            padding: 0,
            border: "1px solid #d9dfe8",
            borderRadius: 10,
            background: "#fff",
          },
        };
      });
    // Selected path is a projection, never an invented relationship.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [answer, selectedPath]);
  return (
    <div className="graphCanvas" aria-label="Evidence relationship graph">
      <ReactFlow
        key={selectedPath || "all"}
        nodes={nodes}
        edges={edges.map((e) => ({
          id: e.id,
          source: e.source_entity_id,
          target: e.target_entity_id,
          label: e.predicate.toLowerCase().replaceAll("_", " "),
          markerEnd: { type: MarkerType.ArrowClosed },
          style: { stroke: e.conflict ? "#b97816" : "#5478c9", strokeWidth: 2 },
          labelStyle: { fontSize: 12, fill: "#4b586d" },
          labelBgStyle: { fill: "#f8faff" },
          data: { evidence: e.evidence_ids },
        }))}
        onEdgeClick={(_, e) => {
          const id = e.data?.evidence[0];
          if (id) onEvidence(id);
        }}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        nodesDraggable
        minZoom={0.3}
        maxZoom={1.4}
        attributionPosition="bottom-right"
      >
        <Background gap={22} color="#dbe2ee" />
        <Controls showInteractive={false} />
      </ReactFlow>
    </div>
  );
}
