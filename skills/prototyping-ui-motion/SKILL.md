---
name: prototyping-ui-motion
description: Use before building or changing an animation, transition, gesture, or other time-based UI behavior in a product, when the user says motion feels janky or wrong, or when the user points at a reference to match. Settles the target and its constraints, then builds a standalone mockup with variants for the user to pick before any product code changes.
---

# Prototyping UI motion

Motion is judged by feel, so it is chosen in a mockup first. Product work then
follows the chosen mockup, with adjustments only as `verifying-motion` finds
differences.

## 1. State the target physically

Write what each visible element does in space and time: which elements move,
where, in what order, and what must never happen (for example "no card fades in
place"). Describe the elements that stay on screen as well as the one that
travels. Resolve ambiguity with one question to the user; otherwise continue.

## 2. Study references as frames

Use the user's references first. Open each in a browser and capture frames with
the procedure in `verifying-motion`. Write down what every element does,
including elements at rest. When a reference's source is unavailable, say so and
work from frames and documentation. When the user gave none, find two or three
and state which behavior each shows; ask when none fits.

## 3. Check the target against the real content

List the properties of the real content the motion must survive: size and
length variation, item count, rapid repeats, reversal mid-motion, wrap-around,
`prefers-reduced-motion`. For each, say how the target motion handles it. When
the real content range breaks the target (for example a physical stack whose
cards differ widely in height), tell the user before building, with the options
that remain.

## 4. Build a standalone mockup

- One HTML file outside the product tree, with samples at the extremes of the
  real content.
- Two or three variants that differ in kind, not in tuning, selectable in the
  page.
- The product's key bindings, a speed control that includes slow motion
  (¼×), and a clock that can be stepped so frames are capturable.

## 5. Verify, then hand over

Run `verifying-motion` on the mockup against the references. Give the user the
file, a recording, and what to watch for, then stop for their pick. Leave
product code, tests, deploys, and pushes untouched until then.

## 6. Implement the pick

Port the mockup's structure and motion constants into the product, then run
`verifying-motion` with the mockup as the reference. Ship through the
repository's own workflow.
