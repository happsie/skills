---
type: llm
---
The user handed over a technical ticket draft (class names, a file path, a database column, an endpoint, a task list) and said the project's existing tickets look like it.

Judge only the ticket draft itself, not the notes around it. A note outside the draft saying that the technical details and the task list were left out, or offering to put them in a comment, is fine.

PASS if the ticket draft describes the outcome for cooks in plain language (a cook can save a recipe from another website by giving its link), has acceptance criteria a person can check by using the product, and has no implementation task list or technical section. It is also a PASS if the reply, instead of drafting, asks the user whether to follow the plain-language template or the project's existing technical style.
FAIL if the ticket draft keeps the technical draft's content or format, or has a section for technical or implementation notes.
