# CLI UX and Machine Output

Check interactive and non-interactive behavior separately. Prompts belong only
in interactive contexts; human prose, warnings, ANSI, and spinners stay off
machine-readable stdout. Use the repository's output abstractions rather than
raw stream writes unless raw output is the established contract.

Check confirmations, help text, errors, warnings, and suggested retry commands.
Retry commands must preserve necessary context and be executable in the mode
where they are emitted. Structured output must remain valid and actionable.
