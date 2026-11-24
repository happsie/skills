---
tags: [tickets]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---


Create this as a story in our Jira project COOK. The draft is ready, a colleague wrote it. The existing tickets in COOK are all written like this one.

There are no related tickets and no epic for it. You have everything I know, so go ahead and draft without asking me more questions.

---
Title: Add RecipeImporter + source_url column

Implement RecipeImporter in cookbook/importer/recipe_importer.py. Expose it as POST /api/v2/recipes/import, which takes a URL. Fetch the page with httpx, read the schema.org JSON-LD block with BeautifulSoup, map it to the Recipe model and save it with source_url set to the URL.

Background: cooks type in recipes they found on other websites by hand, which takes about ten minutes per recipe, and most of them stop after two or three. Saving a recipe from its link should get more recipes into people's collections.

Tasks:
- Alembic migration 0042_add_source_url.py
- RecipeImporter + unit tests
- Wire into recipes_router

Not included: importing from a photo, importing from a PDF file.
---
