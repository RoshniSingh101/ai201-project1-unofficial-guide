# The Unofficial Guide — Project 1

<!-- > **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit. -->

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
| 1 | Please give me a list of medium-level courses to take for the human-computer interaction specialization in fall/spring semesters. | CS 6750: Human-Computer Interaction | ![q1](documents/q1%20eval.png)| Partially Relevant (Ranked by tier entry level instead of medium) | Partially Accurate |
| 2 | Please give me a list of easy-level courses to take for computing systems. | CS 6250: Computer Networks, CS 6310: Software Architecture and Design, and CS 6422: Database System Implementation |![q2](documents/q2%20eval.png)| Relevant | Accurate |
| 3 | What are some of the hardest courses in the OMSCS program?| CSE 6620: Intro to High-Computing, CS 6211: System Design for Cloud Computing, CS 6476: Computer Vision, CS 7210: Distributed Computing, CS 6475: Computational Photography, CS 8803 O08: Compilers - Theory and Practice | ![q3](documents/q3%20eval.png) | Relevant | Accurate |
| 4 | What are the core classes for the Computer Graphics specialization? | CS 6491: Foundations of Computer Graphics, CS 6457: Video Game Design, CS 7496: Computer Animation, CS 6505 Computability, Algorithms, and Complexity, CS 6515 Introduction to Graduate Algorithms. Please note that CS 6505 is only avaliable to students on-campus because the course is not bolded on the website. |![q4](documents/q4%20eval.png)| Relevant | Accurate |
| 5 | What are the elective options for Machine Learning? | CS 6220 Big Data Systems & Analysis, CS 6476 Computer Vision, CS 6603 AI, Ethics, and Society, CS 7280 Network Science, CS 7535 Markov Chain Monte Carlo, CS 7540 Spectral Algorithms, CS 7545 Machine Learning Theory, CS 7616 Pattern Recognition, CS 7626 Behavioral Imaging, CS 7642 Reinforcement Learning and Decision Making (Formerly CS 8803-O03), CS 7643 Deep Learning, CS 7644 Machine Learning for Robotics, CS 7646 Machine Learning for Trading, CS 7650 Natural Language, CS 8803 Special Topics: Probabilistic Graph Models, CSE 6240 Web Search and Text Mining, CSE 6242 Data and Visual Analytics, CSE 6250 Big Data for Health (Formerly CSE 8803), ISYE 6416 Computational Statistics, ISYE 6420 Bayesian Methods, ISYE 6664 Stochastic Optimization | ![q5](documents/q5%20eval.png) | Relevant | Accurate |

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

---
## Query Interface
The user enters a question as input, and the system responds with an answer and sources the system used to retrieve the answer. <img width="1000" height="593" alt="Query Interface" src="https://github.com/user-attachments/assets/0b386993-a797-4828-a68e-df3600bb02a5" />
Gif created with FreeConvert

---

## Demo Video
Here is the demo video linked here that goes over the retrieval test results across three queries and their associated chunks: https://drive.google.com/file/d/18FUEpTzV61jSuykKzEYUCWCQ9usKqVFc/view?usp=share_link

---

## Below are the associated chunks with the five questions from the demo video: 

```bash
.venv/bin/python scripts/embed_and_retrieve.py query "Please give me a list of medium-level courses to take for the human-computer interaction specialization in fall/spring semesters."
```
loading embedding model: all-MiniLM-L6-v2 ...

QUERY: Please give me a list of medium-level courses to take for the human-computer interaction specialization in fall/spring semesters.
------------------------------------------------------------

[1] distance=0.291  source='Specialization in Human-Computer Interaction'  chunk_index=0
------------------------------------------------------------
Specialization in Human-Computer Interaction

For a Master of Science in Computer Science, Specialization in Human-Computer Interaction (15 hours), students must selectfrom the following:

*
The following is a complete look at the courses that may be selected to fulfill the Human-Computer Interaction specialization, regardless of campus; only courses listed with
bold
 titles are offered through the online program
.

Core Courses (6 hours)

CS 6456 Principles of User Interface Software OR
CS 7470 …[truncated]

[2] distance=0.353  source='Human-Computer Interaction Specialization Courses Ranked by Difficulty (Summer)'  chunk_index=0
------------------------------------------------------------
Human-Computer Interaction specialization — courses ranked by difficulty (Summer 2025). Rank 1 = easiest, higher rank = harder.

