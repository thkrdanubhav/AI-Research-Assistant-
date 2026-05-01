TITLE_PROMPT = """
Generate 2–3 alternative academic research titles for:

"{topic}"

Requirements:
- each title between 8 and 14 words
- formal academic tone
- no explanation text
Return numbered list only.
"""


OUTLINE_PROMPT = """
Create a structured academic research outline for:

"{topic}"

Include sections:

1. Introduction
2. Background and Key Concepts
3. Methodology Overview
4. Applications
5. Challenges and Limitations
6. Open Research Gaps
7. Future Research Directions
8. Conclusion

Return headings only.
"""


ABSTRACT_PROMPT = """
Write an academic abstract for:

"{topic}"

Requirements:
- 150–220 words
- include purpose, scope, significance
- formal tone
- paragraph format
"""


SECTION_PROMPT = """
Write a detailed academic section titled:

"{section}"

for topic:

"{topic}"

Length requirements:

Introduction:
300–400 words

Background and Key Concepts:
400–600 words

Methodology Overview:
250–400 words

Applications:
300–500 words

Challenges and Limitations:
250–400 words

Conclusion:
150–250 words

Use formal academic language.
Avoid bullet-only answers.
Write structured paragraphs.
"""


RESEARCH_GAPS_PROMPT = """
Write Open Research Gaps section for:

"{topic}"

Requirements:
200–300 words
formal academic tone
focus on unresolved technical challenges
paragraph format
"""


FUTURE_WORK_PROMPT = """
Write Future Research Directions section for:

"{topic}"

Requirements:
200–300 words
suggest realistic improvements and extensions
formal tone
paragraph format
"""


REVIEW_PROMPT = """
You are editing an academic research report.

Return ONLY the improved research paper.

Do NOT describe improvements.
Do NOT explain grammar corrections.
Do NOT add commentary.

Start the document with:

Detailed Research Report on "{topic}"

Then present:

Title options
Abstract
All structured sections

Text:

{content}
"""