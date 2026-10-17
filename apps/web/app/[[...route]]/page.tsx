import { Suspense } from "react";
import Workspace from "@/components/Workspace";
export default function Page() {
  return (
    <Suspense fallback={<div>Loading workspace…</div>}>
      <Workspace />
    </Suspense>
  );
}
