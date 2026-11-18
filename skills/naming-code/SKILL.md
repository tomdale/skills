---
name: naming-code
description: >
  Choose names for types, fields, tables, functions, config keys, CLI flags,
  events, and UI labels. Use before creating or renaming any of them, and when
  a name needs a definition to be understood.
---

# Naming code

Name each thing by what it holds or does.

1. Search first. Grep the code, schema, docs, and the user's messages for the
   word already in use, and reuse it. One concept keeps one name in the code, the
   database column, the API, the CLI, and the UI.
2. Name the contents. `dependentServices` says what is stored; `blastRadius`
   says what you hoped to do with it. Skip metaphors and role words (`manager`,
   `handler`, `info`, `data`) unless the thing manages or handles something you
   can name.
3. Say the name to someone who has not seen the system and ask what they expect
   inside. If they guess wrong, rename it.
4. A name that claims an actor or a check needs a field that records it. An
   `isVerified` flag set by a webhook as soon as a delivery arrives records only
   the delivery, and a `reviewedBy` column that the merge bot fills records the
   merger. Name what the store holds (`deliveredAt`, `mergedBy`), or add the
   field that records the actor or the check.
5. When a rename is the fix, search the whole project for the old name in
   variables, files, query keys, constants, tests, and docs; the type checker
   finds only type references.
