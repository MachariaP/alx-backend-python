# 🎯 Python Decorators for Database Operations

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite3-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Decorators](https://img.shields.io/badge/Decorators-Advanced-green?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=opensourceinitiative&logoColor=white)

**Master Python decorators to enhance database operations with elegant, reusable, and production-ready code**

</div>

---

## 📜 Table of Contents
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

### 📋 Brief Description

The **Python Decorators for Database Operations** project is a comprehensive, hands-on learning experience designed to master the art of Python decorators in the context of real-world database management. This project demonstrates how decorators can transform repetitive, boilerplate-heavy database code into clean, maintainable, and highly reusable solutions. Through five progressive tasks, developers learn to implement essential patterns like query logging, automatic connection management, transaction handling, retry mechanisms, and intelligent caching.

This project bridges the gap between theoretical decorator knowledge and practical application in production environments. By focusing on database operations—a critical component of most backend systems—learners gain expertise in writing decorators that solve genuine engineering challenges while adhering to Python best practices and design patterns.

### 🎯 Project Goals

- **Master Decorator Design Patterns**: Understand decorator fundamentals, closure concepts, wrapper functions, and the `functools.wraps` utility to create robust, well-documented decorators
- **Automate Database Operations**: Eliminate repetitive connection handling, transaction management, and error handling code through intelligent decorator abstractions
- **Implement Observability**: Build logging decorators that provide visibility into database queries for debugging, monitoring, and performance analysis
- **Ensure Data Integrity**: Create transaction decorators that guarantee ACID properties through automatic commit/rollback mechanisms with proper error handling
- **Build Resilient Systems**: Develop retry decorators with exponential backoff to handle transient database failures and network issues gracefully
- **Optimize Performance**: Implement caching decorators that reduce database load by storing and reusing query results intelligently
- **Apply Production Patterns**: Learn industry-standard techniques used in frameworks like Django, Flask-SQLAlchemy, and enterprise Python applications

### 🔑 Key Tech Stack

- **Language**: Python 3.8+
- **Database**: SQLite3 (lightweight, file-based SQL database)
- **Core Module**: functools for decorator utilities
- **Design Patterns**: Decorator pattern, higher-order functions
- **Testing**: Manual verification with sample database operations

---

## 2. Team Roles and Responsibilities

| Role | Key Responsibility |
|------|-------------------|
| **Backend Python Developer** | Design and implement custom decorators for database operations, ensuring clean code architecture, proper error handling, and adherence to Python conventions (PEP 8) |
| **Database Administrator (DBA)** | Design database schema (users table), create indexes for performance, analyze query execution plans, and validate that decorators don't introduce performance bottlenecks |
| **Quality Assurance Engineer** | Develop comprehensive test suites for decorators, validate edge cases (connection failures, transaction rollbacks), and ensure decorators work with various database scenarios |
| **DevOps / Site Reliability Engineer** | Monitor decorator-enhanced applications in production, track retry patterns, analyze cache hit rates, and tune performance parameters (retry delays, cache TTL) |
| **Code Reviewer / Technical Lead** | Review decorator implementations for correctness, ensure proper use of `functools.wraps`, validate that decorators are composable, and maintain code quality standards |
| **Systems Architect** | Define decorator interfaces, establish patterns for decorator stacking, design cache invalidation strategies, and ensure decorators scale to production workloads |

---

## 3. Technology Stack Overview

| Technology | Purpose in the Project |
|-----------|----------------------|
| **Python 3.8+** | Core programming language providing native decorator syntax (@decorator), first-class functions, and dynamic typing capabilities essential for metaprogramming patterns |
| **SQLite3** | Lightweight, serverless SQL database engine embedded in Python standard library. Used for demonstrating database operations without requiring external database server setup |
| **functools.wraps** | Critical utility that preserves original function metadata (name, docstring, annotations) when creating wrapper functions, ensuring decorated functions remain introspectable and debuggable |
| **sqlite3.Connection** | Database connection object providing cursor creation, transaction control (commit/rollback), and connection lifecycle management through Python's DB-API 2.0 interface |
| **sqlite3.Cursor** | Executes SQL queries, fetches results (fetchone, fetchall), and manages query state. Essential for all database read/write operations in decorator-enhanced functions |
| **Logging Module** | Provides structured logging capabilities for the query logging decorator, enabling different log levels (DEBUG, INFO, WARNING) and output formatting |
| **Time Module** | Used in retry decorator to implement delay mechanisms between retry attempts, supporting both fixed delays and exponential backoff strategies |
| **Dictionary (dict)** | Simple in-memory data structure used as cache storage in the caching decorator, with query strings as keys and result sets as values for O(1) lookup |
| **Exception Handling** | Try-except-finally blocks ensure proper resource cleanup (closing connections), graceful error handling in transactions, and robust retry logic for transient failures |
| **Higher-Order Functions** | Functions that accept other functions as arguments or return functions (decorator pattern foundation), enabling code composition and behavior modification |
| **Closure** | Inner functions that capture and remember variables from outer function scope, crucial for decorators with parameters (retry_on_failure(retries=3)) |

---

## 4. Database Design Overview

### 🗄️ Key Entities

This project uses a simple but realistic database schema designed to demonstrate decorator functionality in a practical context:

- **Users**: Core entity representing application users with essential fields for authentication and profile information
  - **id** (INTEGER PRIMARY KEY): Auto-incrementing unique identifier for each user
  - **name** (TEXT NOT NULL): User's full name or username
  - **email** (TEXT UNIQUE NOT NULL): User's email address with uniqueness constraint for login purposes
  - **created_at** (TIMESTAMP): Record creation timestamp for audit trails
  - **updated_at** (TIMESTAMP): Last modification timestamp for tracking changes

### 🔗 Relationships

This project focuses on single-table operations to emphasize decorator implementation rather than complex database design:

- **Self-Contained Operations**: Each decorator task operates on the users table independently, demonstrating decorator patterns without requiring foreign keys or joins
- **Transaction Integrity**: The transactional decorator ensures that operations like user updates maintain consistency—if email update fails, no partial changes are committed
- **Cache Key Relationships**: The caching decorator creates an implicit relationship between SQL query strings (keys) and their result sets (values), demonstrating query-result mapping patterns

### 📊 Database Setup Example

```sql
-- Sample database schema for testing decorators
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample test data
INSERT INTO users (name, email) VALUES 
    ('Alice Johnson', 'alice@example.com'),
    ('Bob Smith', 'bob@example.com'),
    ('Carol Williams', 'carol@example.com');
```

**Note**: In production systems, these decorator patterns would scale to complex schemas with multiple tables, foreign key relationships (Users → Orders → OrderItems), and would integrate with ORM frameworks like SQLAlchemy or Django ORM. The decorators remain reusable regardless of schema complexity.

---

## 5. Feature Breakdown

### ✨ Core Functionalities

- **📝 Task 0: Logging Database Queries**  
  Implements a `@log_queries` decorator that intercepts function calls and logs the SQL query string before execution. This decorator enhances observability by providing a clear audit trail of all database operations, making it invaluable for debugging, performance monitoring, and security auditing. The logger captures query patterns, helping identify slow queries, N+1 problems, and potential SQL injection attempts.

- **🔌 Task 1: Automatic Database Connection Management**  
  Creates a `@with_db_connection` decorator that handles the complete connection lifecycle—opening the database connection, passing it to the decorated function, and ensuring proper closure even if exceptions occur. This decorator eliminates repetitive connection boilerplate, prevents resource leaks from unclosed connections, and centralizes connection configuration (database path, timeout settings). Functions can focus purely on business logic without worrying about connection handling.

- **💼 Task 2: Transaction Management with ACID Guarantees**  
  Develops a `@transactional` decorator that wraps database operations in proper transactions with automatic commit on success and rollback on failure. This decorator ensures data integrity by preventing partial updates (atomicity), maintaining consistency during concurrent operations, and providing isolation from other transactions. Critical for operations that modify multiple records or enforce business rules that span multiple queries.

- **🔄 Task 3: Retry Mechanism for Transient Failures**  
  Implements a configurable `@retry_on_failure(retries=3, delay=2)` decorator that automatically retries failed database operations. Handles transient issues like temporary network glitches, database locks, connection pool exhaustion, or brief service unavailability. Supports customizable retry counts and delays (fixed or exponential backoff), logging each retry attempt. Essential for building resilient systems that gracefully handle infrastructure hiccups without manual intervention.

- **⚡ Task 4: Intelligent Query Result Caching**  
  Creates a `@cache_query` decorator that memoizes query results in memory, keyed by the SQL query string. Subsequent identical queries return cached results instantly without hitting the database, dramatically improving performance for read-heavy workloads with repeated queries. Particularly effective for reference data, user profiles, configuration settings, and dashboard queries. Production implementations would add cache invalidation, TTL (time-to-live), and distributed cache backends (Redis, Memcached).

- **🎨 Decorator Composition & Stacking**  
  Demonstrates advanced patterns by combining multiple decorators on a single function (e.g., `@with_db_connection @transactional @retry_on_failure @cache_query`). Shows proper ordering considerations—connection must be outermost, transaction wraps business logic, retry wraps error-prone operations, cache is innermost for query results. This composition creates powerful, declarative function enhancements without modifying function bodies.

- **🛡️ Error Handling & Resource Management**  
  All decorators implement robust error handling using try-except-finally blocks to ensure resources (connections, cursors) are properly released even when exceptions occur. Demonstrates the importance of idempotent retry logic, proper exception propagation, and meaningful error messages that include context (which decorator failed, what operation was attempted).

- **📚 Reusability & Maintainability**  
  By centralizing cross-cutting concerns (logging, connections, transactions, retries, caching) in decorators, the codebase becomes more maintainable. Changes to retry logic, cache strategy, or logging format only need to be updated in one place—the decorator—rather than scattered across dozens of functions. This DRY (Don't Repeat Yourself) principle dramatically reduces code duplication and maintenance burden.

---

## 6. API Security Overview

### 🔒 Security Measures

| Security Measure | Implementation & Importance |
|-----------------|---------------------------|
| **🛡️ SQL Injection Prevention** | All example code uses parameterized queries with `?` placeholders (`cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))`). This prevents SQL injection attacks by separating SQL structure from user-provided data. Never use string interpolation or concatenation for SQL queries—a critical security practice enforced by proper decorator design. |
| **🔐 Connection Security** | Decorators ensure database connections are properly closed in finally blocks, preventing connection leaks that could exhaust connection pools and enable denial-of-service attacks. Production implementations should enforce SSL/TLS for remote database connections, authenticate with strong credentials stored in environment variables (not hardcoded), and use connection pooling with timeouts. |
| **✅ Transaction Isolation** | The `@transactional` decorator enforces proper transaction boundaries, preventing dirty reads, non-repeatable reads, and phantom reads. Proper isolation levels (READ COMMITTED, SERIALIZABLE) prevent race conditions where concurrent users could corrupt data. Rollback on errors ensures failed operations don't leave partial, inconsistent data. |
| **🔄 Retry Attack Mitigation** | The retry decorator includes configurable limits (max retries) to prevent infinite retry loops that could amplify denial-of-service attacks or exhaust system resources. Production implementations should include exponential backoff with jitter to prevent thundering herd problems where many clients retry simultaneously after an outage. |
| **📊 Audit Logging** | The `@log_queries` decorator creates an audit trail of all database operations, essential for security incident response, compliance (GDPR, HIPAA), and forensic analysis. Logs should include timestamps, user context, query parameters (sanitized), and results to track who accessed what data when. Consider structured logging (JSON) for parsing by SIEM systems. |
| **🎯 Least Privilege Principle** | While not implemented in this educational project, production decorators should enforce database user permissions (SELECT-only users for read operations, restricted write permissions). Connection decorators can switch database users based on operation type, ensuring compromised code can't perform unauthorized operations. |
| **🔑 Secrets Management** | Database credentials, connection strings, and API keys must never be hardcoded in decorator implementations. Use environment variables (`os.environ['DB_PASSWORD']`), configuration files outside version control, or secrets management services (AWS Secrets Manager, HashiCorp Vault). Decorators should validate credentials are present at startup, not at query time. |
| **⚠️ Error Message Sanitization** | Decorators should catch exceptions and log detailed technical errors for debugging but return sanitized error messages to end users. Never expose database schema details, table names, column names, or SQL syntax errors to users—this information aids SQL injection attacks and reveals system architecture to attackers. |
| **🧪 Security Testing** | Test decorators with malicious inputs: SQL injection attempts in query parameters, extremely long retry delays (resource exhaustion), cache poisoning with crafted queries, and rollback behavior with concurrent transactions. Validate that decorators fail securely—denying access rather than granting it on errors. |

### 🎯 Why Security Matters in Decorators

Decorators are powerful because they wrap many functions, meaning a security vulnerability in a decorator affects every function it decorates. A single SQL injection flaw in a logging decorator could compromise hundreds of queries. Conversely, properly securing decorators provides security guarantees across the entire application with minimal code. These patterns are critical for building trustworthy systems that protect user data and resist attacks.

---

## 7. CI/CD Pipeline Overview

### 🚀 Continuous Integration / Continuous Deployment

**Continuous Integration (CI)** is the practice of automatically testing and validating code changes as they are committed, ensuring that new code doesn't break existing functionality. **Continuous Deployment (CD)** extends this by automatically deploying tested code to production environments. Together, CI/CD creates a rapid, reliable, and repeatable software delivery pipeline.

### 🔧 Why CI/CD for This Project?

This Python decorators project benefits from CI/CD practices even in an educational context:

- **🧪 Automated Testing**: Every decorator implementation should pass unit tests verifying correct behavior (logging works, connections close, transactions rollback on errors, retries respect limits, cache returns correct results)
- **✅ Code Quality Enforcement**: Automated linting with `pycodestyle` or `black` ensures all decorator code follows PEP 8 style guidelines, maintaining readability and consistency across the codebase
- **📊 Integration Testing**: CI pipelines can spin up temporary SQLite databases, run decorator-enhanced functions against real data, and verify end-to-end behavior without manual setup
- **🔄 Regression Prevention**: Automated tests catch bugs introduced when refactoring decorators—for example, ensuring `functools.wraps` is still applied after performance optimizations
- **📚 Learning Industry Practices**: Students experience professional development workflows, learning to write testable code, interpret CI feedback, and iterate based on automated checks

### 🛠️ Tools and Workflow

| Tool/Service | Purpose |
|-------------|---------|
| **GitHub Actions** | Cloud-based CI/CD platform that runs workflows on every push and pull request. Automatically provisions Python environments, installs dependencies, and executes test suites without requiring local setup. |
| **Python unittest / pytest** | Testing frameworks for writing and running decorator tests. Tests verify decorator behavior in isolation (unit tests) and when composed with database operations (integration tests). |
| **SQLite3** | Lightweight database that can be created in-memory (`:memory:`) or in temporary files for CI testing, providing fast, disposable databases for each test run without requiring database server setup. |
| **pycodestyle / black** | Automated code formatters and linters that enforce PEP 8 style guidelines. CI pipeline fails if code doesn't meet style standards, ensuring consistent code quality without manual review effort. |
| **Coverage.py** | Measures test coverage—percentage of code lines executed during tests. CI can enforce minimum coverage thresholds (e.g., 80%) to ensure decorators are thoroughly tested. |
| **Docker** | Optional containerization for creating reproducible test environments. Ensures CI tests run in the same Python version and with the same dependencies as production, eliminating "works on my machine" issues. |

### 📋 Typical CI Pipeline Stages

1. **Trigger Event**: Developer pushes code to feature branch or opens pull request for peer review
2. **Environment Provisioning**: CI system spins up Python 3.8+ environment, installs project dependencies from `requirements.txt`
3. **Linting & Formatting**: Runs `pycodestyle` or `black --check` to verify code style compliance
4. **Unit Tests**: Executes decorator unit tests in isolation, mocking database operations to verify decorator logic without I/O
5. **Integration Tests**: Creates temporary SQLite database, runs decorator-enhanced functions, verifies correct query execution, connection handling, and transaction behavior
6. **Coverage Report**: Generates test coverage metrics, fails build if coverage drops below threshold (e.g., 80%)
7. **Security Scanning**: Optional static analysis tools (Bandit, Safety) check for known security vulnerabilities, insecure function calls, or outdated dependencies
8. **Build Artifacts**: If project includes a package, builds wheel/sdist distributions for deployment
9. **Status Reporting**: CI system posts pass/fail status to pull request, allowing code reviews only for passing builds
10. **Automated Deployment**: On successful merge to main branch, CD pipeline can deploy decorators to shared package repository (PyPI, private artifact store) for reuse across projects

### 🎯 Benefits

- ✅ **Instant Feedback**: Developers know within minutes if their decorator changes break existing functionality, rather than discovering bugs days later in production
- 🚀 **Faster Iteration**: Automated tests run in parallel across multiple Python versions (3.8, 3.9, 3.10, 3.11), catching compatibility issues early
- 📈 **Quality Gates**: Pull requests cannot merge until all tests pass and code meets style standards, maintaining high code quality without manual enforcement
- 🔄 **Confidence in Refactoring**: Comprehensive test suites allow fearless refactoring—decorators can be optimized or rewritten with confidence that tests will catch any behavioral changes
- 📚 **Living Documentation**: CI-tested examples serve as documentation—if the examples pass tests, they demonstrate correct decorator usage patterns
- 🌍 **Collaboration**: Multiple developers can work on decorators simultaneously, with CI preventing merge conflicts and behavioral conflicts

### 💡 Example CI Configuration (GitHub Actions)

```yaml
name: Python Decorators CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest coverage pycodestyle
    
    - name: Lint with pycodestyle
      run: pycodestyle *.py
    
    - name: Run tests with coverage
      run: |
        coverage run -m pytest tests/
        coverage report --fail-under=80
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

---

## 8. Resources

### 📚 Official Documentation

- [Python Decorators (PEP 318)](https://www.python.org/dev/peps/pep-0318/) - Official decorator syntax specification
- [functools Module](https://docs.python.org/3/library/functools.html) - Documentation for `functools.wraps` and other decorator utilities
- [SQLite3 Module](https://docs.python.org/3/library/sqlite3.html) - Python's built-in SQLite interface and DB-API 2.0
- [Python DB-API 2.0 (PEP 249)](https://www.python.org/dev/peps/pep-0249/) - Database interface specification
- [Logging Module](https://docs.python.org/3/library/logging.html) - Python's flexible logging framework

### 🎓 Learning Resources

- [Real Python - Primer on Python Decorators](https://realpython.com/primer-on-python-decorators/) - Comprehensive decorator tutorial with examples
- [Real Python - Database Management](https://realpython.com/python-sql-libraries/) - Guide to database libraries and patterns
- [PEP 8 - Style Guide](https://www.python.org/dev/peps/pep-0008/) - Python code style conventions
- [Decorator Pattern (Gang of Four)](https://refactoring.guru/design-patterns/decorator) - Classic design pattern explanation
- [SQLite Tutorial](https://www.sqlitetutorial.net/) - Comprehensive SQLite SQL syntax guide

### 🛠️ Related Libraries & Frameworks

- [SQLAlchemy](https://www.sqlalchemy.org/) - Production-grade ORM with built-in connection pooling, transaction management, and retry logic
- [Django ORM](https://docs.djangoproject.com/en/stable/topics/db/) - High-level ORM with automatic transaction handling and query optimization
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - Flask integration for SQLAlchemy with decorator-based query patterns
- [tenacity](https://tenacity.readthedocs.io/) - Production-ready retry library with advanced backoff strategies and predicates
- [cachetools](https://cachetools.readthedocs.io/) - Advanced caching utilities including LRU, TTL, and size-limited caches
- [contextlib](https://docs.python.org/3/library/contextlib.html) - Context manager utilities for resource management (alternative to decorators)

### 📖 Additional Resources

- [ALX Software Engineering Program](https://www.alxafrica.com/) - Professional software engineering training
- [Python Metaclasses & Decorators Deep Dive](https://www.youtube.com/watch?v=7lmCu8wz8ro) - Advanced metaprogramming concepts
- [Database Transaction Isolation Levels](https://en.wikipedia.org/wiki/Isolation_(database_systems)) - Understanding ACID properties
- [Exponential Backoff & Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) - Retry strategy best practices

### 🎯 Project Files Structure

```
python-decorators-0x01/
├── README.md                    # This comprehensive documentation
├── 0-log_queries.py             # Task 0: Query logging decorator
├── 1-with_db_connection.py      # Task 1: Connection management decorator
├── 2-transactional.py           # Task 2: Transaction decorator with commit/rollback
├── 3-retry_on_failure.py        # Task 3: Retry decorator with configurable attempts
├── 4-cache_query.py             # Task 4: Query result caching decorator
└── users.db                     # SQLite database file for testing (generated)
```

---

## 9. License

This project is licensed under the **MIT License** - see the [LICENSE](../LICENSE) file in the repository root for complete details.

### 📄 Quick License Summary

```
MIT License

Copyright (c) 2024 Phinehas Macharia

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
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

### ✅ What This Means

- ✔️ **Free to Use**: Use this code in personal or commercial projects
- ✔️ **Modify Freely**: Adapt decorators for your specific use cases
- ✔️ **Share & Distribute**: Include in your projects or share with others
- ✔️ **No Warranty**: Provided as-is for educational purposes
- ❗ **Attribution Required**: Include copyright notice when redistributing

---

## 10. Created By

<div align="center">

### 👨‍💻 **Phinehas Macharia**

[![GitHub](https://img.shields.io/badge/GitHub-MachariaP-181717?style=for-the-badge&logo=github)](https://github.com/MachariaP)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/phinehas-macharia)
[![Twitter](https://img.shields.io/badge/Twitter-Follow-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/phinehas_macharia)

**Backend Python Developer | Database Systems Specialist | ALX Software Engineering Scholar**

*Building elegant, production-ready solutions through clean code, thoughtful design patterns, and comprehensive testing*

---

### 🎓 About This Project

This project is part of the **ALX Software Engineering Program**, a rigorous professional training program focused on full-stack software engineering, system design, and industry best practices. The curriculum emphasizes hands-on learning, peer collaboration, and real-world problem-solving.

### 🌟 Learning Journey

**Topics Covered:**
- ✅ Python Decorators & Metaprogramming
- ✅ Database Operations & SQL
- ✅ Transaction Management & ACID Properties
- ✅ Error Handling & Resilience Patterns
- ✅ Performance Optimization & Caching
- ✅ Production Patterns & Best Practices

### 📞 Get in Touch

💬 Questions about decorators, Python, or backend development?  
📧 Feel free to reach out via [GitHub Issues](https://github.com/MachariaP/alx-backend-python/issues) or connect on LinkedIn!

---

<sub>⭐ **If you found this project helpful, please consider giving it a star!** ⭐</sub>

<sub>📚 **Check out other ALX Backend Python projects**: [python-generators-0x00](../python-generators-0x00) | [python-async-function](../0x01-python_async_function) | [unittests-integration-tests](../0x03-Unittests_and_integration_tests)</sub>

<sub>🔄 **Last Updated**: November 2024</sub>

</div>

---

<div align="center">

### 🚀 Ready to Master Decorators?

**Start with Task 0** and work through each progressive challenge to build your decorator expertise!

```bash
# Clone the repository
git clone https://github.com/MachariaP/alx-backend-python.git

# Navigate to the decorators project
cd alx-backend-python/python-decorators-0x01

# Create your test database
python3 -c "import sqlite3; conn = sqlite3.connect('users.db'); conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)'); conn.commit()"

# Run your first decorator
python3 0-log_queries.py
```

**Happy Coding!** 🐍✨

</div>
