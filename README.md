# Smart Recruitment SaaS – Resume Screening Tool

## 📌 Project Overview

Smart Recruitment SaaS is an AI-driven resume screening and candidate shortlisting platform designed to simplify and speed up the hiring process. The system automatically parses resumes, evaluates them against job descriptions, and ranks candidates based on relevance scores.

This project is **currently under development**, and focuses on building a scalable, backend-heavy recruitment solution with intelligent screening, asynchronous processing, and efficient data handling.

---

## ✨ Key Features

* 📄 Resume upload and storage (PDF/DOCX)
* 🔍 Resume parsing and text extraction
* 🧠 AI-based resume–job description matching
* 📊 Candidate scoring and ranking
* 🏆 Display top-N matched resumes
* ⚡ Asynchronous resume processing using background workers
* 🗄️ Structured data storage using MySQL
* 🚀 Optimized performance with Redis caching

---

## 🛠️ Tech Stack

### Backend

* **Python**
* **Django / Django REST Framework**
* **MySQL** (Primary Database)
* **Redis** (Caching & Message Broker)
* **Celery** (Asynchronous Task Queue)

### AI / NLP

* **Sentence Transformers** (Semantic similarity)
* **NLP-based text preprocessing**

### Tools & Libraries

* pdfplumber
* python-docx
* NumPy

---

## ⚙️ System Architecture (High-Level)

1. User uploads resume(s)
2. Resume files are stored with unique identifiers
3. Celery workers asynchronously:

   * Extract resume text
   * Parse and clean content
   * Compute similarity scores with job description
4. Parsed data and scores are stored in MySQL
5. Redis is used for task queuing and caching
6. Backend APIs return ranked candidate results

---

## 🗃️ Database Design (Simplified)

* **Resume Table**

  * Resume ID
  * Stored file name (UUID-based)
  * Original file name
  * Parsed text
  * Matching score
  * Upload timestamp

* **Job Description Table**

  * Job ID
  * Job description text

---

## 🚧 Project Status

🟡 **In Progress**

Current focus areas:

* Redis & Celery integration
* Performance optimization for bulk resume uploads
* Improving matching accuracy
* API refinement and error handling

Planned enhancements:

* Recruiter dashboard
* Advanced filtering (skills, experience, keywords)
* Role-based access control
* Cloud deployment

---

## ▶️ How to Run (Development Setup)

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies
4. Configure MySQL and Redis
5. Run database migrations
6. Start Django server
7. Start Redis server
8. Run Celery worker

---

