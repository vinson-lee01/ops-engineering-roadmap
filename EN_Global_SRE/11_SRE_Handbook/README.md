# 11 · SRE Handbook

> SRE (Site Reliability Engineering) is not a job title — it is a way of running production systems.
> This module covers the full SRE discipline: philosophy, SLI/SLO engineering, incident management,
> on-call excellence, postmortem culture, toil elimination, capacity planning, and chaos engineering.
>
> **Primary reference**: Google SRE Books (free at sre.google) + real-world patterns from Meta, Uber, Dropbox.

---

## 🎯 What Is SRE?

SRE is what happens when you ask a software engineer to design an operations team.

| Traditional Ops | SRE |
|-----------------|-----|
| "Run it however you can" | Engineering approach to reliability |
| Manual & reactive | Automated & proactive |
| Reliability blocks features | Error budget aligns both teams |
| Toil scales linearly | Toil is systematically eliminated |
| "We are always on fire" | Incidents are learning opportunities |

**The 50% rule**: Spend ≤ 50% of time on operational work (on-call, incidents, toil). The rest goes to engineering projects that reduce future operational load.

If your team is above 50% toil, you're in an **emergency mode** — stop shipping features and pay down technical debt.

---

## Part 1: SLI / SLO / SLA — The Foundation

### Know the Difference

| Term | Full Name | Definition | Example |
|------|-----------|------------|----------|
| **SLI** | Service Level Indicator | A quantifiable metric measuring service behavior | "99.9% of API requests complete in <200ms" |
| **SLO** | Service Level Objective | Target value for your SLI over a window | "99.9% availability per 28-day window" |
| **SLA** | Service Level Agreement | Contractual promise to users, with consequences | "If < 99.5% uptime, customer gets credit" |

### Designing Good SLIs — Not All Metrics Are Equal

**Bad SLIs** (common mistakes):
- ❌ "CPU utilization < 80%" — This is a proxy, not a user-facing indicator
- ❌ "Number of running pods" — Users don't care about infrastructure health directly
- ❌ "Error count" without context — Need rate or ratio

**Good SLIs** (user-centric):
- ✅ **Availability**: `% of valid requests returning successful responses`
- ✅ **Latency**: `p50`, `p95`, `p99` response time
- ✅ **Quality**: `% of correct results` (not just HTTP 200, but semantically right)
- ✅ **Throughput**: Requests/sec sustained without degradation
- ✅ **Freshness**: Data staleness for caching/proxy services

### SLO Window Selection

| Window Size | Pros | Cons | Best For |
|-------------|------|------|----------|
| **28 days (rolling)** | Smooths out weekly patterns; industry standard | Slow to detect degradation | Most services |
| **7 days** | Faster feedback | Noisy; weekend traffic skews | Fast-moving services |
| **90 days (calendar quarter)** | Aligns with business cycles | Very slow feedback; hides short-term issues | Enterprise contracts |
| **1 day** | Immediate signal | Extremely noisy | Only for alerting thresholds |

**Recommendation**: Start with **28-day rolling windows**. They smooth out weekly traffic variations while providing timely enough feedback.

### Error Budget Math

```
SLO Target    → Monthly Budget (30 days)    → Hourly Budget
─────────────────────────────────────────────────────────────
99.9%         → 43 min 12 sec downtime      → 1.79 min/hr
99.95%        → 21 min 36 sec               → 54 sec/hr
99.99%        → 4 min 19 sec                → 8.6 sec/hr
99.999%       → 26 seconds                  → 1.1 sec/hr
```

**Critical insight about error budgets**:

| Situation | Action |
|-----------|--------|
| Budget remaining 70%+ | Ship fast. Take calculated risks. |
| Budget remaining 20-50% | Proceed with caution. Require reliability review for risky changes. |
| Budget nearly exhausted (< 10%) | Feature freeze. Only bug fixes and reliability work allowed. |
| Budget consumed (0%) | Emergency. All hands on deck to improve reliability before next window resets. |

### Implementing SLOs in Practice

#### Step 1: Pick 2-4 SLIs per service

Don't try to track everything. For most services, start with:

```yaml
service: api-gateway
sli_definitions:
  - name: availability
    description: "Percentage of successful HTTP responses"
    numerator: "count(http_requests_total{status_code!=\"5xx\"})"
    denominator: "count(http_requests_total)"
  
  - name: latency_p99
    description: "99th percentile response time"
    query: "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))"
    target_ms: 200
    
  - name: latency_p50
    description: "Median response time"
    query: "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))"
    target_ms: 50
```

#### Step 2: Build the SLO Dashboard

```promql
-- Availability SLO (28-day rolling)
(
  sum(rate(http_requests_total{status!~"5.."}[28d]))
  /
  sum(rate(http_requests_total[28d]))
) * 100

-- Error budget remaining (%)
100 - (
  sum(rate(http_requests_total{status=~"5.."}[28d]))
  /
  sum(rate(http_requests_total[28d])
) * 100)

-- Days until budget exhausts (at current burn rate)
(
  (sum(rate(http_requests_total{status=~"5.."}[28d])) / sum(rate(http_requests_total[28d]))) - 0.001
)
/
(
  sum(rate(http_requests_total{status=~"5.."}[1h])) / sum(rate(http_requests_total[1h]))
) * 24
```

#### Step 3: Alert on Budget Burn Rate

Don't just alert when SLO is missed. **Alert on how fast you're burning budget**:

| Burn Rate | Alert Condition | Meaning | Response |
|-----------|---------------|---------|----------|
| **Slow (×1)** | Normal consumption | On track | No action needed |
| **Medium (×2)** | Burning 2× faster than allowed | Something degraded | Investigate within business hours |
| **Fast (×6)** | Burning 6× faster | Active incident territory | Page immediately |
| **Fast (×14)** | Will miss SLO this month if continued | Critical | Page + consider rollback |

```promql
-- Fast burn alert: consuming error budget at 6x the normal rate
(
  sum(rate(http_requests_total{status=~"5.."}[1h])) 
  / 
  sum(rate(http_requests_total[1h]))
) 
> 
(
  (0.001 / (28 * 24))  -- monthly budget as hourly rate
  * 6                    -- 6x multiplier
)
```

---

## Part 2: Incident Management

### Incident Severity Framework

| SEV | User Impact | Response Time | Escalation | Examples |
|-----|------------|--------------|------------|----------|
| **SEV-0 (Critical)** | Complete outage, revenue loss, data breach | Immediate (page now) | VP / Director | Payment processing down, PII leak |
| **SEV-1 (Major)** | Major feature broken, significant users affected | < 15 min | Engineering Manager | Search broken, checkout fails |
| **SEV-2 (Minor)** | Degraded experience, workaround exists | < 30 min | Tech Lead | Slow page loads, partial search outage |
| **SEV-3 (Trivial)** | Cosmetic issue, single user impact | Next business day | Individual engineer | Typos, minor UI glitch |

### Incident Command System (ICS)

```
┌─────────────────────────────────────────────────────┐
│              INCIDENT COMMAND SYSTEM                 │
│                                                      │
│  ┌─────────────┐                                    │
│  │ IC (指挥者)  │ ← Overall coordination            │
│  │ Decision    │   Final authority on all decisions  │
│  └──────┬──────┘                                    │
│         │                                           │
│  ┌──────┴──────┬──────────┬──────────┐             │
│  │   Comms     │   Scribe  │   SME(s)  │            │
│  │ 外部沟通     │   记录员   │   技术专家  │            │
│  │ 用户通知     │   时间线   │   排障主力  │            │
│  └────────────┘──────────┴──────────┘             │
│                                                       │
│  Rules:                                               │
│  • One voice (IC speaks externally)                  │
│  • Rotate scribe every 30-45 min                     │
│  • Document EVERYTHING in real time                  │
│  • IC can override any decision                       │
└─────────────────────────────────────────────────────┘
```

### Incident Lifecycle

```
DETECTED → TRIAGED → INVESTIGATING → IDENTIFIED → MONITORING → RESOLVED
   │           │          │              │           │           │
   ▼           ▼          ▼              ▼           ▼           ▼
Alert fires  Assign SEV  Gather context  Root cause   Verify fix   Close ticket
Page on-call IC appointed  Diagnosis    Fix applied   No regression  Postmortem starts
```

### Incident Communication Template

When communicating to stakeholders during an active incident:

