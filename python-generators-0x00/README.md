# Python Generators: Efficient Data Streaming with MySQL

## Table of Contents
* [1. Project Overview](#1-project-overview)
* [2. Team Roles and Responsibilities](#2-team-roles-and-responsibilities)
* [3. Technology Stack Overview](#3-technology-stack-overview)
* [4. Database Design Overview](#4-database-design-overview)
* [5. Feature Breakdown](#5-feature-breakdown)
* [6. API Security Overview](#6-api-security-overview)
* [7. CI/CD Pipeline Overview](#7-cicd-pipeline-overview)
* [8. Resources](#8-resources)
* [9. License](#9-license)
* [10. Created By](#10-created-by)

---

## 1. Project Overview

**Brief Description:**  
This project demonstrates **advanced Python generators** to enable **memory-efficient, scalable data streaming** directly from a MySQL database. Using the `yield` keyword, it implements **lazy loading**, **batch processing**, **pagination**, and **incremental aggregation** — eliminating the need to load entire datasets into memory. This approach is ideal for real-world scenarios such as live data feeds, large-scale analytics, and resource-constrained environments.

The project simulates production-grade data pipelines by integrating Python with MySQL, using CSV-seeded data and enforcing strict constraints on loops and memory usage.

**Project Goals:**
- Master generator functions and lazy evaluation
- Stream database rows one at a time using `yield`
- Process data in batches with filtering (age > 25)
- Implement lazy pagination using `LIMIT`/`OFFSET`
- Compute average age without loading full dataset
- Follow best practices in database connection and cleanup

**Key Tech Stack:**  
**Python 3.x** • **MySQL** • **mysql-connector-python** • **CSV Seeding** • **Git & GitHub**

---

## 2. Team Roles and Responsibilities

| Role                  | Key Responsibility |
|-----------------------|---------------------|
| **Backend Developer** | Implement generator logic, SQL queries, and data streaming |
| **Database Engineer** | Design schema, optimize `user_id` index, seed from CSV |
| **DevOps Engineer**   | Configure MySQL, secure credentials, automate setup |
| **QA Engineer**       | Validate output, enforce loop limits, test memory usage |

---

## 3. Technology Stack Overview

| Technology                  | Purpose in the Project |
|-----------------------------|------------------------|
| **Python 3.x**              | Core language for generators and logic |
| **MySQL**                   | Stores `user_data` with UUID primary key |
| **mysql-connector-python**  | Secure Python-to-MySQL connection driver |
| **CSV (`user_data.csv`)**   | Sample data source for seeding |
| **Generators (`yield`)**    | Enable lazy, on-demand data streaming |
| **Git & GitHub**            | Version control and submission platform |

---

## 4. Database Design Overview

### Key Entities:
- **`user_data`**
  - `user_id` → `CHAR(36)` **Primary Key**, UUID, **Indexed**
  - `name` → `VARCHAR(255)` **NOT NULL**
  - `email` → `VARCHAR(255)` **NOT NULL**
  - `age` → `DECIMAL(5,2)` **NOT NULL**

### Relationships:
- **Single-table design** — no foreign keys
- `user_id` indexed for efficient pagination and lookup

```sql
CREATE TABLE IF NOT EXISTS user_data (
    user_id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age DECIMAL(5,2) NOT NULL,
    INDEX idx_user_id (user_id)
);
```

---

## 5. Feature Breakdown

### `seed.py` – Database Initialization & Seeding
Establishes MySQL connection, creates `ALX_prodev` database and `user_data` table, and inserts records from `user_data.csv` using safe bulk operations.

### `0-stream_users.py` – Row-by-Row Streaming Generator
Implements `stream_users()` — yields one user dictionary at a time using a single cursor loop, enabling real-time processing of large datasets.

### `1-batch_processing.py` – Batch Processing with Filtering
`stream_users_in_batches(batch_size)` yields user batches; `batch_processing()` filters users over age 25 using ≤3 loops total, maintaining memory efficiency.

### `2-lazy_paginate.py` – Lazy Pagination
`lazy_paginate(page_size)` yields full pages only when iterated, using `LIMIT`/`OFFSET` with one loop — true on-demand loading.

### `4-stream_ages.py` – Memory-Efficient Aggregation
`stream_user_ages()` yields ages one by one; average is computed incrementally using ≤2 loops — no full dataset materialization.

---

## 6. API Security Overview

### Environment-Based Credentials
Database credentials stored in environment variables (never hardcoded)

### Explicit Resource Management
All cursors and connections closed with `.close()` to prevent leaks

### Safe SQL Construction
`LIMIT`/`OFFSET` use integer formatting — no SQL injection risk

### Input Scope Control
CSV data trusted for project; production requires validation

### No Persistent Connections
Each function opens and closes its own connection — safe and predictable

---

## 7. CI/CD Pipeline Overview

This project uses a hybrid CI/CD model combining automated checks and manual peer review. An auto-check script validates:

- Required files exist (`seed.py`, `0-stream_users.py`, etc.)
- Function prototypes and generator usage are correct
- Loop constraints are respected (≤1 or ≤3 loops)

Manual QA review (requested via generated link) ensures:

- Code quality, readability, and structure
- Correct `yield` usage and lazy behavior
- Output matches `main.py` test expectations

**Deadline:** Nov 3, 2025, 12:00 AM — review link disabled after  
**Future:** GitHub Actions to auto-run `main.py` tests on push

---

## 8. Resources

- [Python Generators – Real Python](https://realpython.com/introduction-to-python-generators/)
- [MySQL Connector/Python Docs](https://dev.mysql.com/doc/connector-python/en/)
- [Pagination Best Practices](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Link)
- [Lazy Evaluation](https://en.wikipedia.org/wiki/Lazy_evaluation)

---

## 9. License

```
MIT License

Copyright (c) 2025 Phinehas Macharia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 10. Created By

**Phinehas Macharia**  
Backend Engineer | Python | Scalable Systems | Data Pipelines

[![GitHub](https://img.shields.io/badge/GitHub-MachariaP-181717?style=flat&logo=github)](https://github.com/MachariaP)
