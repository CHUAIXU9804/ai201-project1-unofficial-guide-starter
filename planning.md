# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

**RPI Campus Dining Experience**

sources might include housing forums, Yelp reviews, orientation wikis, or unofficial FAQs.

1. [A Massive List of Restaurants in the RPI Area](https://www.reddit.com/r/RPI/comments/1kar67/a_massive_list_of_restaurants_in_the_rpi_area/)
2. [Here's a look inside the newly renovated Commons Dining Hall](https://www.facebook.com/RPI.EDU/posts/heres-a-look-inside-the-newly-renovated-commons-dining-hall/10157414067877357/)
3. [Russell Sage Dining Hall: A Culinary Oasis in the Heart of Troy](https://wonstudy.com/russell-sage-dining-hall-a-culinary-oasis-in-the-heart-of-troy/)
4. [RPI Dining Hours: Your Ultimate 2024 Guide for Every Hall](https://the-brain.blog/rpi-dining-hours-ultimate-2024-guide-every-hall-15149/)
5. [Campus dining follow-up: Lally Galley proves decent](https://poly.rpi.edu/features/2013/02/2013-02-20-campus-dining-follow-up-lally-galley-proves-decent)
6. [Rensselaer Polytechnic Institute Reviews](https://www.niche.com/colleges/rensselaer-polytechnic-institute/reviews/)
7. [How's the food](https://www.reddit.com/r/RPI/comments/zrnqys/hows_the_food/)
8. [Food for Thought](https://magazine.rpi.edu/feature/food-for-thought)
9. [RPI neighborhood](https://talk.collegeconfidential.com/t/rpi-neighborhood/1974021)
10. [RPI's failure to feed](https://poly.rpi.edu/opinion/2023/04/rpi-failure-to-feed)

My chosen domain is RPI's campus dining experience. This knowledge is hard to find because food options are publicly visible on the school's website, however, the dining experience are typically provided by the students who are attending or who have attended the university, or the people who live around the areas, and the reviews are typically scattered across the internet, therefore it's necessary to search for all information and piece them together.


<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
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

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
