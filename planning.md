# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Student reviews for the OMSCS program at Georgia Tech. 

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

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
