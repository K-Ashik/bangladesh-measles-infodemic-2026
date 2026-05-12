# bangladesh-measles-infodemic-2026
In early 2026, Bangladesh experienced a severe measles outbreak across the Dhaka and Chattogram divisions. While standard epidemiological models treat outbreaks as purely biological phenomena, this study forensically reconstructs the outbreak as a systemic administrative collapse. Utilizing a multi-disciplinary data science approach—combining automated PDF data extraction, mathematical transmission modeling (𝑅𝑡), and Zero-Shot NLP sentiment analysis of YouTube comments— which demonstrate that the outbreak was triggered by a “Legislative Incubation Period.” Health worker strikes in October 2025 halted routine vaccinations, leading local administrators to submit falsified, >100% coverage metrics (“Phantom Data”). During the resulting healthcare vacuum, citizens turned to social media for triage, creating an “infodemic” of vaccine skepticism weeks before official government reporting began. This paper proves that biological outbreaks are deeply accelerated by institutional friction and digital misinformation.

# 1. Introduction
Measles is one of the most contagious airborne human pathogens, boasting a Basic Reproduction Number (𝑅0) of 12 to 18. Because of this extreme infectivity, populations require a strict 95% vaccination coverage rate to maintain herd immunity. Historically, epidemiological reports in Bangladesh have blamed outbreaks on “vaccine hesitancy” or “logistical delays.” However, these explanations ignore the political reality on the ground. During the political transition of late 2025, frontline Health Assistants initiated a massive strike over unpaid wages (the 6-point demand), explicitly halting routine immunization. The motivation for this research was to move beyond biological blame and mathematically quantify the human cost of administrative red tape. The hypothesis of the study is that the government’s official vaccination data was masking a catastrophic immunity gap, and that terrified citizens were forced to navigate this gap alone through digital channels.

<img width="1920" height="1152" alt="image" src="https://github.com/user-attachments/assets/24897202-db4f-404a-992b-0f1f944ef19c" />

# 2. Data Integration
To circumvent incomplete and sanitized official dashboards, a custom, multi-source data pipeline was built:

Epidemiological Surveillance (Web Scraping & OCR): Directorate General of Health Services (DGHS) situation reports are published as non-machine-readable PDFs hidden behind nested web architectures.An automated Python web scrapers and Dual-Engine OCR (Optical Character Recognition) scripts were deployed to extract daily case counts, fatalities, and regional vaccination data, overcoming regular expression traps and shifting column layouts.

Institutional Friction Timeline: The timeline of the Health Assistant strikes (October–December 2025) was rigorously sourced from historical news archives and cross-referenced with public labor demands.

Digital Sentiment Surveillance (YouTube API): To capture the public’s real-time response, the YouTube Data API was used to execute a global, Bengali-language boolean search, extracting thousands of comments from news broadcasts regarding the measles outbreak during the “silent spread” period.

