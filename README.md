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

The following are five chunks from hybrid chunking after running the command below: 
```bash
python3 scripts/chunk_documents.py --print 5
```
95 chunks from 13 files (target 200 tok, overlap 20)

======================================================================
CHUNK 0 | OMS Reviews (omscentral) | ~191 tok
----------------------------------------------------------------------
OMS Reviews
Reviews
OMSCS Notes
# of Reviews
Course
Code(s)
        Rating  Difficulty      Workload        Reviews

Course name
Machine Learning
Reviews URL
Reviews
GATech URL
GT Official
        CS-7641
        3.12    4.15    22.55   527

Course name
Introduction to Graduate Algorithms
Reviews URL
Reviews
GATech URL
GT Official
        CS-6515
        3.28    4.05    19.13   512

Course name
Computer Networks
Reviews URL
Reviews
GATech URL
GT Official
OMSCSNotes URL
Lecture Notes
        CS-6250
        3.47    2.42    8.91    507

Course name
Introduction to Information Security
Reviews URL
Reviews
GATech URL
GT Official
OMSCSNotes URL
Lecture Notes
        CS-6035
        3.43    2.57    10.70   493

Course name
Machine Learning for Trading
Reviews URL
Reviews
GATech URL
GT Official
OMSCSNotes URL
Lecture Notes
        CS-7646
        3.88    2.66    12.10   481

Course name
Graduate Introduction to Operating Systems
Reviews URL
Reviews
GATech URL
GT Official
OMSCSNotes URL
Lecture Notes
        CS-6200
        4.39    3.69    18.47   380

Course name
Software Development Process
Reviews URL
Reviews
GATech URL
GT Official

======================================================================
CHUNK 1 | OMS Reviews (omscentral) | ~99 tok
----------------------------------------------------------------------
4.39    3.69    18.47   380

Course name
Software Development Process
Reviews URL
Reviews
GATech URL
GT Official
        CS-6300
        3.56    2.31    9.06    376

Course name
Knowledge-Based AI
Reviews URL
Reviews
GATech URL
GT Official
        CS-7637
        3.54    3.07    14.11   367

Course name
Artificial Intelligence Techniques for Robotics
Reviews URL
Reviews
GATech URL
GT Official
OMSCSNotes URL
Lecture Notes
        CS-7638
        3.97    3.00    12.92   337

Course name
Artificial Intelligence
Reviews URL
Reviews
GATech URL
GT Official
        CS-6601
        4.03    4.07    22.32   322

======================================================================
CHUNK 2 | omscs.rocks capacity sheet | ~203 tok
----------------------------------------------------------------------
The owner has graduated a long time so unless the API works again use https://www.omshub.org/schedule for LIVE seats.,,,,,Used to be a Student Project in CS 6750 HCI back in 2022. Has graduated in 2024 so slowly trying to sunset this...,,,,,,,"Fall
2025",,"Summer
2025",,"Spring
2025",,"Fall
2024",,"Summer
2024",,"Spring
2024",,"Fall
2023",,"Summer
2023",,"Spring
2023",
"www.omscs.rocks
tinyurl.com/gt-omscs",,"⌚ Time in Atlanta, GA
(Last Refreshed)","04 Jun 2026, 18:40",,OMSCS Latest Orientation Doc,,,,"◄ Read, Understand or be TROLLED in Reddit, Slack & Ed.",,,,,,,,,,,,,,,,,,,,
,,,,,OMSCS Orientation Videos,,,,OMSCS Course Planner,,,,,,,,,,,,,,,,,,,,
OMSCS Slack,,OMS Computer Science Study Slack,omscs-study.slack.com,,Specs,Comp. Systems,Arti. Intelligence,Percept & Robo,Comp. Graphics,Machine Learning,H-C Interaction,,,,,,,,,,,,,,,,,,
OMSCS Reddit,r/OMSCS,OMS Computer Science Subreddit,reddit.com/r/OMSCS,,Core,CS 6515 + 2 Sys,1 A/D + 2 Intel,CS 6515 + 1 Intel,CS 6515 + 1 Graphix,CS 6515 + 1 Intel,Take All 2,,,,,,,,,,,,,,,,,,
OMSA Slack,,OMS Analytics Study Slack,omsa-study.slack.com,,Elective,Pick 3 - inc. Core,Pick Any 2,Pick 3 - w/ 1 P + 1 R,Pick 3 - inc. Core,Pick Any 3,Pick 3 - w/ 1 D + 1 I,,,,,,,,,,,,,,,,,,
OMSCY Slack,,OMS Cybersecurity Study Slack,oms-cybersecurity.slack.com,"*Primary

