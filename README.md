# SkillProof — Virtual Lab & Skill Intelligence Platform

> A production-grade coding lab + hiring signal system that evaluates, tracks, and **proves** user skills through sandbox-based execution.

---

## Table of Contents

1. [What Is SkillProof?](#what-is-skillproof)
2. [Core Philosophy](#core-philosophy)
3. [Tech Stack](#tech-stack)
4. [Folder Structure](#folder-structure)
5. [Domain Architecture](#domain-architecture)
6. [How It Works — End-to-End Flow](#how-it-works)
7. [Execution Pipeline](#execution-pipeline)
8. [Skill Intelligence Engine](#skill-intelligence-engine)
9. [Skill Proof & Attestation](#skill-proof--attestation)
10. [Trust & Integrity System](#trust--integrity-system)
11. [Admin System](#admin-system)
12. [Security Layer](#security-layer)
13. [Event-Driven Architecture](#event-driven-architecture)
14. [Infrastructure](#infrastructure)
15. [Observability](#observability)
16. [Scaling Strategy](#scaling-strategy)
17. [API Reference Summary](#api-reference-summary)
18. [Environment Setup](#environment-setup)

---

## What Is SkillProof?

SkillProof is NOT a coding platform. It is a **Skill Intelligence System** — a platform that lets users solve real engineering problems inside sandboxed virtual labs and receive verifiable, multi-dimensional proof of their abilities.

### Core Value Proposition

| For Users | For Employers |
|-----------|---------------|
| Prove skills with working code, not quizzes | Verifiable execution-backed skill records |
| Track skill progression over time | Trust scores based on consistency, not one test |
| Weakness detection and guided improvement | Multi-dimensional scores: correctness, efficiency, quality |
| Earn hiring-ready skill attestations | Anti-cheat integrity layer |

---

## Core Philosophy

The system is built on five principles:

**1. Execution over declaration** — Skills are proven by running code, not answering MCQs.

**2. Multi-dimensional scoring** — A single pass/fail score is not intelligence. Every submission is scored across correctness, efficiency, code quality, and historical consistency.

**3. Verifiable trust** — Skill proofs are backed by a full audit trail of executions, not a self-reported claim.

**4. Loose coupling via events** — Domains never call each other directly. All cross-domain communication happens through an event bus.

**5. Microservice-ready from day one** — The modular monolith is designed so every bounded context can be extracted as an independent service without redesign.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python / fast api (modular monolith) |
| Architecture | Domain Driven Design (DDD) |
| Database | PostgreSQL (via SQLAlchemy) |
| Cache | Redis |
| Queue | Redis Queues / RabbitMQ-compatible |
| Sandbox | Docker-based isolation |
| Execution adapter | Judge0 (optional) or custom runner |
| Object storage | AWS S3 (logs, artifacts, audit trail) |
| Workers | Celery / RQ |
| Observability | Structured logging + Prometheus + OpenTelemetry |

---

## Folder Structure

```
src/
│
├── api/                                  # Interface Layer
│   ├── routers/
│   │   ├── lab_routes.py                 # GET /labs, GET /labs/:id
│   │   ├── session_routes.py             # POST /sessions, PATCH /sessions/:id
│   │   ├── submission_routes.py          # POST /submissions
│   │   ├── skill_routes.py              # GET /skills/:user_id/profile
│   │   └── admin_routes.py              # Admin-only endpoints
│   │
│   ├── controllers/
│   │   ├── lab_controller.py
│   │   ├── session_controller.py
│   │   ├── submission_controller.py
│   │   └── skill_controller.py
│   │
│   ├── services/                         # Application Layer (Use-cases)
│   │   ├── lab_service.py
│   │   ├── session_service.py
│   │   ├── submission_service.py
│   │   └── skill_service.py
│   │
│   ├── middleware/
│   │   ├── auth.py                       # JWT validation
│   │   ├── rate_limit.py                 # Per-user rate limiting
│   │   └── request_context.py            # Request ID, user identity
│   │
│   └── websocket.py                      # Live execution feedback to client
│
│
├── domain/                               # Core Business Logic (Pure Python)
│   │
│   ├── lab/
│   │   ├── lab.py                        # Lab aggregate root
│   │   ├── lab_rules.py                  # Business invariants
│   │   ├── lab_events.py                 # LabPublishedEvent, LabArchivedEvent
│   │   └── value_objects.py             # Difficulty, Tag, LabVersion
│   │
│   ├── session/
│   │   ├── session.py                    # Session aggregate
│   │   ├── session_state_machine.py      # STARTED → RUNNING → COMPLETED / ABANDONED
│   │   └── session_events.py            # SessionStartedEvent, SessionCompletedEvent
│   │
│   ├── submission/
│   │   ├── submission.py                 # Submission aggregate
│   │   └── submission_events.py         # SubmissionCreatedEvent
│   │
│   ├── evaluation/
│   │   ├── evaluation.py                 # Evaluation result aggregate
│   │   └── evaluation_rules.py           # Scoring rules, partial credit logic
│   │
│   ├── skill/
│   │   ├── skill_profile.py             # Skill profile aggregate root
│   │   ├── skill_graph.py               # Tech stack hierarchy and relationships
│   │   ├── skill_rules.py               # Scoring thresholds, attestation criteria
│   │   └── value_objects.py             # SkillScore, SkillDimension, TrustScore
│   │
│   └── shared/
│       ├── base_entity.py               # Entity base (id, created_at, updated_at)
│       ├── aggregate_root.py            # Aggregate base + domain event collection
│       └── domain_exceptions.py         # LabNotFound, SessionExpired, etc.
│
│
├── application/                          # Use-case Orchestration
│   ├── commands/
│   │   ├── start_session.py             # StartSessionCommand + handler
│   │   ├── submit_solution.py           # SubmitSolutionCommand + handler
│   │   └── update_skill.py             # UpdateSkillCommand + handler
│   │
│   ├── queries/
│   │   ├── get_lab.py                   # GetLabQuery
│   │   ├── get_session.py              # GetSessionQuery
│   │   └── get_skill_profile.py        # GetSkillProfileQuery
│   │
│   ├── handlers/
│   │   ├── command_handlers.py          # Command → Domain → Event dispatch
│   │   └── query_handlers.py            # Query → Repository → DTO
│   │
│   └── dto/
│       ├── request_dto.py              # Validated inbound payloads
│       └── response_dto.py             # Serialized outbound responses
│
│
├── lab_engine/                           # Lab Generation & Template System (USP)
│   ├── template/
│   │   ├── registry.py                  # Template catalogue lookup
│   │   ├── base_template.py            # Base class for all lab templates
│   │   ├── codebase_builder.py         # Assembles runnable codebase from template
│   │   ├── slots/                       # Pluggable problem slots (function stubs, etc.)
│   │   └── injectors/                  # Context injectors (company data, domain flavour)
│   │
│   ├── config/
│   │   ├── schema.py                    # Lab config schema (validated on publish)
│   │   ├── difficulty_profiles.py      # Easy / Medium / Hard / Expert calibration
│   │   ├── tech_stack_profiles.py      # Per-language execution configs
│   │   └── variation_rules.py          # Rules for generating lab variants
│   │
│   ├── generator/
│   │   ├── pipeline.py                  # Generation pipeline orchestrator
│   │   ├── pre_generator.py            # Pre-generate labs at off-peak (avoids cold start)
│   │   └── stages/
│   │       ├── mutation.py             # Vary problem parameters per user
│   │       ├── context.py              # Inject narrative/domain context
│   │       ├── tests.py                # Generate test cases from spec
│   │       └── assembly.py            # Final codebase assembly
│   │
│   ├── mode/
│   │   ├── learn.py                    # Guided mode with hints enabled
│   │   ├── build.py                    # Project-style open-ended lab
│   │   ├── work.py                     # Timed, hiring-signal mode
│   │   └── hints.py                    # Hint reveal system (affects score)
│   │
│   ├── session/
│   │   ├── manager.py                  # Active session tracking
│   │   └── snapshot.py                 # Session state snapshot (resumability)
│   │
│   └── metadata/
│       ├── lab_catalog.py              # Searchable lab index
│       └── tagging.py                  # Skill tag taxonomy mapper
│
│
├── skill_engine/                         # Skill Intelligence Core
│   ├── evaluation/
│   │   ├── orchestrator.py             # Coordinates all evaluation sub-scorers
│   │   ├── correctness.py              # Test case pass rate scoring
│   │   ├── efficiency.py               # Runtime and memory benchmarking
│   │   ├── quality.py                  # Code quality via AST analysis
│   │   └── composite.py               # Weighted composite score assembly
│   │
│   ├── scoring/
│   │   ├── calculator.py               # Core score computation
│   │   ├── weights.py                  # Configurable dimension weights per lab type
│   │   └── penalties.py               # Deductions (too many attempts, flagged, etc.)
│   │
│   ├── tracking/
│   │   ├── updater.py                  # Updates skill profile after evaluation
│   │   ├── skill_matrix.py            # Multi-tech skill tracking matrix
│   │   ├── weakness.py                 # Detects skill gaps and failure patterns
│   │   └── progression.py             # Trend analysis over time
│   │
│   ├── skill_graph/
│   │   ├── taxonomy.py                 # Skill taxonomy definition (e.g. Python > FastAPI)
│   │   ├── dependency_graph.py         # Skill prerequisites and relationships
│   │   └── mapping.py                  # Lab tag → skill graph node mapping
│   │
│   ├── trust/
│   │   ├── plagiarism.py               # Code similarity detection
│   │   └── anomaly.py                  # Timing and behavioural anomaly detection
│   │
│   └── profile/
│       ├── model.py                    # Skill profile read model
│       └── history.py                  # Historical performance store
│
│
├── execution/                            # Sandbox Execution
│   ├── orchestrator.py                  # Job lifecycle: queue → run → result
│   ├── runner.py                         # Container spawning and output capture
│   │
│   └── adapters/
│       └── judge0.py                    # Judge0 API adapter (drop-in alternative)
│
│
├── security/                             # Security Layer (Mandatory)
│   ├── code_safety/
│   │   ├── static_analyzer.py           # Pre-execution static analysis
│   │   ├── ast_checker.py               # AST traversal for dangerous patterns
│   │   └── blacklist_rules.py           # Blocked calls (os.system, eval, socket, etc.)
│   │
│   ├── execution_guard/
│   │   ├── timeout.py                   # Wall-clock timeout enforcement
│   │   ├── resource_limit.py            # CPU + memory quota enforcement
│   │   └── sandbox_policy.py            # Container isolation policy (no network, no fs)
│   │
│   └── validation/
│       ├── input_validator.py           # Request payload validation
│       └── rate_limiter.py             # Per-user submission rate limiting
│
│
├── workers/                              # Async Workers
│   ├── consumers/
│   │   ├── submission_consumer.py       # Dequeues submissions for execution
│   │   └── evaluation_pipeline.py       # Runs evaluation after execution completes
│   │
│   ├── handlers/
│   │   ├── execution_handler.py         # Handles ExecutionCompletedEvent
│   │   ├── evaluation_handler.py        # Handles SubmissionEvaluatedEvent
│   │   └── skill_handler.py            # Handles SkillUpdatedEvent
│   │
│   └── retry/
│       ├── retry_policy.py              # Exponential backoff config
│       └── dlq.py                       # Dead-letter queue for failed jobs
│
│
├── infrastructure/                       # External Systems
│   ├── db/
│   │   ├── models/                      # SQLAlchemy ORM models
│   │   ├── repositories/               # Repository pattern per domain aggregate
│   │   └── migrations/                 # Alembic migration files
│   │
│   ├── cache/
│   │   ├── redis.py                     # Redis connection and base operations
│   │   └── keys.py                      # Centralised cache key definitions
│   │
│   ├── queue/
│   │   └── redis_queue.py              # Job enqueue / dequeue abstraction
│   │
│   └── storage/
│       └── s3.py                        # S3 client for logs, artifacts, audit trail
│
│
├── admin/                                # Admin Bounded Context
│   ├── lab_management/
│   │   ├── builder.py                   # Lab creation wizard
│   │   ├── editor.py                    # Edit existing lab content
│   │   ├── versioning.py               # Lab versioning and diff
│   │   └── publisher.py               # Publish / unpublish workflow
│   │
│   ├── template_management/
│   │   ├── creator.py                   # Template authoring
│   │   ├── versioning.py               # Template version control
│   │   └── validator.py               # Template schema validation
│   │
│   ├── config_management/
│   │   ├── builder.py                   # Build scoring config for a lab
│   │   ├── validator.py               # Validate config against schema
│   │   └── profiles.py                # Manage difficulty profiles
│   │
│   └── skill_mapping/
│       ├── mapper.py                    # Map lab tags to skill graph nodes
│       └── weights.py                  # Configure scoring dimension weights per lab
│
│
├── shared/
│   ├── constants.py                     # App-wide constants
│   ├── exceptions.py                    # Shared exception types
│   └── utils.py                         # Common utilities
│
│
└── main.py                               # fast api app factory + blueprint registration
```

---

## Domain Architecture

The system is divided into **9 bounded contexts**, each a self-contained module that can be extracted as a microservice independently.

### 1. Lab Domain
Owns the definition, content, metadata, and versioning of labs. A `Lab` aggregate holds the problem statement, starter code, constraints, difficulty, tags, and version history. Lab rules enforce invariants (e.g. a lab cannot be published without at least one hidden test case).

### 2. Session Domain
Manages the lifecycle of a user's engagement with a lab. A session is a state machine: `STARTED → RUNNING → COMPLETED` or `ABANDONED`. Sessions are snapshot-based for resumability — a user can close the browser and return to exactly where they left off.

### 3. Submission Domain
Captures a user's code submission against an active session. The submission aggregate holds code, language, timestamp, and session reference. Static code analysis runs synchronously before the submission is accepted. Once accepted, a job is enqueued.

### 4. Execution Domain
The sandbox layer. An orchestrator picks jobs from the queue, provisions an isolated container with strict resource controls (CPU quota, memory limit, wall-clock timeout), runs the code, and captures all output. The adapter pattern allows Judge0 to be used as a drop-in replacement for the custom runner.

### 5. Evaluation Domain
Runs the submitted code's output against public and hidden test cases. Calculates partial scores for partially correct solutions. Captures performance benchmarks (runtime percentile, memory usage). Feeds scores to the scoring engine.

### 6. Skill Intelligence Domain
The core IP of the platform. The skill graph maps tech stack relationships (e.g. Python → FastAPI → async patterns). The scoring engine calculates a multi-dimensional score: correctness, efficiency, code quality, and historical consistency. The weakness detector identifies where a user consistently fails. The progression tracker shows skill trends over time.

### 7. Skill Proof / Attestation Domain
Once a user's skill score crosses a defined threshold with sufficient consistency, a verifiable skill attestation is issued. The attestation includes a trust score based on submission history, timestamps, and anti-cheat signals. These records are designed to be shared with hiring systems.

### 8. Trust & Integrity Domain
Plagiarism detection compares code submissions for structural similarity. Anomaly detection flags suspicious patterns (e.g. near-instant solutions, copy-paste timing). Execution behaviour analysis adds a second signal layer. Flagged sessions are queued for admin review.

### 9. Admin Domain
A separate bounded context for lab authors and platform administrators. Includes a lab builder, versioning system, publishing workflow, template management, scoring weight configuration, and skill tag mapping.

---

## How It Works

The complete user journey from lab selection to skill proof:

```
1. User selects a lab
   └── GET /labs/:id → Lab domain loads content, metadata, starter code

2. Session starts
   └── POST /sessions → Session aggregate created, state = STARTED
   └── SessionStartedEvent fired → Lab content loaded into session snapshot

3. User writes and submits code
   └── POST /submissions → Static analysis runs (AST check, blacklist scan)
   └── Passes → Submission aggregate created, job enqueued to Redis
   └── SubmissionCreatedEvent fired → Session transitions to RUNNING

4. Execution
   └── Worker dequeues job → Orchestrator provisions sandbox container
   └── Code runs with resource limits → stdout, stderr, exit code captured
   └── ExecutionCompletedEvent fired

5. Evaluation
   └── Output compared against test cases (public + hidden)
   └── Correctness, efficiency, code quality scored independently
   └── Composite score assembled → SubmissionEvaluatedEvent fired

6. Skill update
   └── Skill profile aggregate updated with new scores
   └── Skill graph traversed to propagate scores to related skills
   └── Weakness detector runs → Progression tracker updated
   └── Trust module checks for anomalies → SkillUpdatedEvent fired

7. Attestation check
   └── Attestation domain checks if threshold crossed
   └── If yes → SkillAttestedEvent fired → Verifiable proof record created

8. Result delivered
   └── WebSocket pushes live result to user's browser
   └── Full score breakdown shown: correctness, efficiency, quality, trend
```

---

## Execution Pipeline

Every submission flows through 5 sequential async stages:

### Stage 1 — Pre-check (synchronous, blocks queue write)
- Input validation (size, encoding, language support)
- AST-based static analysis
- Blacklist rule enforcement (blocked system calls, network access, file I/O)
- Fails fast: rejected submissions never enter the queue

### Stage 2 — Execution (async, sandboxed)
- Worker dequeues job
- Orchestrator provisions Docker container
- Resource envelope applied: CPU quota, memory limit, wall-clock timeout
- No network access, no filesystem writes outside sandbox
- stdout, stderr, exit code, and resource metrics captured

### Stage 3 — Evaluation (async)
- Output matched against public test cases (visible to user)
- Output matched against hidden test cases (score-only, not revealed)
- Partial credit computed (e.g. 7/10 test cases passing = 70% correctness)
- Runtime benchmarked against reference implementations
- Memory usage recorded

### Stage 4 — Scoring (async)
- Composite score assembled from weighted dimensions:
  - **Correctness** (default weight: 50%) — test case pass rate
  - **Efficiency** (default weight: 25%) — runtime and memory vs benchmark
  - **Code quality** (default weight: 15%) — AST complexity, readability signals
  - **Consistency** (default weight: 10%) — historical performance on similar problems
- Penalties applied (excessive retries, flagged behaviour)
- Score written to PostgreSQL via repository

### Stage 5 — Persistence (async)
- Evaluation result persisted to database
- Skill profile updated
- Execution logs and artifacts shipped to S3
- Redis cache invalidated where needed
- WebSocket pushes result to user

---

## Skill Intelligence Engine

The `skill_engine/` module is the core IP of the platform.

### Skill Graph
The skill graph is a directed graph of tech skills and their relationships. A node represents a skill (e.g. `Python`, `async/await`, `FastAPI`, `PostgreSQL`). Edges represent dependencies and relationships (e.g. `FastAPI` depends on `Python`, `async/await`).

When a user scores well on a FastAPI lab, their Python score is also partially updated (graph propagation). When they score poorly on async patterns, the weakness detector surfaces this specifically, not just "Python is weak."

### Multi-Dimensional Scoring

| Dimension | What It Measures | Source |
|-----------|-----------------|--------|
| Correctness | Does the code produce right output? | Test case results |
| Efficiency | How fast and memory-efficient is it? | Execution metrics vs benchmark |
| Code quality | Is the code readable and well-structured? | AST analysis |
| Consistency | Is performance stable over time? | Historical submission data |

### Weakness Detection
The `weakness.py` module analyses patterns across multiple submissions to identify where a user consistently underperforms. This produces actionable signals: "You struggle with time complexity in tree problems" rather than "Your score is 62%."

### Progression Tracking
`progression.py` tracks skill scores over time per skill node. The trend (improving / plateauing / declining) is shown in the user's profile and used as a signal in the consistency dimension of the composite score.

---

## Skill Proof & Attestation

A skill attestation is issued when:

1. The user's skill score in a domain crosses the configured threshold
2. The score is based on at least the minimum required number of submissions
3. The Trust & Integrity module has not flagged the user's sessions

Each attestation record contains:
- Skill domain and sub-skills covered
- Composite score and dimension breakdown
- Trust score (based on consistency and anomaly signals)
- Timestamp and submission count
- Audit trail reference (S3 link to execution logs)

Attestations are designed to be shared with hiring systems via API or exported as a verifiable document.

---

## Trust & Integrity System

### Plagiarism Detection
`skill_engine/trust/plagiarism.py` computes structural similarity between code submissions. It uses AST normalisation before comparison, so simple variable renaming does not evade detection.

### Anomaly Detection
`skill_engine/trust/anomaly.py` flags:
- Solutions submitted in implausibly short time
- Copy-paste timing patterns (large code blocks appearing instantly)
- Repeated identical submissions with minor cosmetic changes
- Significant deviation from a user's historical performance baseline

### Flagging Workflow
Flagged sessions emit an `AnomalyDetectedEvent`. The Admin domain receives this and queues the session for human review. Flagged submissions are excluded from skill score calculations until reviewed.

---

## Admin System

The Admin bounded context is a separate module with its own routes, controllers, and persistence logic. It is not exposed to end users.

### Lab Management
- **Builder** — Step-by-step lab creation with content, test cases, and config
- **Editor** — Edit existing lab content without republishing (drafts)
- **Versioning** — Full version history with diff view; rollback supported
- **Publisher** — Publish / unpublish workflow with pre-publish validation

### Template Management
- **Creator** — Author reusable lab templates with configurable slots
- **Versioning** — Template version control independent of lab versions
- **Validator** — Schema validation before template can be used in lab generation

### Config Management
- **Scoring weights** — Configure dimension weights per lab (override platform defaults)
- **Difficulty profiles** — Define what Easy / Medium / Hard means in terms of test case strictness and scoring thresholds
- **Tech stack profiles** — Language-specific execution configs (compiler flags, time limits)

### Skill Mapping
- **Mapper** — Map lab tags to skill graph nodes
- **Weights** — Configure how strongly a lab affects each skill node it maps to

---

## Security Layer

Security is a mandatory cross-cutting concern, not an afterthought.

### Static Code Analysis (pre-execution)
Every submission is scanned before the job is enqueued:
- **AST checker** — Traverses the parsed AST to detect dangerous constructs
- **Blacklist rules** — Blocked calls include `os.system`, `subprocess`, `eval`, `exec`, `socket`, `open` (outside sandbox), `importlib`
- **Input validator** — Size limits, encoding checks, language whitelist

### Sandbox Policies (at execution)
- No outbound network access
- No filesystem writes outside `/sandbox/tmp`
- CPU quota enforced at container level
- Memory hard limit (OOM kill on breach)
- Wall-clock timeout (independent of CPU time)

### API Security
- JWT authentication on all user-facing routes
- Rate limiting per user per endpoint (configurable per route)
- Request context propagation for audit logging

---

## Event-Driven Architecture

Domains communicate exclusively through domain events. No domain imports or calls another domain directly.

| Event | Emitted By | Handled By |
|-------|-----------|-----------|
| `SessionStartedEvent` | Session | Lab (load content), Execution (warm runner) |
| `SubmissionCreatedEvent` | Submission | Execution (enqueue job) |
| `ExecutionCompletedEvent` | Execution | Evaluation (run test cases) |
| `SubmissionEvaluatedEvent` | Evaluation | Skill Intelligence, Trust & Integrity |
| `SkillUpdatedEvent` | Skill Intelligence | Attestation (check threshold) |
| `SkillAttestedEvent` | Attestation | Notifications, Hiring API webhook |
| `AnomalyDetectedEvent` | Trust & Integrity | Admin (review queue), Session (flag) |
| `LabPublishedEvent` | Admin | Lab domain (update catalogue), Cache (invalidate) |

The event bus is implemented via Redis pub/sub at the infrastructure layer (`infrastructure/queue/redis_queue.py`). Handlers in `workers/handlers/` consume these events asynchronously.

---

## Infrastructure

### PostgreSQL
- All domain aggregates have corresponding ORM models in `infrastructure/db/models/`
- Repository pattern: each aggregate has a dedicated repository class
- Read/write separation is prepared for via the repository interface
- Migrations managed with Alembic

### Redis
- Session state cache (TTL-based)
- Job queue for submission → execution handoff
- Evaluation result cache (short TTL, invalidated on skill update)
- Rate limiter counters (sliding window)

### Object Storage (S3)
- Execution logs (stdout, stderr) per submission
- Code artifact storage for audit trail
- Skill proof audit references
- Lab content files (large starter codebases)

### Worker System
- Celery or RQ workers consuming from Redis queues
- One consumer per queue type (submission, evaluation, skill update)
- Exponential backoff retry policy via `workers/retry/retry_policy.py`
- Dead-letter queue (`workers/retry/dlq.py`) for jobs that exhaust retries
- Admin notification on DLQ entries

---

## Observability

### Logging
- Structured JSON logging throughout
- Request ID propagated from HTTP request through to execution result
- Every domain event logged with correlation ID

### Metrics
- Submission volume (per language, per lab, per time window)
- Execution success / timeout / error rates
- Evaluation score distributions
- Queue depth and worker throughput
- Cache hit rates

### Tracing
- OpenTelemetry trace IDs from HTTP request → queue → execution → evaluation → persistence
- Full trace visible per submission for debugging latency

### Feature Flags
- Feature flag hooks in the codebase (compatible with LaunchDarkly or custom implementation)
- Used for gradual rollout of new lab types, scoring model changes, and new language support

---

## Scaling Strategy

### Phase 1 — Modular Monolith (0 → 10K users)
All bounded contexts run as modules within a single fast api application. Redis handles queuing and caching. PostgreSQL handles all persistence. Horizontal scaling via multiple fast api processes behind a load balancer.

### Phase 2 — Extract Execution (10K → 100K users)
The `execution/` module is the first to be extracted. Execution is stateless and CPU-intensive — it scales independently of the API. Worker pool scales horizontally with queue depth.

### Phase 3 — Extract Skill Engine (100K → 500K users)
`skill_engine/` is extracted as a separate service. Skill calculations are compute-intensive and asynchronous — they do not need to block the submission path.

### Phase 4 — Full Decomposition (500K → 1M+ users)
Each bounded context becomes an independent service. Inter-service communication via the event bus (RabbitMQ or Kafka at this scale). Read models (CQRS) introduced for the skill profile and lab catalogue to handle query load.

---

## API Reference Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/labs` | List available labs with filters |
| GET | `/labs/:id` | Get lab detail, starter code, metadata |
| POST | `/sessions` | Start a new lab session |
| PATCH | `/sessions/:id` | Update session state |
| POST | `/submissions` | Submit code for a session |
| GET | `/submissions/:id` | Get submission result |
| GET | `/skills/:user_id/profile` | Get user skill profile |
| GET | `/skills/:user_id/attestations` | Get user skill attestations |
| POST | `/admin/labs` | Create a new lab (admin) |
| PUT | `/admin/labs/:id/publish` | Publish a lab (admin) |

---

## Environment Setup

```bash
# Clone and set up
git clone https://github.com/your-org/skillproof
cd skillproof
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Set: DATABASE_URL, REDIS_URL, AWS_BUCKET, SECRET_KEY

# Run migrations
fast api db upgrade

# Start workers (separate terminal)
celery -A src.workers worker --loglevel=info

# Start API
fast api --app src.main run --port 5000
```

### Docker (recommended for local development)
```bash
docker-compose up --build
```

The `docker-compose.yml` spins up fast api, PostgreSQL, Redis, and a Celery worker together.

---

*SkillProof — Built for engineers who prove, not just claim.*
