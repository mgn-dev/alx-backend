# ALX Backend Specialization

Backend engineering tasks covering API pagination, in-memory caching strategies, Flask internationalization, and a Redis-backed job queuing system in JavaScript.

## Overview

This project includes four backend tasks that address common production concerns: slicing large datasets for clients, reducing database load with cache eviction policies, serving localized content, and decoupling work with message queues. Tasks combine Python (Flask, typing) and JavaScript (Node.js, Redis clients) with emphasis on algorithmic correctness and interface design.

Each task builds on patterns used in real APIs—hypermedia pagination metadata, pluggable cache backends, Babel locale negotiation, and pub/sub job processing.

## Skills covered


- Build offset/limit pagination with index range calculations
- Return hypermedia pagination metadata (`page_size`, `total_pages`, `next_page`, etc.)
- Design cache interfaces and concrete FIFO, LIFO, LRU, MRU, and LFU eviction policies
- Set up Flask-Babel for locale detection, translation, and timezone-aware datetime rendering
- Build a Redis-backed queuing system with publishers, subscribers, and job processors in Node.js

## Tech Stack

| Category | Technologies |
|----------|-------------|
| Languages | Python 3, JavaScript (Node.js) |
| Frameworks | Flask, Flask-Babel |
| Data | CSV datasets, Redis |
| Patterns | Strategy (caching), Pub/Sub (queuing), Hypermedia pagination |
| Tooling | `pycodestyle`, npm |

## Project Structure

| Module | Directory | Focus |
|--------|-----------|-------|
| 0x00 | `0x00-pagination` | Index ranges, simple and hypermedia pagination |
| 0x01 | `0x01-caching` | Base cache class, FIFO/LIFO/LRU/MRU/LFU implementations |
| 0x02 | `0x02-i18n` | Flask-Babel setup, locale selectors, timezone display |
| 0x03 | `0x03-queuing_system_in_js` | Redis operations, job creation, async processing |

## Key Implementations

- **Pagination (`0x00`)** — `index_range()` helper and a `Server` class that loads a CSV dataset and exposes `get_page()` with optional deletion-aware hypermedia links
- **Caching (`0x01`)** — `BaseCaching` abstract class with `MAX_ITEMS` limit; subclasses implement `put()`/`get()` for FIFO, LIFO, LRU, MRU, and LFU replacement strategies
- **Internationalization (`0x02`)** — Progressive Flask apps (`0-app.py` through `7-app.py`) adding Babel locale configuration, `gettext` translations, parameterized strings, and timezone conversion in templates
- **Queuing system (`0x03`)** — Node.js scripts for Redis client setup, atomic operations, seat reservation logic, and a publisher/subscriber job pipeline with Mocha tests

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+ and npm (module `0x03`)
- Redis Server (modules `0x01` context and `0x03`)
- Flask and Flask-Babel (`pip install flask flask-babel`)

### Setup

```bash
git clone <repository-url>
cd alx-backend
```

For the queuing module:

```bash
cd 0x03-queuing_system_in_js
npm install
```

Ensure Redis is running locally:

```bash
redis-server
```

### Running Tasks

Pagination checker scripts:

```bash
python3 0x00-pagination/1-main.py
python3 0x00-pagination/2-main.py
```

Cache implementations:

```bash
python3 0x01-caching/1-main.py   # FIFO
python3 0x01-caching/3-main.py   # LRU
```

Flask i18n apps:

```bash
python3 0x02-i18n/0-app.py
# Visit http://0.0.0.0:5000
```

Queuing system (Node.js):

```bash
node 0x03-queuing_system_in_js/5-publisher.js
node 0x03-queuing_system_in_js/6-job_processor.js
npm test  # where package.json defines Mocha tests
```

## Curriculum Context

This project sits in the ALX backend specialization project after higher-level Python and precedes storage and user-data task folders. Pagination and caching concepts directly support scalable REST API design; i18n prepares learners for globally deployed Flask services; the Redis queuing project foreshadows background workers and task brokers used in production systems. Together these modules bridge foundational Python/JS skills and the AirBnB clone API implementations.