======================================================================
CHUNK 3 | omscs.rocks capacity sheet | ~195 tok
----------------------------------------------------------------------
OMSA Slack,,OMS Analytics Study Slack,omsa-study.slack.com,,Elective,Pick 3 - inc. Core,Pick Any 2,Pick 3 - w/ 1 P + 1 R,Pick 3 - inc. Core,Pick Any 3,Pick 3 - w/ 1 D + 1 I,,,,,,,,,,,,,,,,,,
OMSCY Slack,,OMS Cybersecurity Study Slack,oms-cybersecurity.slack.com,"*Primary
Language",Free,Pick 4 - inc. above ,Pick 5 - inc. above ,Pick 5 - inc. above ,Pick 5 - inc. above ,Pick 5 - inc. above ,Pick 5 - inc. above ,"Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left"
Code,AKA,Course Name,Slack Study Group,,Found?,Comp. Systems,Arti. Intelligence,Percept & Robo,Comp. Graphics,Machine Learning,H-C Interaction,,,,,,,,,,,,,,,,,,
1,,CS/CSE Courses,,,"Unless otherwise stated, those not highlighted can be taken as ""Free Electives"".",,,,,,,,,,,,,,,,,,,,,,,,
CS 6035,iIS,Introduction to Information Security,#cs6035,JavaScript,
,Elective,,,,,,750,203,700,384,850,189,950,298,700,310,750,62,700,74,700,252,750,56
CS 6150,C4G 😇,Computing for Good,#cs6150,English,⛔,,,,,,,❄️ Break,,☀️ Break,,50,1,50,2,☀️ Break,,50,2,CS 8903 C4G,,☀️ Break,,50,1
CS 6200,GIOS,Operating Systems - Graduate Introduction,omscs6200.slack.com,C / C++,
,Elective,,,,,,1100,47,750,460,1000,0,900,0,750,511,850,15,700,7,750,532,750,74
CS 6210,AOS,Operating Systems - Advanced,#cs6210,C / C++,
,Core | Systems,,,,,,400,34,☀️ Break,,425,59,400,55,☀️ Break,,300,47,250,48,☀️ Break,,200,26

