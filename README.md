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

**RPI's campus dining experience** — what it's actually like to eat at RPI's dining halls (Commons, Russell Sage, Blitman, BARH) and the restaurants around campus in Troy, NY.

This knowledge is valuable but hard to find through official channels because official pages only publish the *menus, hours, and locations* — not the lived experience. What students actually think about food quality, wait times, dietary accommodations, meal-plan value, and which off-campus spots are worth it comes from the students who attend (or have attended) RPI and the people who live in the area. Those opinions are scattered across Reddit threads, forums, review sites, and local blogs, so answering a simple question like "how is the food at Commons?" means finding and piecing together many separate sources. This system collects those community voices into one place and answers questions grounded only in them.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | A Massive List of Restaurants in the RPI Area | Reddit post (r/RPI) | https://www.reddit.com/r/RPI/comments/1kar67/a_massive_list_of_restaurants_in_the_rpi_area/ — `documents/01_reddit_massive_list_of_restaurants.txt` |
| 2 | Sodexo (dining-hall changes: tray removal, Blitman ordering, meal-plan refunds) | Reddit post (r/RPI) | https://www.reddit.com/r/RPI/comments/1li57g/sodexo/ — `documents/02_sodexo.txt` |
| 3 | Russell Sage Dining Hall: A Culinary Oasis in the Heart of Troy | Blog article (wonstudy.com) | https://wonstudy.com/russell-sage-dining-hall-a-culinary-oasis-in-the-heart-of-troy/ — `documents/03_russell_sage_culinary_oasis.txt` |
| 4 | RPI Dining Hours: Your Ultimate 2024 Guide for Every Hall | Blog article (The Brain Blog) | https://the-brain.blog/rpi-dining-hours-ultimate-2024-guide-every-hall-15149/ — `documents/04_rpi_dining_hours_guide.txt` |
| 5 | Campus dining follow-up: Lally Galley proves decent | University newspaper (The Polytechnic) | https://poly.rpi.edu/features/2013/02/2013-02-20-campus-dining-follow-up-lally-galley-proves-decent — `documents/05_lally_galley_proves_decent.txt` |
| 6 | Rensselaer Polytechnic Institute Reviews | Review site (Niche) | https://www.niche.com/colleges/rensselaer-polytechnic-institute/reviews/ — `documents/06_niche_reviews.txt` |
| 7 | How's the food | Reddit post (r/RPI) | https://www.reddit.com/r/RPI/comments/zrnqys/hows_the_food/ — `documents/07_hows_the_food.txt` |
| 8 | Food for Thought | University magazine (Rensselaer) | https://magazine.rpi.edu/feature/food-for-thought — `documents/08_food_for_thought.txt` |
| 9 | RPI neighborhood | Online forum (College Confidential) | https://talk.collegeconfidential.com/t/rpi-neighborhood/1974021 — `documents/09_rpi_neighborhood.txt` |
| 10 | RPI's failure to feed | University newspaper (The Polytechnic) | https://poly.rpi.edu/opinion/2023/04/rpi-failure-to-feed — `documents/10_rpi_failure_to_feed.txt` |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** ~150 tokens, measured with the all-MiniLM-L6-v2 tokenizer (not characters), so "150 tokens" means 150 tokens to the embedding model too. Split with LangChain's `RecursiveCharacterTextSplitter`, which prefers to break on paragraph breaks, then lines, then sentences, so chunks stay coherent.

**Overlap:** ~25 tokens. A small overlap carries a little context across boundaries so a sentence split between two chunks isn't stranded, without heavily duplicating text.

**Preprocessing before chunking:** each source is loaded from `documents/`, HTML is stripped (BeautifulSoup, dropping script/style/nav/header/footer), Unicode is normalized (NFKC, zero-width/non-breaking spaces removed), and whitespace is collapsed **while preserving paragraph breaks (`\n\n`)** so the splitter has real boundaries to cut on. Site boilerplate, ads, nav menus, and vote/share buttons were removed from the saved source text beforehand.

