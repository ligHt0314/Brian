"""A bounded model/tool/result loop; all writes remain outside investigation tools."""

from app.agent.tools import ReadTools, ToolCall, ToolArguments


def investigate_with_tools(provider, repo, question, intent, entity, groups, epoch, stage):
    tools = ReadTools(repo, groups, epoch, entity)
    tools.execute(ToolCall(name="resolve_entity", arguments=ToolArguments(name=entity.label)), 0)
    for round_number in (1, 2):
        decision = provider.next_tools(
            question, intent, entity.model_dump(), tools.observations(), 6 - len(tools.trace), round_number
        )
        if len(decision.calls) > 6 - len(tools.trace):
            raise ValueError("Agent tool budget exceeded")
        if not decision.calls and not tools.results[-1].claims:
            raise ValueError("Agent stopped without retrieving evidence")
        for call in decision.calls:
            stage("Reading graph: " + call.name.replace("_", " "))
            tools.execute(call, round_number)
        if decision.finish:
            break
    # The agent cannot call a narrower subset "no known blockers" for the whole project.
    calls = tools.calls
    if intent == "release_risk" and entity.kind == "Project":
        context = any(c.name == "get_project_context" and c.arguments.entity_id == entity.id for c in calls)
        traced = [
            r
            for c, r in zip(calls, tools.results)
            if c.name == "trace_dependencies"
            and c.arguments.entity_id == entity.id
            and c.arguments.direction != "reverse"
            and c.arguments.max_business_hops in {None, 3}
        ]
        required = {entity.id}
        for result in traced:
            required.update(
                id for id in result.entity_ids if tools.directory[id].kind in {"Project", "Service"}
            )
        checked = {id for c in calls if c.name == "find_blockers" for id in c.arguments.entity_ids}
        if not context or not traced or not required <= checked:
            raise ValueError("Tool plan did not cover the project dependency and blocker scope")
    if intent == "owner_lookup" and not any(
        c.name == "find_ownership" and c.arguments.entity_id == entity.id for c in calls
    ):
        raise ValueError("Ownership evidence was not retrieved")
    if intent == "evidence_search" and not any(
        c.name == "search_evidence" and entity.id in (c.arguments.entity_ids or []) for c in calls
    ):
        raise ValueError("Direct evidence lookup did not cover the selected entity")
    claims = {c.id: c for r in tools.results for c in r.claims}
    return list(claims.values()), tools.trace, any(r.truncated for r in tools.results)