======================================================================
CHUNK 4 | omscs.rocks capacity sheet | ~204 tok
----------------------------------------------------------------------
CS 6200,GIOS,Operating Systems - Graduate Introduction,omscs6200.slack.com,C / C++,
,Elective,,,,,,1100,47,750,460,1000,0,900,0,750,511,850,15,700,7,750,532,750,74
CS 6210,AOS,Operating Systems - Advanced,#cs6210,C / C++,
,Core | Systems,,,,,,400,34,☀️ Break,,425,59,400,55,☀️ Break,,300,47,250,48,☀️ Break,,200,26
CS 6211,SDCC,Systems Design for Cloud Computing (req. A/B AOS),#cs6211,Python / Go,
,Elective,,,,,,60,12,☀️ Break,,48,9,60,24,☀️ Break,,50,4,75,39,☀️ Break,,75,33
CS 6238,SCS,Secure Computer Systems,OMSCyber #cs6238,C / C++,
,Elective,,,,,,150,116,100,88,100,71,150,117,100,85,100,59,150,117,100,75,100,59
CS 6250,CN,Computer Networks,#cs6250,Python,
,Core | Systems,,,,,,1100,0,700,15,950,0,900,3,700,0,700,1,700,2,700,0,700,1
CS 6260,AC,Applied Cryptography,#cs6260,Math,
,Elective,,,,,,100,30,☀️ Break,,100,24,100,39,☀️ Break,,100,49,100,32,☀️ Break,,100,21
CS 6261,SIR,Security Incident Response,#cs6261,English,⛔,,,,,,,50,0,☀️ Break,,50,0,50,21,☀️ Break,,50,0,
️ First Offer,,,,,
CS 6262,NetSec,Network Security,#cs6262,Various,
,Elective,,,,,,250,5,300,116,250,23,250,64,300,186,300,119,300,72,300,111,300,34
CS 6263,CPSS,Cyber Physical - Systems Security,#cs6263,Various,
,Elective,,,,,,100,59,150,133,100,43,200,157,150,112,100,22,100,37,150,101,150,81
CS 6264,SND,Info Security Lab - System & Network Defenses,#cs6264,Various,
,Elective,,,,,,50,32,50,31,🌸 Break,,50,33,50,39,🌸 Break,,50,37,75,29,🌸 Break,
CS 6265,BE,Info Security Lab - Binary Exploitation,#cs6265,Various,⛔,,,,,,,50,4,50,25,50,15,50,10,50,33,50,21,50,18,50,21,50,28
CS 6290,HPCA,High-Performance Computer Architecture,#cs6290,C / C++,
,Core | Systems,,,,,,400,55,200,40,350,34,350,23,150,15,300,27,250,15,100,0,250,12
CS 6291,ESO,Embedded Systems Optimizations,#cs6291,C / C++,
,Elective,,,,,,100,79,100,87,100,55,150,115,100,81,100,46,50,9,100,77,100,57
CS 6300,SDP,Software - Development Process,#cs6300,Java,
,Core | Systems,Core | Algo/Design,,,,,950,0,800,15,950,0,850,4,800,3,825,1,775,0,550,0,750,0
CS 6310,SAD 😥,Software - Architecture & Design,#cs6310,Java,
,Elective,,,,,,550,199,650,475,550,217,650,326,650,531,600,169,600,232,650,434,600,82
CS 6340,SAT,Software - Analysis & Testing,omscs6340.slack.com,C / C++,
,Elective,,,,,,400,137,350,167,400,39,350,40,350,190,350,136,350,125,350,134,350,31
CS 6400,DBS,Database Systems - Concepts & Design,OMSA #cs6400_database,SQL,
,Core | Systems,,,,,,650,263,400,269,650,131,750,214,400,269,600,133,600,103,400,132,550,54
CS 6422,DSI,Database Systems - Implementation,#cs6422,C++,

The following are 5 chunks without hybrid chunking after running the command below:
```bash
python3 scripts/chunk_documents.py --no-hybrid --print 5
```
89 chunks from 13 files (target 200 tok, overlap 20)


======================================================================
CHUNK 0 | OMS Reviews (omscentral) | ~191 tok
----------------------------------------------------------------------
OMS Reviews
Reviews
OMSCS Notes
# of Reviews
Course
Code(s)
        Rating  Difficulty      Workload        Reviews

Course name
Machine Learning
Reviews URL
Reviews
GATech URL
GT Official
        CS-7641
        3.12    4.15    22.55   527

Course name
Introduction to Graduate Algorithms
Reviews URL
Reviews
GATech URL
GT Official
        CS-6515
        3.28    4.05    19.13   512

Course name
Computer Networks
Reviews URL
Reviews
GATech URL
GT Official
OMSCSNotes URL
Lecture Notes
        CS-6250
        3.47    2.42    8.91    507

Course name
Introduction to Information Security
Reviews URL
Reviews
GATech URL
GT Official
OMSCSNotes URL
Lecture Notes
        CS-6035
        3.43    2.57    10.70   493

Course name
Machine Learning for Trading
Reviews URL
Reviews
GATech URL
GT Official
OMSCSNotes URL
Lecture Notes
        CS-7646
        3.88    2.66    12.10   481

Course name
Graduate Introduction to Operating Systems
Reviews URL
Reviews
GATech URL
GT Official
OMSCSNotes URL
Lecture Notes
        CS-6200
        4.39    3.69    18.47   380

Course name
Software Development Process
Reviews URL
Reviews
GATech URL
GT Official

======================================================================
CHUNK 1 | OMS Reviews (omscentral) | ~99 tok
----------------------------------------------------------------------
4.39    3.69    18.47   380

Course name
Software Development Process
Reviews URL
Reviews
GATech URL
GT Official
        CS-6300
        3.56    2.31    9.06    376

Course name
Knowledge-Based AI
Reviews URL
Reviews
GATech URL
GT Official
        CS-7637
        3.54    3.07    14.11   367