**Why these choices fit your documents:** the corpus is review-heavy — students' opinions and short comments rather than long structured guides. I first used ~256 tokens (the point where all-MiniLM-L6-v2 truncates, so every token still influences the vector), but testing retrieval on the 5 evaluation questions recalled only 3/5: some answers were a single sentence buried inside a large multi-topic chunk, so their signal was diluted and they ranked below top-k. Re-chunking at ~150 tokens raised recall to 5/5 by giving each chunk a tighter, more focused idea. I did not go smaller — at ~100 tokens recall fell back to 3/5 as answers were split across chunk boundaries. So 150/25 was the empirical sweet spot.

**Final chunk count:** 211 chunks across 10 documents (min 9 / max 149 / avg ~105 tokens per chunk).

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

all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**

If I were deploying this for real users and cost wasn't a constraint, I would consider the tradeoffs on context length, accuracy on domain-specific text, and latency when using different models, since these are key factors users value the most when interacting with RAG systems or AI Models

---

## Retrieval Test Results

<!-- Run these 3 queries through your retrieval system and record the top returned chunks.
     For at least 2 of the 3, explain why the returned chunks are relevant to the query.
     Results must be text — not screenshots. -->

**Query 1:**

Which one of the restaurants do students recommend are especially good choices for weekend breakfasts?

**Top returned chunks:**

- `score=0.623  distance=0.377  source=Reddit Post  (01_reddit_massive_list_of_restaurants::17)`
    - https://www.reddit.com/r/RPI/comments/1kar67/a_massive_list_of_restaurants_in_the_rpi_area/
    - Bonus: They're next door to a vintage game store.  Manory's - Breakfast/Diner  At the corner of Congress and 4th, and awesome for weekend breakfasts. Go with a big group, they are always very accommodating. Theyalso occasionally have interesting breakfast specials (or specials on pancakes). Manory'…
- `score=0.591  distance=0.409  source=University Magazine  (08_food_for_thought::1)`
    - https://magazine.rpi.edu/feature/food-for-thought
    - "The students definitely have moved healthier," says David Wilkerson, lead daytime lunch cook, who has been at Rensselaer for three years. "They ask for more grain dishes and salad dishes; overall, just more variety. We always have at least one gluten-free option and a vegan or vegetarian offering."…
- `score=0.583  distance=0.417  source=The Brain Blog  (04_rpi_dining_hours_guide::18)`
    - https://the-brain.blog/rpi-dining-hours-ultimate-2024-guide-every-hall-15149/
    - When the pressure is on and you only have 20 minutes between labs, students have their proven favorites. The Deli/Sandwich Shop is often a top choice for a quick, customized, and relatively healthy meal. For that essential morning or mid-afternoon boost, the Campus Cafe is unmatched for its speed an…

**Relevance explanation:**
Chunk 1 is the most revelent as it directly provides the restaurant recommendation with details

---

**Query 2:**

Which two pizza restaurants near the campus area are the most popular among RPI students, and how are they compared?

**Top returned chunks:**

- `score=0.771  distance=0.229  source=Reddit Post  (01_reddit_massive_list_of_restaurants::1)`
    - https://www.reddit.com/r/RPI/comments/1kar67/a_massive_list_of_restaurants_in_the_rpi_area/
    - And now for the list that has no real specific order:  Big Apple Pizza - Pizza  The most popular pizza place, and the closest to RPI campus. You may hear of it by it's colloquial name, "Bella" or "Pizza Bella". This was the name before Big Apple Pizza, (Same owners, nothing changed except the title)…
- `score=0.658  distance=0.342  source=Reddit Post  (01_reddit_massive_list_of_restaurants::0)`
    - https://www.reddit.com/r/RPI/comments/1kar67/a_massive_list_of_restaurants_in_the_rpi_area/
    - A Massive List of Restaurants in the RPI Area  In the spirit of encouraging people to eat out and explore the downtown area, I've made a list of places you might hear about, or should hear about while at RPI. Troy has become way less sketchy/scary/jank in the past couple years, although some vandals…
- `score=0.625  distance=0.375  source=University Magazine  (08_food_for_thought::2)`
    - https://magazine.rpi.edu/feature/food-for-thought
    - "With such a broad range of diversity here at RPI, the tastes that the students bring are so eclectic," says Aaron Pouliot, Rensselaer Dining Services' new campus executive chef. "The students are educated in food and they are not afraid to try new things. They have a strong global palate. They want…

