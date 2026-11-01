---
name: design-preflight
description: >
  Critique and verify a UI or designed artifact before delivery, or investigate
  weak LLM-generated design. Checks reader tasks, truthful copy, hierarchy,
  interactions, and the whole rendered artifact while distinguishing defects
  from contextual trade-offs and aesthetic preferences.
---

# Design preflight

## Establish the contract

Read the brief, applicable product/design-system guidance, selected references, and actual implementation. Use design-references when substantial design work lacks a researched basis. Identify audience and task, host surface, supported themes/viewports, meaningful states, and permitted actions. Distinguish established behavior, chosen policy, and assumptions. Report conflicts rather than silently changing product policy.

Review the unit the reader actually uses: a complete page, embedded comment in its host, repeated list, or end-to-end interaction. Judge scanning, close reading, and repeated expert use differently. Keep the authorized scope: a critique request produces findings, while an implementation request permits bounded fixes within its requested behavior.

## Collect evidence

Use available source/DOM checks for heading structure, accessible names, placeholder destinations, overflow, and contrast where computable. Trace percentages, completion/coverage claims, retry promises, approval states, and resolution labels to actual product behavior. A word or visual motif can identify a candidate; its presence alone establishes no defect.

Render the whole artifact, including document background, margins, content width, host boundary, and surrounding controls. Inspect screenshots at the supported themes and representative wide/narrow viewports. Include long content, empty/loading/completed states, and relevant errors or partial failures. For embedded artifacts, verify in the real host when possible; label a simulated host as such. Use the available browser tools and follow their skill. If rendering is unavailable, report a source-only review and keep visual conclusions unverified.

Exercise meaningful controls and links, keyboard focus/navigation, disclosures, and state transitions. Inspect the accessibility tree or equivalent semantic evidence where available; screenshots cannot establish keyboard or assistive-technology behavior. Preserve durable state across interruption or failure according to the product contract. Use the installed verifying-motion skill for time-based behavior. Save evidence in task storage, noting which artifact/revision, state, viewport, and theme it represents. Keep sensitive evidence local unless sharing is explicitly authorized and safe.

## Critique the task, not a house style

Look for unclear hierarchy, ambiguous action/outcome vocabulary, unnecessary boundaries, competing emphasis, unsupported claims, inaccessible presentation, ineffective controls, and mismatches between local components and the complete artifact. Consider plausible reader consequences, then test them where possible.

Interpuncts, cards, badges, metrics, gradients, dense layouts, and technical terminology are contextual choices. Ask what each communicates and what would be lost by removing it. Familiar host metadata, independently saved form groups, expert vocabulary, measured progress, deliberate preview boundaries, and neutral decision controls can all be correct. A sentence-expanded design may scan worse; an always-primary action may introduce an unjustified recommendation. See references/retention-cases.md for counterexamples and paired defects.

For each proposed finding supply:
- Exact text, element, code location, or captured region and the affected state/task.
- Reader consequence and evidence; distinguish an observed defect, testable concern, and preference.
- Strongest reason to retain the current treatment, and why the proposed change wins under the brief.
- Smallest useful correction and how to verify it without breaking behavior or another task.

Return no findings when none are justified. Prioritize consequential issues, normally presenting at most three at once; include additional established safety, accessibility, or functional defects rather than hiding them behind a quota. Keep optional aesthetic alternatives separate from required corrections. Do not present a plausible usability hypothesis as measured harm.

## Correct and verify within scope

During authorized implementation, fix evidenced functional, semantic, accessibility, and contract defects. For uncertain design concerns, test the hypothesis when feasible or present it as advice; seek the user's choice when a consequential trade-off remains. Correct grouping, priority, wording, or behavior to address the cause. A separator substitution alone does not clarify unrelated status, identity, counts, and errors.

Make one bounded correction pass within the requested scope, then rerun affected checks and capture the result. Continue for established defects or regressions within scope; stop aesthetic cycling when evidence no longer supports a change. Ask the user when verification requires an unavailable prerequisite or a product decision. External critique or additional agents follow the session's authorization rules.

## Deliver evidence and limits

State what changed or should be retained, which tasks/states/themes/viewports were actually checked, evidence locations, and remaining uncertainty. Distinguish source checks, simulated-host rendering, real-host rendering, interaction checks, and human usability testing. Report blocked checks as blocked. A static screenshot, an independent model's approval, or passing types/tests alone is not full design verification.