Course name
Artificial Intelligence Techniques for Robotics
Reviews URL
Reviews
GATech URL
GT Official
OMSCSNotes URL
Lecture Notes
        CS-7638
        3.97    3.00    12.92   337

Course name
Artificial Intelligence
Reviews URL
Reviews
GATech URL
GT Official
        CS-6601
        4.03    4.07    22.32   322

======================================================================
CHUNK 2 | omscs.rocks capacity sheet | ~203 tok
----------------------------------------------------------------------
The owner has graduated a long time so unless the API works again use https://www.omshub.org/schedule for LIVE seats.,,,,,Used to be a Student Project in CS 6750 HCI back in 2022. Has graduated in 2024 so slowly trying to sunset this...,,,,,,,"Fall
2025",,"Summer
2025",,"Spring
2025",,"Fall
2024",,"Summer
2024",,"Spring
2024",,"Fall
2023",,"Summer
2023",,"Spring
2023",
"www.omscs.rocks
tinyurl.com/gt-omscs",,"⌚ Time in Atlanta, GA
(Last Refreshed)","04 Jun 2026, 18:40",,OMSCS Latest Orientation Doc,,,,"◄ Read, Understand or be TROLLED in Reddit, Slack & Ed.",,,,,,,,,,,,,,,,,,,,
,,,,,OMSCS Orientation Videos,,,,OMSCS Course Planner,,,,,,,,,,,,,,,,,,,,
OMSCS Slack,,OMS Computer Science Study Slack,omscs-study.slack.com,,Specs,Comp. Systems,Arti. Intelligence,Percept & Robo,Comp. Graphics,Machine Learning,H-C Interaction,,,,,,,,,,,,,,,,,,
OMSCS Reddit,r/OMSCS,OMS Computer Science Subreddit,reddit.com/r/OMSCS,,Core,CS 6515 + 2 Sys,1 A/D + 2 Intel,CS 6515 + 1 Intel,CS 6515 + 1 Graphix,CS 6515 + 1 Intel,Take All 2,,,,,,,,,,,,,,,,,,
OMSA Slack,,OMS Analytics Study Slack,omsa-study.slack.com,,Elective,Pick 3 - inc. Core,Pick Any 2,Pick 3 - w/ 1 P + 1 R,Pick 3 - inc. Core,Pick Any 3,Pick 3 - w/ 1 D + 1 I,,,,,,,,,,,,,,,,,,
OMSCY Slack,,OMS Cybersecurity Study Slack,oms-cybersecurity.slack.com,"*Primary

======================================================================
CHUNK 3 | omscs.rocks capacity sheet | ~195 tok
----------------------------------------------------------------------
OMSA Slack,,OMS Analytics Study Slack,omsa-study.slack.com,,Elective,Pick 3 - inc. Core,Pick Any 2,Pick 3 - w/ 1 P + 1 R,Pick 3 - inc. Core,Pick Any 3,Pick 3 - w/ 1 D + 1 I,,,,,,,,,,,,,,,,,,
OMSCY Slack,,OMS Cybersecurity Study Slack,oms-cybersecurity.slack.com,"*Primary
Language",Free,Pick 4 - inc. above ,Pick 5 - inc. above ,Pick 5 - inc. above ,Pick 5 - inc. above ,Pick 5 - inc. above ,Pick 5 - inc. above ,"Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left"
Code,AKA,Course Name,Slack Study Group,,Found?,Comp. Systems,Arti. Intelligence,Percept & Robo,Comp. Graphics,Machine Learning,H-C Interaction,,,,,,,,,,,,,,,,,,
1,,CS/CSE Courses,,,"Unless otherwise stated, those not highlighted can be taken as ""Free Electives"".",,,,,,,,,,,,,,,,,,,,,,,,
CS 6035,iIS,Introduction to Information Security,#cs6035,JavaScript,
,Elective,,,,,,750,203,700,384,850,189,950,298,700,310,750,62,700,74,700,252,750,56
CS 6150,C4G 😇,Computing for Good,#cs6150,English,⛔,,,,,,,❄️ Break,,☀️ Break,,50,1,50,2,☀️ Break,,50,2,CS 8903 C4G,,☀️ Break,,50,1
CS 6200,GIOS,Operating Systems - Graduate Introduction,omscs6200.slack.com,C / C++,
,Elective,,,,,,1100,47,750,460,1000,0,900,0,750,511,850,15,700,7,750,532,750,74
CS 6210,AOS,Operating Systems - Advanced,#cs6210,C / C++,
,Core | Systems,,,,,,400,34,☀️ Break,,425,59,400,55,☀️ Break,,300,47,250,48,☀️ Break,,200,26