Easiest course in the Human-Computer Interaction specialization: CS 7470 Mobile and Ubiquitous Computing (MUC) — rank 5, Tier 2 (Easy).
Hardest course in the Human-Computer Interaction specialization: CS 6750 Human-Computer Interaction (HCI) — rank 23, Tier 4 (Medium).

All ranked Human-Computer Interaction courses, easiest to hardest:
- rank 5: CS 7470 Mobile and Ubiq …[truncated]

[3] distance=0.355  source='Human-Computer Interaction Specialization Courses Ranked by Difficulty (Spring/Fall)'  chunk_index=0
------------------------------------------------------------
Human-Computer Interaction specialization — courses ranked by difficulty (Spring/Fall 2025). Rank 1 = easiest, higher rank = harder.

Easiest course in the Human-Computer Interaction specialization: CS 6795 Introduction to Cognitive Science (ICS) — rank 7, Tier 2 (Easy).
Hardest course in the Human-Computer Interaction specialization: CS 6750 Human-Computer Interaction (HCI) — rank 30, Tier 4 (Medium).

All ranked Human-Computer Interaction courses, easiest to hardest:
- rank 7: CS 6795 Introduc …[truncated]

[4] distance=0.388  source='Specialization in Computer Graphics'  chunk_index=0
------------------------------------------------------------
Specialization in Computer Graphics

For a Master of Science in Computer Science, Specialization in Computer Graphics (15 hours), students must selectfrom the following:
*The following is a complete look at the courses that may be selected to fulfill the Computer Graphics specialization, regardless of campus; only courses listed with
bold
 titles are offered through the online program.
Core Courses (6 hours)
Pick one (1) of:
CS 6491 Foundations of Computer Graphics
CS 6457 Video Game Design
CS 7 …[truncated]

[5] distance=0.419  source='Specialization in Artificial Intelligence'  chunk_index=0
------------------------------------------------------------
Specialization in Artificial Intelligence (formerly Interactive Intelligence)

For a Master of Science in Computer Science, Specialization in Artificial Intelligence (15 hours), students must select from the following:
*The following is a complete look at the courses that may be selected to fulfill the Artificial Intelligence specialization, regardless of campus; only courses listed with
bold
 titles are offered through the online program.
