# Decoding AI
*The AI whisperer's guide to intelligence.*

Welcome to **Decoding AI**, a modular AI information source and practical workflow toolkit tailored for bioinformatics researchers working across lipidomics, metabolomics, RNA-seq, and systems immunology (focusing on practical examples such as dendritic cell dynamics in lymph nodes). 

This course is built to help colleagues **use AI effectively in daily research**, focusing on practical application, current debates, limitations, and prompting strategies rather than technical model architecture. Designed like a textbook, each module combines readable chapters with hands-on exercises (including no-code alternatives) and concludes with a team hackathon.

> **Privacy First:** Pre-publication omics data, patient-derived material, and unpublished manuscripts must be treated as strictly confidential. Please review Part 3 of Module 1 (`module_01_foundations_and_privacy/README.md`)—and Part 3 of Module 5 before deploying autonomous agents—prior to processing any lab data with cloud models.

*Note on AI assistance:* This course was crafted with the assistance of AI, synthesising online sources alongside two years of personal domain experience. While thoroughly reviewed, subtle errors may exist—feel free to flag any inaccuracies or submit corrections!

## Quickstart

To begin, clone the repository using `git clone https://github.com/HoltropAF/AI_course.git ai-learning-automation` (or download and extract the ZIP archive from GitHub).

Your central hub for the course is `course/dashboard.html`. Opening this file in your browser provides an interactive map tracking your progress through every module without requiring any servers or local installations. While files can be read in any editor, the dashboard offers the optimal visual experience.

For the best environment when working through markdown and presentation files, open the project folder in **VS Code** with the **Marp for VS Code** extension installed:
* **View Slide Presentations (`slides.md`):** Press `Ctrl+K` then `V` (`Cmd+K` then `V` on macOS) to open a side-by-side preview.
* **View Document Files (`.md`):** Press `Ctrl+Shift+V` (`Cmd+Shift+V` on macOS) for enhanced markdown rendering.
* **Exporting Presentations:** Press `Ctrl+Shift+P` and select *Marp: Export Slide Deck* to output to PDF, PowerPoint, or HTML.

Work through the course sequentially following the dashboard roadmap: **Orientation → Modules 1–5 → Module 6 (Team Hackathon)**. Each module contains a main chapter, supplementary readings, a practical exercise, and a self-check.

## Technical Setup

### Prerequisites
Running local experiments requires **Python 3.10+**, **Git**, and [Ollama](https://ollama.com) (for local model inference in Modules 1, 2, and Track B). Optional tools include [Claude Code](https://code.claude.com) (Modules 3–5) and **Node.js 18+** (required for Model Context Protocol servers in Module 4).

### Environment & Verification
Run the following commands in your terminal to set up your virtual environment, download the local Llama model, and verify your installation:

```bash
git clone [https://github.com/HoltropAF/AI_course.git](https://github.com/HoltropAF/AI_course.git) ai-learning-automation
cd ai-learning-automation
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install requests ollama pydantic
ollama pull llama3.1:8b
python module_01_foundations_and_privacy/exercises/test_ollama_local.py