======================================================================
CHUNK 4 | omscs.rocks capacity sheet | ~204 tok
----------------------------------------------------------------------
CS 6200,GIOS,Operating Systems - Graduate Introduction,omscs6200.slack.com,C / C++,
,Elective,,,,,,1100,47,750,460,1000,0,900,0,750,511,850,15,700,7,750,532,750,74
CS 6210,AOS,Operating Systems - Advanced,#cs6210,C / C++,
,Core | Systems,,,,,,400,34,☀️ Break,,425,59,400,55,☀️ Break,,300,47,250,48,☀️ Break,,200,26
CS 6211,SDCC,Systems Design for Cloud Computing (req. A/B AOS),#cs6211,Python / Go,
,Elective,,,,,,60,12,☀️ Break,,48,9,60,24,☀️ Break,,50,4,75,39,☀️ Break,,75,33
CS 6238,SCS,Secure Computer Systems,OMSCyber #cs6238,C / C++,
,Elective,,,,,,150,116,100,88,100,71,150,117,100,85,100,59,150,117,100,75,100,59
CS 6250,CN,Computer Networks,#cs6250,Python,
,Core | Systems,,,,,,1100,0,700,15,950,0,900,3,700,0,700,1,700,2,700,0,700,1
CS 6260,AC,Applied Cryptography,#cs6260,Math,
,Elective,,,,,,100,30,☀️ Break,,100,24,100,39,☀️ Break,,100,49,100,32,☀️ Break,,100,21
CS 6261,SIR,Security Incident Response,#cs6261,English,⛔,,,,,,,50,0,☀️ Break,,50,0,50,21,☀️ Break,,50,0,
️ First Offer,,,,,
CS 6262,NetSec,Network Security,#cs6262,Various,
,Elective,,,,,,250,5,300,116,250,23,250,64,300,186,300,119,300,72,300,111,300,34
CS 6263,CPSS,Cyber Physical - Systems Security,#cs6263,Various,
,Elective,,,,,,100,59,150,133,100,43,200,157,150,112,100,22,100,37,150,101,150,81
CS 6264,SND,Info Security Lab - System & Network Defenses,#cs6264,Various,
,Elective,,,,,,50,32,50,31,🌸 Break,,50,33,50,39,🌸 Break,,50,37,75,29,🌸 Break,
CS 6265,BE,Info Security Lab - Binary Exploitation,#cs6265,Various,⛔,,,,,,,50,4,50,25,50,15,50,10,50,33,50,21,50,18,50,21,50,28
CS 6290,HPCA,High-Performance Computer Architecture,#cs6290,C / C++,
,Core | Systems,,,,,,400,55,200,40,350,34,350,23,150,15,300,27,250,15,100,0,250,12
CS 6291,ESO,Embedded Systems Optimizations,#cs6291,C / C++,
,Elective,,,,,,100,79,100,87,100,55,150,115,100,81,100,46,50,9,100,77,100,57
CS 6300,SDP,Software - Development Process,#cs6300,Java,
,Core | Systems,Core | Algo/Design,,,,,950,0,800,15,950,0,850,4,800,3,825,1,775,0,550,0,750,0
CS 6310,SAD 😥,Software - Architecture & Design,#cs6310,Java,
,Elective,,,,,,550,199,650,475,550,217,650,326,650,531,600,169,600,232,650,434,600,82
CS 6340,SAT,Software - Analysis & Testing,omscs6340.slack.com,C / C++,
,Elective,,,,,,400,137,350,167,400,39,350,40,350,190,350,136,350,125,350,134,350,31
CS 6400,DBS,Database Systems - Concepts & Design,OMSA #cs6400_database,SQL,
,Core | Systems,,,,,,650,263,400,269,650,131,750,214,400,269,600,133,600,103,400,132,550,54
CS 6422,DSI,Database Systems - Implementation,#cs6422,C++,

