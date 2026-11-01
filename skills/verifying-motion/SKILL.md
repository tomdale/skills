---
name: verifying-motion
description: Use after writing or changing any animation, transition, or time-based UI behavior, before reporting it done or showing it to the user. Captures frames of the result and of the reference or stated intent, compares them element by element, measures motion invariants, and has a fresh-context reviewer judge the frames.
---

# Verifying motion

Passing tests and clean types say nothing about how motion looks. The evidence
is captured frames of the result, compared with a reference or the user's
stated intent.

## 1. Capture frames

- Drive the page in headless Chrome (Playwright). Pause animations and step
  them (`document.getAnimations()`, setting `currentTime`) or inject a
  controllable clock, so frames land at exact intervals.
- Sample every 20–50 ms from the start of the motion until it settles. Build a
  contact sheet with timestamps.
- Capture each scenario that matters: every direction, smallest-to-largest and
  largest-to-smallest content, rapid repeats, reversal mid-motion, wrap-around
  or edge items.
- Record a real-time video as well, to see frame pacing.

## 2. Compare with the reference

Capture the reference the same way: the live demo, the previous version, or the
approved mockup. Put the two contact sheets side by side. For every element,
including those at rest, list what the reference does and what the result does:
travel, scale, opacity, stacking order, start offset, easing. Fix each
difference or record why it is intended.

When the only reference is the user's stated intent, turn it into a per-element
checklist of expected behavior (what moves, in what order, what must not
happen) and mark each item against the result's contact sheet.

## 3. Measure the invariants

Sample transforms and computed styles per frame and report each result. These
are defaults; where the reference or stated intent differs, it wins, and the
report says so.

- Elements meant to move together start within one stagger interval of each
  other, so the whole group is in motion at once; count the moving elements
  per frame.
- Each element's opacity follows the reference or stated intent; list every
  opacity change that neither calls for, especially on elements meant to travel.
- No per-frame jump in position, size, or color that the reference or stated
  intent does not show; flag any single-frame change much larger than its
  neighbors.
- No size animates unless the reference or stated intent calls for it.
- Stacking order changes only while the elements involved are visually apart,
  before they overlap or after they separate.
- Where the interaction is interruptible, a new input retargets from the
  current value without snapping.
- Animation prefers `transform` and `opacity`, which can usually be composited;
  animated layout properties cause jank. When the design needs another
  property, confirm in a performance trace that smoothness holds.
- `prefers-reduced-motion` has a calm path.

Common failures to look for: opacity changes standing in for spatial motion, one
element moving while its neighbors sit still, one fixed duration for every
distance, animated layout properties.

Starting values when the reference gives none: springs for interactive motion;
about 100–200 ms for small elements, 250–400 ms for medium, 450–700 ms for
large (Material motion); 20–100 ms stagger between related elements;
decelerate on enter, accelerate on exit. Match the reference first.

## 4. Get an independent judgment

Spawn a fresh-context subagent on a vision-capable model. Give it only the
user's own words, the reference sheet, and the result sheet, and ask: does the
result match, and what visible defects appear (pops, overlaps, inert elements,
content showing through a moving card). Withhold your explanation of the
design. Fix the findings, recapture, and repeat until it reports none.

## 5. Report

State which scenarios were captured, what was compared, each invariant's
result, and what was not verified (for example "frame pacing measured in
headless Chrome only; not felt on a real display").
