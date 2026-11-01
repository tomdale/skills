---
name: design-preflight
description: >
  Critique and verify a UI or designed artifact before delivery, or investigate
  weak LLM-generated design. Checks reader tasks, truthful copy, hierarchy,
  interactions, and the whole rendered artifact while distinguishing defects
  from contextual trade-offs and aesthetic preferences. Load at task start when
  evaluating the design workflow so evidence and overhead can be recorded.
---

# Design preflight

## Establish the contract

Read the brief, applicable product/design-system guidance, selected references, chosen direction/decision record, and actual implementation. Use design-references when substantial design work lacks a researched basis. When the requested work includes a new visual direction or making generic output distinctive, use design-direction before implementing that direction; targeted repairs retain the established identity. Identify audience and task, host surface, supported themes/viewports, meaningful states, and permitted actions. Distinguish established behavior, chosen policy, and assumptions. Report conflicts rather than silently changing product policy.

Review the unit the reader actually uses: a complete page, embedded comment in its host, repeated list, or end-to-end interaction. Judge scanning, close reading, and repeated expert use differently. Keep the authorized scope: a critique request produces findings, while an implementation request permits bounded fixes within its requested behavior.

For a redesign, compare the existing product and proposal on the same reader task, representative content, state, host/container size, and theme. Capture the affected baseline before changing it when possible; record mismatches that prevent comparison. Name the expected benefit and its cost, such as improved orientation versus lost reading space. Missing baseline evidence leaves that benefit a hypothesis; prototype verification can still proceed. For a new surface, compare against the brief's task and constraints.

## Collect evidence

Use available source/DOM checks for heading structure, accessible names, placeholder destinations, overflow, and contrast where computable. Trace percentages, completion/coverage claims, retry promises, approval states, and resolution labels to actual product behavior. A word or visual motif can identify a candidate; its presence alone establishes no defect.

Render the whole artifact, including document background, margins, content width, host boundary, and surrounding controls. Select a bounded set of checks from the affected task and contract: representative supported themes, wide/narrow containers, long content, relevant empty/loading/completed states, and errors or partial failures. Prioritize the state and size motivating the change; viewport width alone may not represent an embedded panel's width. For embedded artifacts, verify in the real host when possible; label a simulated host as such. Use the available browser tools and follow their skill. If rendering is unavailable, report a source-only review and keep visual conclusions unverified.

Exercise meaningful controls and links, keyboard focus/navigation, disclosures, and state transitions. Inspect the accessibility tree or equivalent semantic evidence where available; screenshots cannot establish keyboard or assistive-technology behavior. Preserve durable state across interruption or failure according to the product contract. Use the installed verifying-motion skill for time-based behavior. Save evidence in task storage, noting which artifact/revision, state, viewport, and theme it represents. Keep sensitive evidence local unless sharing is explicitly authorized and safe.

## Critique the task, not a house style

Look for unclear hierarchy, ambiguous action/outcome vocabulary, unnecessary boundaries, competing emphasis, unsupported claims, inaccessible presentation, ineffective controls, and mismatches between local components and the complete artifact. Check type scale, line height, tracking, figures, and text contrast with the installed typography skill's checks. Consider plausible reader consequences, then test them where possible. Compare the render with the chosen direction as well as the functional contract: check composition and character, including supporting sections and states. Preserve justified expressive choices while correcting evidenced defects; a quieter treatment is not inherently an improvement.

Interpuncts, cards, badges, metrics, gradients, dense layouts, and technical terminology are contextual choices. Ask what each communicates and what would be lost by removing it. Familiar host metadata, independently saved form groups, expert vocabulary, measured progress, deliberate preview boundaries, and neutral decision controls can all be correct. A sentence-expanded design may scan worse; an always-primary action may introduce an unjustified recommendation. See references/retention-cases.md for counterexamples and paired defects.

For each proposed finding supply:
- Exact text, element, code location, or captured region, the affected state/task, and which artifact/revision exhibits it: existing product or proposal/prototype.
- Reader consequence and evidence; distinguish an observed defect, testable concern, and preference.
- Strongest reason to retain the current treatment, and why the proposed change wins under the brief.
- Smallest useful correction and how to verify it without breaking behavior or another task.

Return no findings when none are justified. Prioritize consequential issues, normally presenting at most three at once; include additional established safety, accessibility, or functional defects rather than hiding them behind a quota. Keep optional aesthetic alternatives separate from required corrections. Do not present a plausible usability hypothesis as measured harm.

## Correct and verify within scope

During authorized implementation, fix evidenced functional, semantic, accessibility, and contract defects. For uncertain design concerns, test the hypothesis when feasible or present it as advice; seek the user's choice when a consequential trade-off remains. Correct grouping, priority, wording, or behavior to address the cause. A separator substitution alone does not clarify unrelated status, identity, counts, and errors.

Make one bounded correction pass within the requested scope, then rerun affected checks and capture the result. Separate repairs to defects introduced during prototyping from evidence that the proposal improves the existing product. Check the intended benefit and its trade-off against the baseline where available; repaired overflow alone does not establish better navigation or comprehension. Continue for established defects or regressions within scope; stop aesthetic cycling when evidence no longer supports a change. Ask the user when verification requires an unavailable prerequisite or a product decision. External critique or additional agents follow the session's authorization rules.

## Deliver evidence and limits

State what changed or should be retained, which tasks/states/themes/container sizes were actually checked, evidence locations, and remaining uncertainty. Distinguish source checks, simulated-host rendering, real-host rendering, interaction checks, and human usability testing. Report proposed benefits separately from verified corrections and measured reader outcomes. Report blocked checks as blocked. A static screenshot, an independent model's approval, or passing types/tests alone is not full design verification.

When the user requests evaluation of the workflow or skills, use references/evaluating-workflow.md from the start of the task. Routine design delivery needs the relevant evidence and limits, not a separate process study.