We can also experiment with chunk and overlap size. Run the following command to get the below results if we wanted a chunk size of 400 and overlap size of 40.
```bash
scripts/chunk_documents.py --size 400 --overlap 40 --stats
```
chunks per source:
    1  OMS Reviews (omscentral)
    4  omscs.rocks capacity sheet
    4  Course & Specs Megathread
   12  Courses Ranked by Difficulty Spring/Fall 2025
   11  Courses Ranked by Difficulty Summer 2025
    4  Workload Distributions
    4  OMSHub
    1  Specialization in Machine Learning
    1  Specialization in Artificial Intelligence
    1  Specialization in Human-Computer Interaction
    1  Specialization in Computational Perception and Robotics
    1  Specialization in Computing Systems
    1  Specialization in Computer Graphics
    1  Computer Graphics Specialization Courses Ranked by Difficulty (Spring/Fall)
    1  Computer Graphics Specialization Courses Ranked by Difficulty (Summer)
    1  Artificial Intelligence Specialization Courses Ranked by Difficulty (Spring/Fall)
    1  Artificial Intelligence Specialization Courses Ranked by Difficulty (Summer)
    1  Machine Learning Specialization Courses Ranked by Difficulty (Spring/Fall)
    1  Machine Learning Specialization Courses Ranked by Difficulty (Summer)
    1  Human-Computer Interaction Specialization Courses Ranked by Difficulty (Spring/Fall)
    1  Human-Computer Interaction Specialization Courses Ranked by Difficulty (Summer)
    1  Computational Perception and Robotics Specialization Courses Ranked by Difficulty (Spring/Fall)
    1  Computational Perception and Robotics Specialization Courses Ranked by Difficulty (Summer)
    1  Computing Systems Specialization Courses Ranked by Difficulty (Spring/Fall)
    1  Computing Systems Specialization Courses Ranked by Difficulty (Summer)
(.venv) (base) roshnisingh@Roshnis-MacBook-Pro ai201-project1-unofficial-guide % python3 scripts/chunk_documents.py --no-hybrid --print 5          
89 chunks from 13 files (target 200 tok, overlap 20)


======================================================================
CHUNK 0 | OMS Reviews (omscentral) | ~191 tok
----------------------------------------------------------------------
OMS Reviews
Reviews
OMSCS Notes
# of Reviews
Course
Code(s)
        Rating  Difficulty      Workload        Reviews

Course name
Machine Learning
Reviews URL
Reviews
GATech URL
GT Official
        CS-7641
        3.12    4.15    22.55   527

Course name
Introduction to Graduate Algorithms
Reviews URL
Reviews
GATech URL
GT Official
        CS-6515
        3.28    4.05    19.13   512

Course name
Computer Networks
Reviews URL
Reviews
GATech URL
GT Official
OMSCSNotes URL
Lecture Notes
        CS-6250
        3.47    2.42    8.91    507

Course name
Introduction to Information Security
Reviews URL
Reviews
GATech URL
GT Official
OMSCSNotes URL
Lecture Notes
        CS-6035
        3.43    2.57    10.70   493

Course name
Machine Learning for Trading
Reviews URL
Reviews
GATech URL
GT Official
OMSCSNotes URL
Lecture Notes
        CS-7646
        3.88    2.66    12.10   481

Course name
Graduate Introduction to Operating Systems
Reviews URL
Reviews
GATech URL
GT Official
OMSCSNotes URL
Lecture Notes
        CS-6200
        4.39    3.69    18.47   380

Course name
Software Development Process
Reviews URL
Reviews
GATech URL
GT Official

======================================================================
CHUNK 1 | OMS Reviews (omscentral) | ~99 tok
----------------------------------------------------------------------
4.39    3.69    18.47   380

Course name
Software Development Process
Reviews URL
Reviews
GATech URL
GT Official
        CS-6300
        3.56    2.31    9.06    376

Course name
Knowledge-Based AI
Reviews URL
Reviews
GATech URL
GT Official
        CS-7637
        3.54    3.07    14.11   367