**Relevance explanation:**
Chunk 1 is the most relevant chunk as it directly provides the name of the restaurant and the reason why it is popular among students.

---

**Query 3:**

What do university staff say about BARH Dining Hall's food menu focus area?

**Top returned chunks:**

- `score=0.733  distance=0.267  source=University Magazine  (08_food_for_thought::7)`
    - https://magazine.rpi.edu/feature/food-for-thought
    - And the BARH dining hall has transitioned to performance-based menus. "It's always leaned in that direction, but now the menus are focused on foods that enhance optimal athletic and mental performance—things like lean proteins, whole grains, steamed vegetables, and cauliflower and whole wheat crust …
- `score=0.656  distance=0.344  source=Reddit Post  (07_hows_the_food::14)`
    - https://www.reddit.com/r/RPI/comments/zrnqys/hows_the_food/
    - Puppyboy2003 — ENGR 2026 (7 upvotes) This is mostly a review of Commons Dining hall, but mostly appliesto other dining halls. The food (at it's best) is worse than Georgia Tech, Boston College, American University, and Bentley (at their worst). (I was at summer camps at all those places, and they w…
- `score=0.631  distance=0.369  source=The Brain Blog  (04_rpi_dining_hours_guide::3)`
    - https://the-brain.blog/rpi-dining-hours-ultimate-2024-guide-every-hall-15149/
    - Why Your Dining Schedule is a Game-Changer  Think of your dining schedule as a secret weapon for a stress-free RPI experience. Knowing when and where to eat can significantly ease your student life. No more scrambling for food between back-to-back lectures, missing out on your favorite meal, or wand…

**Relevance explanation:**
Chunk 1 is the most relevant as it uses university staff's explanation on how the dining hall menu food options are designed.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

```
Milestone 5 — Grounded generation.

Pipeline stage implemented here (see the Architecture diagram in planning.md):

    5. Generation — take a user question, retrieve the top-k chunks (Milestone 4),
                    and ask the LLM to answer *using only those chunks*, then return
                    the answer together with a programmatically-built source list.

Grounding is enforced by construction, not merely requested:

  (a) RETRIEVAL GATE — if retrieval finds nothing above MIN_SCORE, we return the
      refusal string WITHOUT calling the LLM at all. An out-of-scope question can
      never reach the model, so it cannot be answered from the model's own
      knowledge.
  (b) CONTEXT-ONLY INPUT — the model is given ONLY the retrieved passages. It has
      no other documents to draw on.
  (c) HARD SYSTEM PROMPT — the model is instructed to use only the passages, to
      refuse with an EXACT sentinel string when they are insufficient, and to not
      use outside knowledge. temperature=0 makes this deterministic.
  (d) CODE-BUILT ATTRIBUTION — the `sources` returned to the caller are assembled
      in Python from the retrieved chunks' metadata (source label + url + doc_id).
      They are NOT parsed from, or generated by, the model. The model literally
      cannot omit, alter, or fabricate a source in the returned source list.

Usage:
    pip install -r requirements.txt          # groq, python-dotenv (+ gradio for app.py)
    cp .env.example .env                     # then put your real GROQ_API_KEY in .env
    python retrieval.py build                # index must exist first
    python generate.py "how is the food at commons?"
```

**How source attribution is surfaced in the response:**

The source attribution is directly cited in the response, as well as at the end of the response listing all sources that are used.

---

## Example Responses

<!-- Provide at least 2 grounded responses (query + response + source attribution)
     and 1 out-of-scope query showing your system's refusal.
     All entries must be text — not screenshots. -->

**Grounded response 1**

**Query:** What do students say about if Russell Sage Dining Hall accomodate to dietary needs?

**Response:** According to wonstudy.com (russell sage culinary oasis), Russell Sage Dining Hall is committed to meeting the dietary needs of all its patrons, offering a variety of gluten-free, vegan, and vegetarian options, and the staff is happy to assist with any special dietary requests. Additionally, the dining hall staff is well-versed in allergen identification and can assist diners with any dietary restrictions, with the menu clearly labeling all dishes with common allergens, and special dietary requests can be accommodated upon request.

**Source attribution:** 1. wonstudy.com (russell sage culinary oasis) — https://wonstudy.com/russell-sage-dining-hall-a-culinary-oasis-in-the-heart-of-troy/


---

**Grounded response 2**

**Query:** What do university staff say about BARH Dining Hall's food menu focus area?

**Response:** According to University Magazine (food for thought), university staff, specifically Kimberly Mayer, registered dietitian-nutritionist and dietitian for Rensselaer Dining Services, say that BARH Dining Hall's food menu focus area is on "foods that enhance optimal athletic and mental performance—things like lean proteins, whole grains, steamed vegetables, and cauliflower and whole wheat crust pizzas" to "fuel their bodies and minds to keep them at the top of their game."

**Source attribution:**
  1. University Magazine (food for thought) — https://magazine.rpi.edu/feature/food-for-thought
  2. Reddit Post (hows the food) — https://www.reddit.com/r/RPI/comments/zrnqys/hows_the_food/
  3. The Brain Blog (rpi dining hours guide) — https://the-brain.blog/rpi-dining-hours-ultimate-2024-guide-every-hall-15149/


---

**Out-of-scope query**

**Query:** Where is Stony Brook University located?

**System response (refusal):** I don't have enough information in my sources to answer that.

---

## Query Interface

<!-- Describe your query interface: what are the input fields, what does the output look like?
     Then provide a complete sample interaction transcript showing a real exchange. -->

**Input fields:**
The user is able to provide their question in the "Your question" input field

**Output format:**
The user will be able to get the response after they entered their quetsion in text, with a brief summary, and the cited sources at the end of page

---

**Sample Interaction Transcript**

<!-- Show a complete query → response exchange as it actually appears in your interface.
     Must be text — not a screenshot. -->

> **User:**  The user enters a question into the prompt, such as: Which dining hall is recommended for late night food?

> **System:** After the user clicks the ask button, the response will appear in the answer bar, such as: According to The Brain Blog (rpi dining hours guide), for late-night dining at RPI, several venues cater to late-night needs, such as Father's Marketplace or the RPI Pub. Additionally, Commons Dining Hall is open until 12:00 AM (Midnight) during typical Exam Week hours.
>
> Along with the sources cited below the answer:
> - The Brain Blog (rpi dining hours guide)
> - Reddit Post (hows the food)

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about the peak hours at Russell Sage? | The absolute busiest time at Sage is usually weekdays between 12:00 PM and 1:00 PM for lunch. Dinner rush also tends to pick up right at 5:00 PM. (from The-Brain.blog) | According to The Brain Blog (rpi dining hours guide), students say that Russell Sage can get pretty busy, especially during peak meal times, which are usually weekdays between 12:00 PM and 1:00 PM for lunch and 5:00 PM for dinner. Additionally, late-night dining can get a crowd, especially around 9:00 PM or 10:00 PM. However, the passages do not provide direct quotes from students, but rather describe the general atmosphere and busiest times at Russell Sage. | Relevant | Accurate |
| 2 | What do university staff say about BARH Dining Hall's food menu focus area? | A registered dietitian-nutritionist and dietitian for Rensselaer Dining Services shared that  dining hall has always been leaned on performance-based menus. But now the menus are focused on foods that enhance optimal athletic and mental performance  (from RPI Alumni Magazine) | According to University Magazine (food for thought), university staff, specifically Kimberly Mayer, registered dietitian-nutritionist and dietitian for Rensselaer Dining Services, say that BARH Dining Hall's food menu focus area is on "foods that enhance optimal athletic and mental performance—things like lean proteins, whole grains, steamed vegetables, and cauliflower and whole wheat crust pizzas" to "fuel their bodies and minds to keep them at the top of their game." | Relevant | Accurate |
| 3 | Does Russell Sage Dining Hall accomodate to dietary needs? | Yes, The dining hall staff is well-versed in allergen identification and can assist diners with any dietary restrictions. The menu clearly labels all dishes with common allergens, and special dietary requests can be accommodated upon request. (from wonstudy.com) | According to wonstudy.com (russell sage culinary oasis), Russell Sage Dining Hall accommodates to dietary needs. The dining hall offers a variety of gluten-free, vegan, and vegetarian options, and the staff is happy to assist with any special dietary requests (Source: [1] wonstudy.com). Additionally, the menu clearly labels all dishes with common allergens, and special dietary requests can be accommodated upon request (Source: [3] wonstudy.com). The staff is also well-versed in allergen identification and can assist diners with any dietary restrictions (Source: [3] wonstudy.com). Furthermore, diners can request modifications to dishes to accommodate dietary restrictions or personal preferences (Source: [2] wonstudy.com). | Partially Relevant | Partially Accurate |
| 4 | Which two pizza restaurants near the campus area are the most popular among RPI students, and how are they compared? | Big Apple Pizza (Pizza Bella) and Defazios are mentioned by students being the two most popular pizza places. The comparison is described as similar to a "Mac vs. PC" debate, with the recommendation that students try both and decide for themselves. (from Reddit ) | According to Reddit Post (reddit massive list of restaurants), the two most popular pizza restaurants near the RPI campus area are Big Apple Pizza and Defazios.<br>According to Reddit Post (reddit massive list of restaurants), Big Apple Pizza is the closest to RPI campus and is often referred to by its colloquial name "Bella" or "Pizza Bella".<br>According to Reddit Post (reddit massive list of restaurants), Defazios is also a highly suggested pizza place with a wide array of toppings and pizza cooked in a wood-fired oven.<br>According to Reddit Post (reddit massive list of restaurants), the comparison between the two boils down to a "Mac vs Pc style debate", suggesting that the choice between the two is a matter of personal preference, and it is recommended to try both places to find your favorite. | Relevant | Partially Accurate |
| 5 | Which one of the restaurants do students recommend are especially good choices for weekend breakfasts? | For weekend breakfasts, students recommend Manory's, praising its accommodating service for groups and breakfast specials. (from Reddit) | According to the Reddit Post (reddit massive list of restaurants), Manory's is a recommended choice for weekend breakfasts, as it is "awesome for weekend breakfasts" and has interesting breakfast specials. | Relevant | Accurate |

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
Are there recommended restuarants that are family friendly?

**What the system returned:**

According to the Reddit Post (reddit massive list of restaurants), Manory's is recommended for weekend breakfasts and is awesome for big groups, which could be family-friendly. Additionally, the Reddit Post (reddit massive list of restaurants) mentions that Moe's and Muza are options, but it does not specifically state that they are family-friendly. The Reddit Post (hows the food) does not provide recommendations for family-friendly restaurants. The Online Forum (rpi neighborhood) and University Magazine (food for thought) do not provide information about family-friendly restaurants.

**Root cause (tied to a specific pipeline stage):**

The issue might have to do with the Embedding Stage, the sources stated some restaurant recommendations if students decide to bring their parents to the campus, just not specifically used the word "family-friendly", and because of the fact the RAG model only uses the information I provide to provide answer, it's not able to understand the semantic association between "parents" and "family", which is why it failured to provide the right answer.

**What you would change to fix it:**

I would consider to add changes so the RAG system is able to understand the relationship between similar words, not just based on the document information I provided, which should help to improve or resolve the situation.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The spec helped me to keep track of my overall workflow design of the system - how it starts from data ingestion, to chunking, to embedding, all the way to generation, to make sure my workflow implementation does not diverge from the design.

**One way your implementation diverged from the spec, and why:**
My chunk size is updated from the initial design, because after using the initial chunk size, with the help of AI, I realized the initial chunk size is too big to get the information retrieval for the specific question, therefore I have to narrow it down for better retrieval purpose.

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

- *What I gave the AI:* I gave instruction to Claude to help cleaning the document so they are ready for data ingestion
- *What it produced:* It encountered issues accessing the content for some documents, but was able to clean some of the documents 
- *What I changed or overrode:* I reviewed the document content and updated the wrong document that contains irrelevant information to the chosen domain

**Instance 2**

- *What I gave the AI:* I gave instruction to Claude to use the chunk size design to create ingestion function
- *What it produced:* It produced the ingestion function which parses the documents, break documents into chunks, so they are ready for the next step of the workflow - embedding process
- *What I changed or overrode:* I noticed the chunk size is too big which impacted the retrieval result down the line, so I decided to decrease the chunk size so that system is able to retrieve more accurate information to the specific questions given.
