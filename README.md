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
  I used a Hybrid Chunking approach because I wanted the RAG chatbot to identify keywords, such as course names and course ids. Sentiment is also important when ranking workload and class difficulty to aid OMS students with course selection.

**Chunk size:** 200 tokens

**Overlap:** 20 tokens

**Why these choices fit your documents:** I switched from 500 tokens to 200 tokens for the chunk size and 50 to 20 tokens for the overlap size. The chunk and overlap sizes are greater than 50 chunks and cover the right amount of information. 

**Final chunk count:** 95 chunks (Hybrid Chunking), 89 chunks (Without Hybrid Chunking)

Please reference [Chunking.md](https://github.com/RoshniSingh101/ai201-project1-unofficial-guide/blob/main/scripts/Chunking.md) here to read more on how we can switch between hybrid and no-hybrid chunking strategies, and how users can experiment with different chunking and overlap sizes in this project.

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

**System prompt grounding instruction:** You are an assistant that answers questions about the Georgia Tech OMSCS program using ONLY the reference documents provided in the user message.

Strict rules:
1. Use ONLY information found in the provided documents. Do not use any prior \
knowledge, training data, or outside information.
1. If the documents do not contain enough information to answer the question, \
reply with EXACTLY this sentence and nothing else: "{REFUSAL}"
1. Do not guess, infer beyond the text, or fill gaps with plausible-sounding \
information.
1. When you do answer, cite the source document name(s) in parentheses next to \
the claims they support, e.g. "(source: Specialization in Machine Learning)".
1. Be concise and list course codes/names exactly as written in the documents.

**How source attribution is surfaced in the response:** Source attribution consists of embedded citations and a Retrieved from box that houses all the sources the RAG chatbot parsed through before generating the output to the user. 

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

**Question that failed:** Questions that asked for class difficulty based on specialization caused problems. 

**What the system returned:** The system returned that it did not have enough information. 

**Root cause (tied to a specific pipeline stage):** The primary issue came from how the system chunked the ingested documents. Another minor issue that popped up was in the embed and retrieve script as well. 

**What you would change to fix it:** I worked with Claude to fix the issue. I think the main issue was the web scraping and cleaning scripts. I had to manually clean them after running both scripts, so updating the cleaning scripts to remove comments and ads would have made parsing more efficient. 

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The architecture diagrams, domain, and documents guided Claude on how to build the RAG chatbot and pipelines. 

**One way your implementation diverged from the spec, and why:** The top-k count and chunking size diverged from the spec because of how much noise existed in the documents I provided Claude to pre-process and ingest. 

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

- *What I gave the AI:* I opened the folder in Claude and asked it to reference my planning.md file, architecture diagram, and provided the instructions from milestone 4 to build the document pipeline. 
- *What it produced:* It chose to use a top-k 8 instead of 5 approach and built the pipeline.
- *What I changed or overrode:* I had a conversation with Claude back and forth on PRs, and read stack traces to debug demo.launch() to ensure the show_api field returned True. 

**Instance 2**

- *What I gave the AI:* I prompted Claude on scripts to clean the ingested documents I provided (Reddit Threads, Wikis, Official Websites). 
- *What it produced:* We had a background and forth conversation on API calls to clean the documents. Reddit threads posed the greatest challenge to Claude. 
- *What I changed or overrode:* At the end, I needed to manually clean out the comments and ads from the Reddit threads. I could have converted the documents to pdf files, but I wanted a continuous pipeline of information flowing from these documents in case something changed. 