Course name
Artificial Intelligence Techniques for Robotics
Reviews URL
Reviews
GATech URL
GT Official
OMSCSNotes URL
Lecture Notes
        CS-7638
        3.97    3.00    12.92   337

Course name
Artificial Intelligence
Reviews URL
Reviews
GATech URL
GT Official
        CS-6601
        4.03    4.07    22.32   322

======================================================================
CHUNK 2 | omscs.rocks capacity sheet | ~203 tok
----------------------------------------------------------------------
The owner has graduated a long time so unless the API works again use https://www.omshub.org/schedule for LIVE seats.,,,,,Used to be a Student Project in CS 6750 HCI back in 2022. Has graduated in 2024 so slowly trying to sunset this...,,,,,,,"Fall
2025",,"Summer
2025",,"Spring
2025",,"Fall
2024",,"Summer
2024",,"Spring
2024",,"Fall
2023",,"Summer
2023",,"Spring
2023",
"www.omscs.rocks
tinyurl.com/gt-omscs",,"⌚ Time in Atlanta, GA
(Last Refreshed)","04 Jun 2026, 18:40",,OMSCS Latest Orientation Doc,,,,"◄ Read, Understand or be TROLLED in Reddit, Slack & Ed.",,,,,,,,,,,,,,,,,,,,
,,,,,OMSCS Orientation Videos,,,,OMSCS Course Planner,,,,,,,,,,,,,,,,,,,,
OMSCS Slack,,OMS Computer Science Study Slack,omscs-study.slack.com,,Specs,Comp. Systems,Arti. Intelligence,Percept & Robo,Comp. Graphics,Machine Learning,H-C Interaction,,,,,,,,,,,,,,,,,,
OMSCS Reddit,r/OMSCS,OMS Computer Science Subreddit,reddit.com/r/OMSCS,,Core,CS 6515 + 2 Sys,1 A/D + 2 Intel,CS 6515 + 1 Intel,CS 6515 + 1 Graphix,CS 6515 + 1 Intel,Take All 2,,,,,,,,,,,,,,,,,,
OMSA Slack,,OMS Analytics Study Slack,omsa-study.slack.com,,Elective,Pick 3 - inc. Core,Pick Any 2,Pick 3 - w/ 1 P + 1 R,Pick 3 - inc. Core,Pick Any 3,Pick 3 - w/ 1 D + 1 I,,,,,,,,,,,,,,,,,,
OMSCY Slack,,OMS Cybersecurity Study Slack,oms-cybersecurity.slack.com,"*Primary

======================================================================
CHUNK 3 | omscs.rocks capacity sheet | ~195 tok
----------------------------------------------------------------------
OMSA Slack,,OMS Analytics Study Slack,omsa-study.slack.com,,Elective,Pick 3 - inc. Core,Pick Any 2,Pick 3 - w/ 1 P + 1 R,Pick 3 - inc. Core,Pick Any 3,Pick 3 - w/ 1 D + 1 I,,,,,,,,,,,,,,,,,,
OMSCY Slack,,OMS Cybersecurity Study Slack,oms-cybersecurity.slack.com,"*Primary
Language",Free,Pick 4 - inc. above ,Pick 5 - inc. above ,Pick 5 - inc. above ,Pick 5 - inc. above ,Pick 5 - inc. above ,Pick 5 - inc. above ,"Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left","Seats
Total","Seats
Left"
Code,AKA,Course Name,Slack Study Group,,Found?,Comp. Systems,Arti. Intelligence,Percept & Robo,Comp. Graphics,Machine Learning,H-C Interaction,,,,,,,,,,,,,,,,,,
1,,CS/CSE Courses,,,"Unless otherwise stated, those not highlighted can be taken as ""Free Electives"".",,,,,,,,,,,,,,,,,,,,,,,,
CS 6035,iIS,Introduction to Information Security,#cs6035,JavaScript,
,Elective,,,,,,750,203,700,384,850,189,950,298,700,310,750,62,700,74,700,252,750,56
CS 6150,C4G 😇,Computing for Good,#cs6150,English,⛔,,,,,,,❄️ Break,,☀️ Break,,50,1,50,2,☀️ Break,,50,2,CS 8903 C4G,,☀️ Break,,50,1
CS 6200,GIOS,Operating Systems - Graduate Introduction,omscs6200.slack.com,C / C++,
,Elective,,,,,,1100,47,750,460,1000,0,900,0,750,511,850,15,700,7,750,532,750,74
CS 6210,AOS,Operating Systems - Advanced,#cs6210,C / C++,
,Core | Systems,,,,,,400,34,☀️ Break,,425,59,400,55,☀️ Break,,300,47,250,48,☀️ Break,,200,26

