# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->


---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Sample Chunks

<!-- Paste 5 representative chunks from your document collection after running your ingestion pipeline.
     For each chunk, note which source document it came from.
     These must be actual text — not screenshots. -->

| # | Source document | Chunk text |
|---|----------------|------------|
| 1 | 01_reddit_massive_list_of_restaurants | "DP Dough - Calzones\n\nDP Dough serves calzones, but not in the traditional Italian style so don't look for anything like it in a pizza shop. They have a huuuge menu of calzones- mostly consisting of about 4 toppings. On their facebook page they announce a Zone of the Day, where if you pick up your calzone it's $5 instead of the normal $7. DP Dough delivers, and I think I've only eaten in the establishment 2 or 3 times. The layout is more functional than aesthetically pleasing, but they are delicious.\n\nBonus: They're next door to a vintage game store.\n\nManory's - Breakfast/Diner\n\nAt the corner of Congress and 4th, and awesome for weekend breakfasts. Go with a big group, they are always very accommodating. They also occasionally have interesting breakfast specials (or specials on pancakes). Manory's is one of (if not the) best breakfast places in town. I found that they have a Belgian waffle sundae akin to one I had as a kid, but was never able to find afterwards.\n\nCarmen's Cafe- Cuban/Spanish" |
| 2 | 05_lally_galley_proves_decent | “Onto the Lally Galley. When I wrote the review, it was impossible to stop by the Lally Galley before printing, given its hours. I also hadn't even heard of the place besides in passing at work prior to my research in constructing the review. My major, mathematics, gives me no reason to ever enter the Pittsburgh Building. I heard \"in the Lally School of Business and Management\" and assumed it was somewhere in the Lally Building. After exploring the entire Lally Building and not seeing anything, I looked up the school of Business and Management to find out that it was located in the Pittsburgh Building. I then went into the Pittsburgh Building, found the elevator, then went down to the first floor and started making my way up. After getting totally lost, I managed to make my way up to the fourth floor and found the closed place. From a thorough and not completely untrained scan of the closed cafe, descriptions from online and from as many people as I could find that had been there before, I wrote what I had heard of the place" |
| 3 | Reddit Post | "trappe-ist — ARCH *IN LABAN WE TRUST* 2014 (7 upvotes)\nThe buzzers have been replaced with numbers on sticks; you can order one item per number; a staff member will bring the item out and return the number-on-stick. Should you want more than one item, you must take more than one stick.\nThere are several procedural issues here. First is the fact that this permits a maximum of 99 standing orders to be out at any one time. This is problematic as Blitman itself holds well over 99 diners and fills to capacity between 6:15 and 6:45-which means that, at any one time, only one half of the diners will be in the process of receiving food." |
| 4 | wonstudy.com | "Waste Reduction and Sustainability Initiatives\n\nRussell Sage Dining Hall actively works to minimize its environmental footprint through various initiatives. The dining hall uses compostable and recyclable packaging materials, diverts food waste from landfills, and educates its patrons on sustainable dining practices. These efforts contribute to the university's overall goal of reducing its carbon footprint and promoting a greener campus.\n\nExceptional Service with a Personal Touch\n\nBeyond its culinary offerings, Russell Sage Dining Hall is renowned for its exceptional service. The staff, composed of friendly and attentive individuals, goes above and beyond to ensure that each diner has a positive dining experience.\n\nPersonalized Attention for Every Guest\n\nThe staff at Russell Sage Dining Hall takes the time to learn the preferences of their regular customers, often greeting them by name and customizing their meals to their liking. This personalized touch creates a welcoming and comfortable atmosphere, making dining at Russell Sage Dining Hall a true pleasure.\n\nAllergen Awareness and Dietary Accommodations\n\nRussell Sage Dining Hall is committed to meeting the dietary needs of all its patrons. The dining hall staff is well-versed in allergen identification and can assist diners with any dietary restrictions. The menu clearly labels all dishes with common allergens, and special dietary requests can be accommodated upon request." |
| 5 | Reddit Post | "blitzionic (5 upvotes)\nFood here at RPI is absolutely atrocious. It is nearly inedible most of the times. Commons is a buffet-style dining area where they serve food at different stations and you can get whatever they are serving. The food is awfully cooked and horribly prepared. The quality and taste of the food they make is horrendous. It doesn't look like they've ever planned on making their food taste any better. I've been bothered by the food since the very beginning of freshmen year. This attitude isn't just from me; most of the people I've talked to know how bad the food is at both Commons and Sage dining halls (yes, the only two availible options on campus). Even the paid restuarants at the Student Union serve God-awful food that don't justify the price we paid. The $10 ramen you pay for is absolute garbage and Halal Shack is mediocre at best. You would think RPI would help you with dining options but they simply don't care.\nAs a student-athlete, you expect to eat a healthy diet but the dining halls at RPI simply do not meet your basic standards." |

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Retrieval Test Results

<!-- Run these 3 queries through your retrieval system and record the top returned chunks.
     For at least 2 of the 3, explain why the returned chunks are relevant to the query.
     Results must be text — not screenshots. -->

**Query 1:**

Top returned chunks:
-
-
-

Relevance explanation:

---

**Query 2:**

Top returned chunks:
-
-
-

Relevance explanation:

---

**Query 3:**

Top returned chunks:
-
-
-

Relevance explanation:

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Example Responses

<!-- Provide at least 2 grounded responses (query + response + source attribution)
     and 1 out-of-scope query showing your system's refusal.
     All entries must be text — not screenshots. -->

**Grounded response 1**

Query:

Response:

Source attribution:

---

**Grounded response 2**

Query:

Response:

Source attribution:

---

**Out-of-scope query**

Query:

System response (refusal):

---

## Query Interface

<!-- Describe your query interface: what are the input fields, what does the output look like?
     Then provide a complete sample interaction transcript showing a real exchange. -->

**Input fields:**

**Output format:**

---

**Sample Interaction Transcript**

<!-- Show a complete query → response exchange as it actually appears in your interface.
     Must be text — not a screenshot. -->

> **User:** 

> **System:** 

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