```markdown
## 🔴 SEV-1: API Gateway Elevated Errors
**Status**: 🟡 Investigating → 🟠 Identified → 🟢 Monitoring → ✅ Resolved
**Started**: 2026-06-20 13:00 UTC
**Impact**: ~40% of API requests returning 5xx errors. Checkout flow affected.
**Current Update**: Database connection pool exhaustion identified. Increasing pool size.

**Next Update**: 2026-06-20 14:00 UTC (or sooner if status changes)
```

**Communication cadence by SEV**:

| SEV | Update Frequency | Channel |
|-----|-----------------|---------|
| SEV-0/SEV-1 | Every 30 min minimum | Slack (#incidents), Status Page, Email to execs |
| SEV-2 | Every 60 min | Slack, Status Page |
| SEV-3 | End of incident summary | Ticket comment only |

---

## Part 3: Postmortem Culture (Blameless!)

### The Golden Rule

> **A blameless postmortem is not about absolving individuals of responsibility. It is about acknowledging that complex systems fail in ways that cannot be attributed to a single person's mistake.**

If you blame someone for an incident:
- They will hide mistakes next time
- You lose the opportunity to learn from the systemic issue
- Your team develops a culture of fear
- Future incidents get worse because people don't speak up

### Postmortem Structure

```markdown
# Postmortem: [Short Title]

## Metadata
- **Date**: YYYY-MM-DD
- **Duration**: X hours (HH:MM – HH:MM UTC)
- **SEV Level**: SEV-X
- **Author**: @name
- **Reviewer**: @lead

## Executive Summary (TL;DR)
> 2-3 sentences. What happened, what was the impact, and what we're doing about it.
> Executives should understand everything from this section alone.

## Timeline
| Time (UTC) | Event |
|------------|-------|
| HH:MM | Alert fired: [alert name] |
| HH:MM | On-call acknowledged |
| HH:MM | Investigation started |
| HH:MM | Root cause identified |
| HH:MM | Mitigation applied |
| HH:MM | Service recovered |

## Impact Analysis
- Affected users: X% (or number)
- Duration of degradation: X minutes
- Revenue impact: $X (estimate) or "No direct revenue impact"
- User-facing symptoms: [description]

## Root Cause
> The deepest technical explanation. Include diagrams, logs snippets, config excerpts.
> Explain WHY this happened, not just WHAT happened.

## Contributing Factors (The "Five Whys")
1. **Direct cause**: [what broke]
2. **Why?**: [first layer reason]
3. **Why?**: [deeper reason]
4. **Why?**: [systemic issue]
5. **Why?**: [organizational/process gap] ← THIS is where the real fix lives

## Detection & Recovery
- How was it detected? (alerting, user report, dashboard?)
- How long to detect? (MTTD — Mean Time To Detect)
- How long to recover? (MTTR — Mean Time To Resolve)
- Could detection be faster? How?
- Could recovery be faster? How?

## Lessons Learned

### What went well 👍
- (Be specific — "team responded quickly" is too vague)
- "PagerDuty reached primary on-call in 42 seconds"
- "Runbook step 3 had the exact command needed"

### What went wrong 👎
- (Again, be specific and actionable)
- "Runbook was outdated — step 4 referenced old config format"
- "No integration test for database migration scripts"

### Action Items
| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| 1 | [Specific action verb] | @person | YYYY-MM-DD | Open/Done/Wontfix |

**Rules for action items**:
- Every action has an owner and deadline
- Actions address contributing factors, not just the immediate bug
- Review action items at next team meeting
- Close items only after verification, not just "it looks done"
```

---

## Part 4: On-Call Excellence

### Building a Healthy On-Call Rotation

**Bad on-call burns people out. Good on-call is sustainable.**

#### Core Principles

| Principle | Description |
|-----------|-------------|
| **Primary + Secondary** | Never have a single point of failure. Primary pages first, secondary backs up if no response. |
| **Maximum rotation length** | 1 week recommended, 2 weeks absolute max. Longer rotations increase burnout exponentially. |
| **Follow-the-sun** | If global team, rotate so each timezone covers their daytime hours. |
| **Compensatory time off** | After a rough on-call shift, give compensatory time off. |
| **No development work while on-call** | Focus on incidents, toil reduction, or self-paced learning. Don't ship features. |
| **Page budget** | Limit paged incidents per shift (e.g., max 5/week). Exceeding triggers process review. |

#### On-Call Toolkit

Every on-call engineer needs these ready:

```bash
# 1. Quick status dashboard (one command)
alias status='curl -s https://grafana.company.com/d/oncall-status | jq'

# 2. Runbook finder
function find_runbook() {
  grep -rl "$1" ~/runbooks/ 2>/dev/null | head -5
}

# 3. Quick service health check
alias svc-health='kubectl get pods -A -o wide | grep -v Running'

# 4. Recent errors (last 10 min)
alias recent-errors='kubectl logs -l app=$1 --since=10m | grep -i "error\\|exception" | tail -20'

# 5. Who's on call today
alias whos-on-call='pduty schedules list --active'
```

#### Reducing Alert Fatigue

**The #1 problem in on-call health is bad alerts.**

| Anti-pattern | Better approach |
|-------------|----------------|
| Alerting every time CPU > 80% for 1 minute | Alert when CPU > 90% for 15 consecutive minutes |
| Email notifications for alerts | Pager (PagerDuty/OpsGenie) for actionable alerts only |
| Same alert firing 200 times/night | Alert grouping + deduplication (every unique symptom once) |
| Alerts requiring manual investigation | Alerts with suggested action in message |
| Waking someone up for auto-recoverable issues | Auto-remediation first, page only if recovery fails |

```yaml
# Example: Well-crafted alert definition
- alert: HighErrorRate_BudgetBurnFast
  expr: |
    (
      sum(rate(http_requests_total{status=~"5.."}[1h]))
      / sum(rate(http_requests_total[1h]))
    ) > 0.007  # 6x normal error budget burn rate
  for: 10m  # Must sustain for 10 min before alerting
  labels:
    severity: critical
    team: platform
  annotations:
    summary: "High error rate consuming error budget 6x faster than allowed"
    runbook: "https://wiki.internal/runbooks/high-error-rate"
    dashboard: "https://grafana.internal/d/error-budget"
    current_error_rate: "{{ $value | humanizePercentage }}"
    suggested_action: "1. Check recent deployments 2. Check Grafana error dashboard 3. Consider rollback"
```

---

## Part 5: Observability Stack

### The Three Pillars

```
                    ┌──────────────────────┐
                    │   OBSERVABILITY      │
                    │                      │
    ┌───────────┐   │  ┌──────┐ ┌──────┐  │   ┌───────────┐
    │ METRICS   │───┼─▶│Prom  ││Grafana│◀──┼───│ Dashboards│
    └───────────┘   │  └──────┘ └──────┘  │   │ Alerting  │
                    │                      │   └───────────┘
    ┌───────────┐   │  ┌──────┐ ┌──────┐  │   ┌───────────┐
    │ LOGS      │───┼─▶│Loki  ││Grafana│◀──┼───│ Search    │
    └───────────┘   │  └──────┘ └──────┘  │   │ Correlation│
                    │                      │   └───────────┘
    ┌───────────┐   │  ┌──────┐ ┌──────┐  │   ┌───────────┐
    │ TRACES    │───┼─▶│Jaeger││Tempo │◀──┼───│ Latency   │
    └───────────┘   │  └──────┘ └──────┘  │   │ Topology  │
                    └──────────────────────┘   └───────────┘
```

### The Four Golden Signals (Google SRE)

| Signal | Question | PromQL Example | Threshold |
|--------|----------|---------------|-----------|
| **Latency** | How long does it take? | `histogram_quantile(0.99, rate(...))` | p99 < 200ms |
| **Traffic** | How much demand? | `rate(requests_total[5m])` | Trend analysis |
| **Errors** | How many failing? | `rate(errors_total[5m]) / rate(total[5m])` | < 0.1% |
| **Saturation** | How close to capacity? | `(1 - avg(node_memory_available)) * 100` | < 80% |

Plus two modern additions:
| Signal | Question | Tool |
|--------|----------|------|
| **Saturation deep dive** | Which resource is the bottleneck? | cAdvisor / node-exporter |
| **Distribution** | Are latency/errors evenly distributed? | Histogram buckets, heatmaps |

### Instrumentation Maturity Model

| Level | Name | Characteristics |
|-------|------|----------------|
| 0 | **Unknown** | No metrics. You find out about problems from users. |
| 1 | **Basic** | Infrastructure metrics (CPU, memory, disk). No application insight. |
| 2 | **Good** | Application metrics exist but scattered. Some dashboards. |
| 3 | **Structured** | Standardized metrics across services. RED method or USE method consistently applied. |
| 4 | **SLO-driven** | SLIs defined, SLO dashboards, error budget tracking, burn rate alerts. |
| 5 | **Predictive** | Anomaly detection, capacity forecasting, proactive remediation. |

**Goal**: Get every service to level 4. That's where SRE really begins.

---

## Part 6: Toil Elimination

### What Is Toil?

Toil is operational work that meets **all** of these criteria:

- ☐ **Manual** — Requires human intervention (can't be fully automated)
- ☐ **Repetitive** — You've done this before and will do it again
- ☐ **Automatable** — Could be automated with sufficient effort
- ☐ **Tactical** — No enduring value; doesn't scale the system
- ☐ **No enduring value** — Doesn't improve the service or teach you anything new

### Common Toil Sources & Fixes

| Toil Type | Example | Fix |
|-----------|---------|-----|
| Manual deployment | "SSH into server and pull latest code" | CI/CD pipeline |
| Certificate renewal | "Log in and click renew" | certbot / cert-manager auto-renewal |
| Capacity provisioning | "User asks for more disk, I add it" | Auto-scaling + quota automation |
| Onboarding new service | "Manually set up monitoring, logging, alerts" | Platform template / scaffolding tool |
| Incident triage | "Same alert fires nightly, manually acknowledge" | Fix the root cause OR suppress properly |
| Access management | "Add user to group X" repeated daily | Self-service RBAC portal |
| Backup verification | "Check backup succeeded" | Automated restore test + alert on failure |

### Measuring Toil

Track the percentage of engineering time spent on toil:

```promql
# Proxy metric: ratio of manual intervention tickets to total work items
# (This is imperfect but gives directional signal)
sum(increase(manual_intervention_tickets[30d])) 
/ 
sum(increase(all_work_items[30d])) 
* 100
```

**Target**: < 30% toil for mature SRE teams. If > 50%, declare emergency and focus exclusively on automation.

---

## Part 7: Capacity Planning

### The Planning Process

```
┌──────────────────────────────────────────────────┐
│              CAPACITY PLANNING CYCLE              │
│                                                    │
│  1. MEASURE                                       │
│     Current traffic, growth rate, resource usage  │
│                                                    │
│  2. FORECAST                                      │
│     Predict demand 3-6 months out                 │
│     (Use historical trend + known events)         │
│                                                    │
│  3. PLAN                                          │
│     Calculate resources needed + headroom         │
│     Account for lead times                        │
│                                                    │
│  4. EXECUTE                                       │
│     Provision in advance                          │
│     Validate under load                           │
│                                                    │
│  5. REPEAT                                        │
│     Quarterly review cycle                         │
└──────────────────────────────────────────────────┘
```

### Practical Formulas

**Resource calculation**:
```
instances_needed = (peak_rps × latency_per_request_safety_factor) / rps_per_instance

Example:
- Peak: 5000 RPS
- Each instance handles 100 RPS at p99 < 200ms
- Safety factor: 1.5 (handles burst + buffer)
- Needed: 5000 × 1.5 / 100 = 75 instances
```

**Storage projection**:
```
storage_next_quarter = current_usage_gb × (1 + growth_rate)^quarters_ahead × compression_ratio
```

**Database capacity**:
```
connections_needed = (active_users × avg_queries_per_page × concurrent_pages_per_user) / queries_per_connection
```

### Lead Time Awareness

| Resource type | Typical lead time | Planning horizon |
|---------------|------------------|-----------------|
| VM / Instance | Minutes to hours | Weekly forecast |
| Physical hardware | Weeks to months | Quarterly planning |
| IP address allocation | Instant | Just-in-time |
| DNS changes | Minutes (propagation up to 48h) | Plan ahead for critical |
| SSL certificates | Instant (Let's Encrypt) | Auto-renewal |
| Database scaling (vertical) | Hours | Daily review |
| Database scaling (horizontal) | Days to weeks | Monthly planning |

---

## Part 8: Chaos Engineering

### Philosophy

> "The best way to avoid failure is to fail constantly." — Netflix

Chaos engineering is the **discipline of experimenting on a system** to build confidence in its ability to withstand turbulent conditions.

### Principles (Principles of Chaos Engineering)

1. **Build a hypothesis around steady-state behavior** — Define what "normal" looks like
2. **Vary real-world events** — Don't simulate failures; cause them
3. **Run experiments in production** — Staging doesn't match production reality
4. **Minimize blast radius** — Start small, contained experiments
5. **Automate continuous experiments** — Make chaos part of the deployment pipeline

### Experiment Maturity Levels

| Level | Experiment Type | Blast Radius | Automation |
|-------|----------------|-------------|------------|
| 1 | Kill a single pod | One replica | Manual |
| 2 | Kill entire service | One service | Semi-auto |
| 3 | Network partition between AZs | Multi-AZ | Scheduled job |
| 4 | Region-level failure simulation | Full region | Fully automated |
| 5 | Game Day (full scenario) | Entire system | Planned exercise |

### Tools

| Tool | Scope | Best For |
|------|-------|----------|
| **Chaos Mesh** | K8s-native | Pod kill, network fault, IO stress, JVM chaos |
| **Litmus Chaos** | K8s-native | Cloud-native chaos experiments |
| **Gremlin** | Multi-platform | Host-level experiments (CPU, memory, network) |
| **Chaos Monkey** (Netflix) | AWS | Random instance termination |
| **Powerful Seaper** | Network | Network latency, loss, partition simulation |

### Experiment Template

```markdown
# Chaos Experiment: Pod Failure Resilience

## Hypothesis
> When a random pod in the payment service is terminated, the system will
> automatically recover within 30 seconds with zero failed transactions.

## Steady-State Definition
- Success rate: > 99.9%
- p99 latency: < 300ms
- Active connections: stable ± 5%

## Experiment Steps
1. Baseline: Record steady-state metrics for 5 minutes
2. Action: Terminate one randomly selected payment pod
3. Observe: Monitor metrics for 5 minutes
4. Verify: Did the hypothesis hold?

## Results
- Time to recover: __ seconds
- Failed transactions: __
- Error budget consumed: __
- Hypothesis: CONFIRMED / REJECTED

## Learnings
- (What did we learn about our system's resilience?)
```

---

## 📖 Essential Reading Order

Read in this order. Each builds on the previous.

| Order | Book | Why First | Free? |
|-------|------|----------|-------|
| 1 | **Site Reliability Engineering** | Foundational concepts. Everything else references this. | [Yes](https://sre.google/books/) |
| 2 | **The Site Reliability Workbook** | Hands-on implementation of concepts from book #1. | [Yes](https://sre.google/workbook/table-of-contents/) |
| 3 | **Seeking SRE** | Case studies from companies beyond Google. | [Yes](https://sre.google/seeking-sre/table-of-contents/) |
| 4 | **Implementing SLOs** | Deep dive into SLI/SLO methodology. Practical. | No |
| 5 | **Building Secure & Reliable Systems** | SRE meets security. Essential for modern ops. | Partially |

**Pro tip**: All three Google books are free online. Read them. Take notes. Discuss with your team.

---

## ✅ Self-Check: Can You...

### Concepts
- [ ] Explain SLI vs SLO vs SLA with concrete examples from a real service
- [ ] Calculate the error budget for any given SLO and window
- [ ] Design a set of SLIs for a hypothetical microservice
- [ ] Write a proper blameless postmortem (with contributing factors, not just root cause)
- [ ] Explain why 100% availability is usually the wrong target

### Hands-On Skills
- [ ] Create a Prometheus alert based on error budget burn rate
- [ ] Set up a basic observability stack (Prometheus + Grafana + Loki)
- [ ] Run a chaos experiment using Chaos Mesh
- [ ] Build an incident response runbook
- [ ] Design an on-call rotation schedule for a global team

---

## 🔗 Related Resources

- [← Back to English Home](../README.md)
- [10 · Cloud Native & IaC](./10_Cloud_Native_IaC/)
- [09 · Database](./09_Database/)
- [08 · Monitoring & Observability](./08_Monitoring_Observability/)
- [12 · Interview Prep](./12_Interview_Prep/)