======================================================================
CHUNK 4 | omscs.rocks capacity sheet | ~204 tok
----------------------------------------------------------------------
CS 6200,GIOS,Operating Systems - Graduate Introduction,omscs6200.slack.com,C / C++,
,Elective,,,,,,1100,47,750,460,1000,0,900,0,750,511,850,15,700,7,750,532,750,74
CS 6210,AOS,Operating Systems - Advanced,#cs6210,C / C++,
,Core | Systems,,,,,,400,34,☀️ Break,,425,59,400,55,☀️ Break,,300,47,250,48,☀️ Break,,200,26
CS 6211,SDCC,Systems Design for Cloud Computing (req. A/B AOS),#cs6211,Python / Go,
,Elective,,,,,,60,12,☀️ Break,,48,9,60,24,☀️ Break,,50,4,75,39,☀️ Break,,75,33
CS 6238,SCS,Secure Computer Systems,OMSCyber #cs6238,C / C++,
,Elective,,,,,,150,116,100,88,100,71,150,117,100,85,100,59,150,117,100,75,100,59
CS 6250,CN,Computer Networks,#cs6250,Python,
,Core | Systems,,,,,,1100,0,700,15,950,0,900,3,700,0,700,1,700,2,700,0,700,1
CS 6260,AC,Applied Cryptography,#cs6260,Math,
,Elective,,,,,,100,30,☀️ Break,,100,24,100,39,☀️ Break,,100,49,100,32,☀️ Break,,100,21
CS 6261,SIR,Security Incident Response,#cs6261,English,⛔,,,,,,,50,0,☀️ Break,,50,0,50,21,☀️ Break,,50,0,
️ First Offer,,,,,
CS 6262,NetSec,Network Security,#cs6262,Various,
,Elective,,,,,,250,5,300,116,250,23,250,64,300,186,300,119,300,72,300,111,300,34
CS 6263,CPSS,Cyber Physical - Systems Security,#cs6263,Various,
,Elective,,,,,,100,59,150,133,100,43,200,157,150,112,100,22,100,37,150,101,150,81
CS 6264,SND,Info Security Lab - System & Network Defenses,#cs6264,Various,
,Elective,,,,,,50,32,50,31,🌸 Break,,50,33,50,39,🌸 Break,,50,37,75,29,🌸 Break,
CS 6265,BE,Info Security Lab - Binary Exploitation,#cs6265,Various,⛔,,,,,,,50,4,50,25,50,15,50,10,50,33,50,21,50,18,50,21,50,28
CS 6290,HPCA,High-Performance Computer Architecture,#cs6290,C / C++,
,Core | Systems,,,,,,400,55,200,40,350,34,350,23,150,15,300,27,250,15,100,0,250,12
CS 6291,ESO,Embedded Systems Optimizations,#cs6291,C / C++,
,Elective,,,,,,100,79,100,87,100,55,150,115,100,81,100,46,50,9,100,77,100,57
CS 6300,SDP,Software - Development Process,#cs6300,Java,
,Core | Systems,Core | Algo/Design,,,,,950,0,800,15,950,0,850,4,800,3,825,1,775,0,550,0,750,0
CS 6310,SAD 😥,Software - Architecture & Design,#cs6310,Java,
,Elective,,,,,,550,199,650,475,550,217,650,326,650,531,600,169,600,232,650,434,600,82
CS 6340,SAT,Software - Analysis & Testing,omscs6340.slack.com,C / C++,
,Elective,,,,,,400,137,350,167,400,39,350,40,350,190,350,136,350,125,350,134,350,31
CS 6400,DBS,Database Systems - Concepts & Design,OMSA #cs6400_database,SQL,
,Core | Systems,,,,,,650,263,400,269,650,131,750,214,400,269,600,133,600,103,400,132,550,54
CS 6422,DSI,Database Systems - Implementation,#cs6422,C++,

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
