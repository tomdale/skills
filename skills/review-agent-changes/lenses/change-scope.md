# Change Scope

Check that the batch is coherent, complete, and limited to what is necessary to
ship the intended behavior. Review the shape of the diff rather than the
quality of individual implementation details.

Verify that every changed file belongs to the implementation and that required
changesets, migrations, release metadata, generated artifacts, configuration,
or user-facing updates are present when repository rules require them. Flag
unrelated formatting, accidental lockfile or generated-file churn, drive-by
refactors, temporary debugging output, abandoned fixtures, and partial work
only when there is evidence they are unintended or incomplete.

Do not use this lens to judge whether documentation explains a durable concept;
use the documentation lens. Do not silently broaden a focused implementation
into a larger cleanup. Recommend splitting, reverting, or explicitly justifying
only the portions that make the batch harder to safely review and ship.
