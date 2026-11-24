---
type: regex
target: last_message
flags: im
match: not_contains
---
^\s*(?:#{1,6}\s*|h[1-6]\.\s*|\*\*)?(?:Title|Description)\b[\s\S]*?(?:RecipeImporter|recipe_importer|source_url|recipes_router|0042_|/api/v2|cookbook/importer|JSON-LD|\.py\b)[\s\S]*?^\s*(?:#{1,6}\s*|h[1-6]\.\s*|\*\*)?Out of scope\b
