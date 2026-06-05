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
     Domain: Student reviews for the OMSCS program at Georgia Tech. The information is valuable because there is no one-stop shop for incoming and current OMS students to find information on selecting courses for the program. Instead of searching YouTube reviews, Reddit Threads, OMS Reviews, and OMSHub separately, we can access the materials through one RAG chatbot. 

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->


| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | OMS Reviews | Reviews for OMS Classes at Georgia Tech |https://www.omscentral.com|
| 2 | omscs.rocks | Student-Run Sheet that details capacity of OMS courses previous semesters | https://docs.google.com/spreadsheets/d/e/2PACX-1vRyHrRhH2V52bsYFEtm-8oJDaFOlyGYz6AKXm8WwsthN3fNP3KGkEx7O7D9ZHV3j2iKnzU2XHqoh4pQ/pubhtml |
| 3 | Course & Specs Megathread - Selection, Choices & Registration | Reddit Thread to help OMSCS students navigate course selection | https://www.reddit.com/r/OMSCS/comments/1pyef5z/course_specs_megathread_selection_choices/ |
| 4 | Courses Ranked by Difficulty Spring/Fall 2025 | List of OMS Classes Categorized by Difficulty in Spring and Fall Semesters 2025 | https://www.reddit.com/r/OMSCS/comments/1hsbc76/all_courses_ranked_by_difficulty_2025_springfall/ |
| 5 | Courses Ranked by Difficulty Summer 2025 | List of OMS Classes Categorized by Difficulty in Summer Semester 2025 | https://www.reddit.com/r/OMSCS/comments/1k5k7av/all_courses_ranked_by_difficulty_2025_summer/ |
| 6 | Workload Distributions | Course Workload Distribution for OMS Courses from 2021 - 2024 | https://www.reddit.com/r/OMSCS/comments/1dd0snd/all_courses_workload_distributions_table/ |
| 7 | OMSHub | Wiki of Course Reviews and Ratings for OMS programs | https://www.omshub.org |
| 8 | Specialization in Machine Learning | Requirements and Course Options for OMSCS students interested in pursuing Machine Learning Specialization | https://omscs.gatech.edu/specialization-machine-learning |
| 9 | Specialization in Artificial Intelligence | Requirements and Course Options for OMSCS students interested in specializing in Artifical Intelligence | https://omscs.gatech.edu/specialization-artificial-intelligence-formerly-interactive-intelligence |
| 10 | Specialization in Human-Computer Interaction | Requirements and Course Options for OMSCS students interested in selecting Human-Computer Interaction for their specialization | https://omscs.gatech.edu/specialization-human-computer-interaction |
| 11 | Specialization in Computational Perception and Robotics | Requirements and Course Options for OMSCS students interested in choosing Computational Perception and Robotics as their specialization | https://omscs.gatech.edu/specialization-computational-perception-and-robotics |
| 12 | Specialization in Computing Systems | Requirements and Course Options for OMSCS students interested in studying Computing Systems | https://omscs.gatech.edu/specialization-computing-systems |
| 13 | Specialization in Computer Graphics | Requirements and Course Options for OMSCS students opting to specialize in Computer Graphics | https://omscs.gatech.edu/specialization-computer-graphics |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 200 tokens

**Overlap:** 20 tokens

**Why these choices fit your documents:** I switched from 500 tokens to 200 tokens for the chunk size and 50 to 20 tokens for the overlap size. The chunk and overlap sizes are greater than 50 chunks and cover the right amount of information. 

**Final chunk count:** 95 chunks

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 

**Production tradeoff reflection:** I switched from top-k 5 to 8 because of how noisy the Reddit threads were, and I had to manually clean them as a result. Accuracy and precision on keywords (course numbers and information) that reflect sentiment of OMSCS class reviews, was the biggest tradeoff I was concerned with throughout the process. 

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