Core Courses (9 hours)
Algorithms and Design: Take one ( …[truncated]

[6] distance=0.425  source='Specialization in Computing Systems'  chunk_index=0
------------------------------------------------------------
Specialization in Computing Systems

For a Master of Science in Computer Science, Specialization in Computing Systems (18 hours), students must selectfrom the following:
*
The following is a complete look at the courses that may be selected to fulfill the Computing Systems specialization, regardless of campus; only courses listed with
bold
 titles are offered through the online program
.
Core Courses (9 hours)
CS 6505 Computability, Algorithms, and Complexity
or
CS 6515 Introduction to Graduate  …[truncated]

[7] distance=0.463  source='Course & Specs Megathread'  chunk_index=0
------------------------------------------------------------
Course & Specs Megathread - Selection, Choices & Registration : r/OMSCS
Detective-Raichu
Course & Specs Megathread - Selection, Choices & Registration
Megathread
📌Specializations & Courses Megathread - Selection & Registration

Welcome to the Specialization & Course Megathread for OMSCS!

Now that you've {just been accepted / been here for a bit / been here for awhile}*, this thread is designed to help you navigate the various specializations offered and assist with selecting the right courses f …[truncated]

[8] distance=0.472  source='Specialization in Computational Perception and Robotics'  chunk_index=0
------------------------------------------------------------
Specialization in Computational Perception and Robotics

For a Master of Science in Computer Science, Specialization in Computational Perception and Robotics (15 hours), students must selectfrom the following:

*The following is a complete look at the courses that may be selected to fulfill the Computational Perception and Robotics specialization, regardless of campus; only courses listed with
bold
 titles are offered through the online program.

Core Courses (6 hours)

Algorithms:Pick one (1) o …[truncated]

```bash
.venv/bin/python scripts/embed_and_retrieve.py query "Please give me a list of easy-level courses to take for computing systems."
```
loading embedding model: all-MiniLM-L6-v2 ...

QUERY: Please give me a list of easy-level courses to take for computing systems.
------------------------------------------------------------

[1] distance=0.394  source='Specialization in Computing Systems'  chunk_index=0
------------------------------------------------------------
Specialization in Computing Systems

For a Master of Science in Computer Science, Specialization in Computing Systems (18 hours), students must selectfrom the following:
*
The following is a complete look at the courses that may be selected to fulfill the Computing Systems specialization, regardless of campus; only courses listed with
bold
 titles are offered through the online program
.
Core Courses (9 hours)
CS 6505 Computability, Algorithms, and Complexity
or
CS 6515 Introduction to Graduate  …[truncated]

[2] distance=0.401  source='Computing Systems Specialization Courses Ranked by Difficulty (Summer)'  chunk_index=0
------------------------------------------------------------
Computing Systems specialization — courses ranked by difficulty (Summer 2025). Rank 1 = easiest, higher rank = harder.

Easiest course in the Computing Systems specialization: CS 6300 Software Development Process (SDP) — rank 13, Tier 2 (Easy).
Hardest course in the Computing Systems specialization: CS 6515 Introduction to Graduate Algorithms (GA) — rank 49, Tier 7 (Tell your Loved Ones goodbye).

All ranked Computing Systems courses, easiest to hardest:
- rank 13: CS 6300 Software Development P …[truncated]

[3] distance=0.410  source='Computing Systems Specialization Courses Ranked by Difficulty (Spring/Fall)'  chunk_index=0
------------------------------------------------------------
Computing Systems specialization — courses ranked by difficulty (Spring/Fall 2025). Rank 1 = easiest, higher rank = harder.

Easiest course in the Computing Systems specialization: CS 6300 Software Development Process (SDP) — rank 15, Tier 2 (Easy).
Hardest course in the Computing Systems specialization: CS 7210 Distributed Computing (DC) — rank 64, Tier 7 (Tell your Loved Ones goodbye).

All ranked Computing Systems courses, easiest to hardest:
- rank 15: CS 6300 Software Development Process (S …[truncated]

[4] distance=0.495  source='Specialization in Computer Graphics'  chunk_index=0
------------------------------------------------------------
Specialization in Computer Graphics

For a Master of Science in Computer Science, Specialization in Computer Graphics (15 hours), students must selectfrom the following:
*The following is a complete look at the courses that may be selected to fulfill the Computer Graphics specialization, regardless of campus; only courses listed with
bold
 titles are offered through the online program.
Core Courses (6 hours)
Pick one (1) of:
CS 6491 Foundations of Computer Graphics
CS 6457 Video Game Design
CS 7 …[truncated]

[5] distance=0.504  source='Computational Perception and Robotics Specialization Courses Ranked by Difficulty (Spring/Fall)'  chunk_index=0
------------------------------------------------------------
Computational Perception and Robotics specialization — courses ranked by difficulty (Spring/Fall 2025). Rank 1 = easiest, higher rank = harder.

Easiest course in the Computational Perception and Robotics specialization: CS 7650 Natural Language (NLP) — rank 8, Tier 2 (Easy).
Hardest course in the Computational Perception and Robotics specialization: CS 6475 Computational Photography (CP) — rank 65, Tier 7 (Tell your Loved Ones goodbye).

All ranked Computational Perception and Robotics courses, …[truncated]

[6] distance=0.517  source='Course & Specs Megathread'  chunk_index=0
------------------------------------------------------------
Course & Specs Megathread - Selection, Choices & Registration : r/OMSCS
Detective-Raichu
Course & Specs Megathread - Selection, Choices & Registration
Megathread
📌Specializations & Courses Megathread - Selection & Registration

Welcome to the Specialization & Course Megathread for OMSCS!

Now that you've {just been accepted / been here for a bit / been here for awhile}*, this thread is designed to help you navigate the various specializations offered and assist with selecting the right courses f …[truncated]

[7] distance=0.523  source='Human-Computer Interaction Specialization Courses Ranked by Difficulty (Spring/Fall)'  chunk_index=0
------------------------------------------------------------
Human-Computer Interaction specialization — courses ranked by difficulty (Spring/Fall 2025). Rank 1 = easiest, higher rank = harder.

Easiest course in the Human-Computer Interaction specialization: CS 6795 Introduction to Cognitive Science (ICS) — rank 7, Tier 2 (Easy).
Hardest course in the Human-Computer Interaction specialization: CS 6750 Human-Computer Interaction (HCI) — rank 30, Tier 4 (Medium).

All ranked Human-Computer Interaction courses, easiest to hardest:
- rank 7: CS 6795 Introduc …[truncated]

[8] distance=0.532  source='Computational Perception and Robotics Specialization Courses Ranked by Difficulty (Summer)'  chunk_index=0
------------------------------------------------------------
Computational Perception and Robotics specialization — courses ranked by difficulty (Summer 2025). Rank 1 = easiest, higher rank = harder.

Easiest course in the Computational Perception and Robotics specialization: CS 7650 Natural Language (NLP) — rank 9, Tier 2 (Easy).
Hardest course in the Computational Perception and Robotics specialization: CS 6515 Introduction to Graduate Algorithms (GA) — rank 49, Tier 7 (Tell your Loved Ones goodbye).

All ranked Computational Perception and Robotics cou …[truncated]

```bash
venv/bin/python scripts/embed_and_retrieve.py query "What are some of the hardest courses in the OMSCS program?"
```
loading embedding model: all-MiniLM-L6-v2 ...

QUERY: What are some of the hardest courses in the OMSCS program?
------------------------------------------------------------

[1] distance=0.332  source='Workload Distributions'  chunk_index=6
------------------------------------------------------------
#       Course Code     AKA     Count   5th %   25th %  Median  75th %  95th %  Mean
(continued)

56      CS 6603 AIES    88      1.4     3.8     5       8       14.7    6.4
57      PUBP 6725       ISP     7       1.3     3       5       10      11.4    6.3
58      CS 8803 O22     SIR     4       3.3     4.5     5       5.8     7.6     5.3
59      INTA 6450       DAS     21      2       3       4       5       10      4.7
60      CSE 6742        MSMG    3       1.3     2.5     4       5       5.8     3.7
61      CS 8803 O15     Law     9       1.4     2       2       3       10.6    3.8
62      MGT 6311        DM      22      1       2       2       4.5     7.9     3.2
63      MGT 8813        FMX     7       1       1       2       2.5     3       1.9
ALL     OMSCS   Courses 2142    4       10      14      20      30      15.5

[2] distance=0.362  source='Courses Ranked by Difficulty Summer 2025'  chunk_index=20
------------------------------------------------------------
Tier 7 (Tell your Loved Ones goodbye)
Rank    Course Number   AKA     A%      A-B%    W%      Grades Rank     Rating  Difficulty      Workload

47      CS 8803 O08     Compiler        43.7%   62.5%   29.0%   39      4       49      49
48      CS 6200 GIOS    30.2%   46.2%   48.8%   49      8       43      48
49      CS 6515 GA      21.8%   62.1%   18.0%   46      46      47      45
Notes:

[3] distance=0.373  source='Courses Ranked by Difficulty Spring/Fall 2025'  chunk_index=21
------------------------------------------------------------
Tier 7 (Tell your Loved Ones goodbye)
Rank    Course Number   AKA     A%      A-B%    W%      Grades Rank     Rating  Difficulty      Workload

61      CSE 6220        IHPC    35.7%   51.8%   37.1%   62      25      60      55
**62    CS 6211 SDCC    34.9%   54.2%   35.5%   58      2       65      64
63      CS 6476 CV      36.5%   50.8%   33.9%   63      41      61      62
64      CS 7210 DC      32.6%   56.%    30.9%   60      24      66      65
65      CS 6475 CP      23.5%   43.9%   39.9%   66      46      49      58
66      CS 8803 O08     Compiler        30.9%   47.6%   37.2%   64      4       64      66
Notes:

[4] distance=0.377  source='Courses Ranked by Difficulty Spring/Fall 2025'  chunk_index=12
------------------------------------------------------------
Recent data is generally weighed heavier since courses change over time. For this list, only reviews from Spring 2022 forward are considered, except for courses with less than 15 reviews where older reviews were used to increase sample size. For most courses, only grades from the most recent 5 long semesters are included. A few courses have on-campus offerings one semester/year that cannot be separated from OMSCS grades in lite because they have the same professor as the OMSCS section. For these …[truncated]

[5] distance=0.378  source='Course & Specs Megathread'  chunk_index=0
------------------------------------------------------------
Course & Specs Megathread - Selection, Choices & Registration : r/OMSCS
Detective-Raichu
Course & Specs Megathread - Selection, Choices & Registration
Megathread
📌Specializations & Courses Megathread - Selection & Registration

Welcome to the Specialization & Course Megathread for OMSCS!

Now that you've {just been accepted / been here for a bit / been here for awhile}*, this thread is designed to help you navigate the various specializations offered and assist with selecting the right courses f …[truncated]

[6] distance=0.380  source='Course & Specs Megathread'  chunk_index=1
------------------------------------------------------------
📝 Course Selection Guide

A cheat code is to check out the student-run website at www.omscs.rocks.

It details you the capacity of each course in each semester.

It details you if the course capacity has been max'ed out before.

Understand each of the Specialization Requirements

All courses must be graded for it to be considered part of your degree fulfilment.

Cores are mandatory courses for your specialization. They cannot be avoided.

Electives are choices within your specialisations that al …[truncated]

[7] distance=0.380  source='Courses Ranked by Difficulty Spring/Fall 2025'  chunk_index=14
------------------------------------------------------------
Tier 1 (Free Credits)
Rank    Course Number   AKA     A%      A-B%    W%      Grades Rank     Rating  Difficulty      Workload

1       MGT 6311        DM      75.0%   93.4%   3.8%    5       22      1       1
+2      CSE 6742        MSMG    88.4%   92.1%   6.8%    2       9       4       4
3       CS 8803 O15     Law     77.0%   90.6%   6.1%    11      3       6       3
4       MGT 8813        FMX     83.9%   90.0%   8.2%    6       64      3       2
5       CS 6261 SIR     83.7%   93.8%   5.6%    1       41      9       9
6       INTA 6450       DAS     80.9%   91.6%   6.3%    4       62      5       5

[8] distance=0.381  source='Courses Ranked by Difficulty Summer 2025'  chunk_index=0
------------------------------------------------------------
All Courses Ranked by Difficulty 2025: Summer : r/OMSCS
Stagef6
All Courses Ranked by Difficulty 2025: Summer
Other Courses

This is a list which combines the last three years of grades and reviews data to sort all courses by average difficulty. Only Summer semester information is considered.

```bash
.venv/bin/python scripts/embed_and_retrieve.py query "What are the core classes for the Computer Graphics specialization?"
```
loading embedding model: all-MiniLM-L6-v2 ...

QUERY: What are the core classes for the Computer Graphics specialization?
------------------------------------------------------------

[1] distance=0.333  source='Specialization in Computer Graphics'  chunk_index=0
------------------------------------------------------------
Specialization in Computer Graphics

For a Master of Science in Computer Science, Specialization in Computer Graphics (15 hours), students must selectfrom the following:
*The following is a complete look at the courses that may be selected to fulfill the Computer Graphics specialization, regardless of campus; only courses listed with
bold
 titles are offered through the online program.
Core Courses (6 hours)
Pick one (1) of:
CS 6491 Foundations of Computer Graphics
CS 6457 Video Game Design
CS 7 …[truncated]

[2] distance=0.347  source='Computer Graphics Specialization Courses Ranked by Difficulty (Spring/Fall)'  chunk_index=0
------------------------------------------------------------
Computer Graphics specialization — courses ranked by difficulty (Spring/Fall 2025). Rank 1 = easiest, higher rank = harder.

Easiest course in the Computer Graphics specialization: CS 6457 Video Game Design (VGD) — rank 11, Tier 2 (Easy).
Hardest course in the Computer Graphics specialization: CS 6475 Computational Photography (CP) — rank 65, Tier 7 (Tell your Loved Ones goodbye).

All ranked Computer Graphics courses, easiest to hardest:
- rank 11: CS 6457 Video Game Design (VGD) — Tier 2
- ran …[truncated]

[3] distance=0.385  source='Computer Graphics Specialization Courses Ranked by Difficulty (Summer)'  chunk_index=0
------------------------------------------------------------
Computer Graphics specialization — courses ranked by difficulty (Summer 2025). Rank 1 = easiest, higher rank = harder.

Easiest course in the Computer Graphics specialization: CS 6457 Video Game Design (VGD) — rank 10, Tier 2 (Easy).
Hardest course in the Computer Graphics specialization: CS 6515 Introduction to Graduate Algorithms (GA) — rank 49, Tier 7 (Tell your Loved Ones goodbye).

All ranked Computer Graphics courses, easiest to hardest:
- rank 10: CS 6457 Video Game Design (VGD) — Tier 2
 …[truncated]

[4] distance=0.421  source='Specialization in Human-Computer Interaction'  chunk_index=0
------------------------------------------------------------
Specialization in Human-Computer Interaction

For a Master of Science in Computer Science, Specialization in Human-Computer Interaction (15 hours), students must selectfrom the following:

*
The following is a complete look at the courses that may be selected to fulfill the Human-Computer Interaction specialization, regardless of campus; only courses listed with
bold
 titles are offered through the online program
.

Core Courses (6 hours)

CS 6456 Principles of User Interface Software OR
CS 7470 …[truncated]

[5] distance=0.432  source='Specialization in Computing Systems'  chunk_index=0
------------------------------------------------------------
Specialization in Computing Systems

For a Master of Science in Computer Science, Specialization in Computing Systems (18 hours), students must selectfrom the following:
*
The following is a complete look at the courses that may be selected to fulfill the Computing Systems specialization, regardless of campus; only courses listed with
bold
 titles are offered through the online program
.
Core Courses (9 hours)
CS 6505 Computability, Algorithms, and Complexity
or
CS 6515 Introduction to Graduate  …[truncated]

[6] distance=0.466  source='Specialization in Computational Perception and Robotics'  chunk_index=0
------------------------------------------------------------
Specialization in Computational Perception and Robotics

For a Master of Science in Computer Science, Specialization in Computational Perception and Robotics (15 hours), students must selectfrom the following:

*The following is a complete look at the courses that may be selected to fulfill the Computational Perception and Robotics specialization, regardless of campus; only courses listed with
bold
 titles are offered through the online program.

Core Courses (6 hours)

Algorithms:Pick one (1) o …[truncated]

[7] distance=0.468  source='Human-Computer Interaction Specialization Courses Ranked by Difficulty (Summer)'  chunk_index=0
------------------------------------------------------------
Human-Computer Interaction specialization — courses ranked by difficulty (Summer 2025). Rank 1 = easiest, higher rank = harder.

Easiest course in the Human-Computer Interaction specialization: CS 7470 Mobile and Ubiquitous Computing (MUC) — rank 5, Tier 2 (Easy).
Hardest course in the Human-Computer Interaction specialization: CS 6750 Human-Computer Interaction (HCI) — rank 23, Tier 4 (Medium).

All ranked Human-Computer Interaction courses, easiest to hardest:
- rank 5: CS 7470 Mobile and Ubiq …[truncated]

[8] distance=0.472  source='Human-Computer Interaction Specialization Courses Ranked by Difficulty (Spring/Fall)'  chunk_index=0
------------------------------------------------------------
Human-Computer Interaction specialization — courses ranked by difficulty (Spring/Fall 2025). Rank 1 = easiest, higher rank = harder.

Easiest course in the Human-Computer Interaction specialization: CS 6795 Introduction to Cognitive Science (ICS) — rank 7, Tier 2 (Easy).
Hardest course in the Human-Computer Interaction specialization: CS 6750 Human-Computer Interaction (HCI) — rank 30, Tier 4 (Medium).

All ranked Human-Computer Interaction courses, easiest to hardest:
- rank 7: CS 6795 Introduc …[truncated]

```bash
.venv/bin/python scripts/embed_and_retrieve.py query "What are the elective options for Machine Learning?"
```

loading embedding model: all-MiniLM-L6-v2 ...

QUERY: What are the elective options for Machine Learning?
------------------------------------------------------------

[1] distance=0.386  source='Specialization in Machine Learning'  chunk_index=0
------------------------------------------------------------
Specialization in Machine Learning

For a Master of Science in Computer Science, Specialization in Machine Learning (15 hours), students must select from the following:
*The following is a complete look at the courses that may be selected to fulfill the Machine Learning specialization, regardless of campus; only courses listed with
bold
 titles are offered through the online program.
Core Courses (6 hours)
Algorithms: Pick one (1) of:
CS 6505 Computability, Algorithms, and Complexity
CS 6515 Int …[truncated]

[2] distance=0.442  source='Machine Learning Specialization Courses Ranked by Difficulty (Spring/Fall)'  chunk_index=0
------------------------------------------------------------
Machine Learning specialization — courses ranked by difficulty (Spring/Fall 2025). Rank 1 = easiest, higher rank = harder.

Easiest course in the Machine Learning specialization: CS 7650 Natural Language (NLP) — rank 8, Tier 2 (Easy).
Hardest course in the Machine Learning specialization: CS 6476 Computer Vision (CV) — rank 63, Tier 7 (Tell your Loved Ones goodbye).

All ranked Machine Learning courses, easiest to hardest:
- rank 8: CS 7650 Natural Language (NLP) — Tier 2
- rank 9: CS 6603 AI, E …[truncated]

[3] distance=0.454  source='Machine Learning Specialization Courses Ranked by Difficulty (Summer)'  chunk_index=0
------------------------------------------------------------
Machine Learning specialization — courses ranked by difficulty (Summer 2025). Rank 1 = easiest, higher rank = harder.

Easiest course in the Machine Learning specialization: CS 6603 AI, Ethics, and Society (AIES) — rank 3, Tier 1 (Summer Vacation).
Hardest course in the Machine Learning specialization: CS 6515 Introduction to Graduate Algorithms (GA) — rank 49, Tier 7 (Tell your Loved Ones goodbye).

All ranked Machine Learning courses, easiest to hardest:
- rank 3: CS 6603 AI, Ethics, and Socie …[truncated]

[4] distance=0.529  source='Computational Perception and Robotics Specialization Courses Ranked by Difficulty (Spring/Fall)'  chunk_index=0
------------------------------------------------------------
Computational Perception and Robotics specialization — courses ranked by difficulty (Spring/Fall 2025). Rank 1 = easiest, higher rank = harder.

Easiest course in the Computational Perception and Robotics specialization: CS 7650 Natural Language (NLP) — rank 8, Tier 2 (Easy).
Hardest course in the Computational Perception and Robotics specialization: CS 6475 Computational Photography (CP) — rank 65, Tier 7 (Tell your Loved Ones goodbye).

All ranked Computational Perception and Robotics courses, …[truncated]

[5] distance=0.529  source='Specialization in Computational Perception and Robotics'  chunk_index=0
------------------------------------------------------------
Specialization in Computational Perception and Robotics

For a Master of Science in Computer Science, Specialization in Computational Perception and Robotics (15 hours), students must selectfrom the following:

*The following is a complete look at the courses that may be selected to fulfill the Computational Perception and Robotics specialization, regardless of campus; only courses listed with
bold
 titles are offered through the online program.

Core Courses (6 hours)

Algorithms:Pick one (1) o …[truncated]

[6] distance=0.541  source='Computational Perception and Robotics Specialization Courses Ranked by Difficulty (Summer)'  chunk_index=0
------------------------------------------------------------
Computational Perception and Robotics specialization — courses ranked by difficulty (Summer 2025). Rank 1 = easiest, higher rank = harder.

Easiest course in the Computational Perception and Robotics specialization: CS 7650 Natural Language (NLP) — rank 9, Tier 2 (Easy).
Hardest course in the Computational Perception and Robotics specialization: CS 6515 Introduction to Graduate Algorithms (GA) — rank 49, Tier 7 (Tell your Loved Ones goodbye).

All ranked Computational Perception and Robotics cou …[truncated]

[7] distance=0.552  source='Specialization in Artificial Intelligence'  chunk_index=0
------------------------------------------------------------
Specialization in Artificial Intelligence (formerly Interactive Intelligence)

For a Master of Science in Computer Science, Specialization in Artificial Intelligence (15 hours), students must select from the following:
*The following is a complete look at the courses that may be selected to fulfill the Artificial Intelligence specialization, regardless of campus; only courses listed with
bold
 titles are offered through the online program.
Core Courses (9 hours)
Algorithms and Design: Take one ( …[truncated]

[8] distance=0.602  source='Artificial Intelligence Specialization Courses Ranked by Difficulty (Spring/Fall)'  chunk_index=0
------------------------------------------------------------
Artificial Intelligence specialization — courses ranked by difficulty (Spring/Fall 2025). Rank 1 = easiest, higher rank = harder.

Easiest course in the Artificial Intelligence specialization: CS 6795 Introduction to Cognitive Science (ICS) — rank 7, Tier 2 (Easy).
Hardest course in the Artificial Intelligence specialization: CS 6476 Computer Vision (CV) — rank 63, Tier 7 (Tell your Loved Ones goodbye).

All ranked Artificial Intelligence courses, easiest to hardest:
- rank 7: CS 6795 Introducti …[truncated]

