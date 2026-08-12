# Security and Secrets

Review authentication, authorization, permissions, redirects, user input,
network requests, and token handling at their trust boundaries. Verify that the
correct actor is authorized before the sensitive action and that validation is
performed before remote mutation.

Secrets and sensitive values must not reach output, telemetry, logs, tests,
fixtures, or suggested commands. Report only concrete exposure, authorization,
or input-handling risks supported by the changed code and its real boundary.
