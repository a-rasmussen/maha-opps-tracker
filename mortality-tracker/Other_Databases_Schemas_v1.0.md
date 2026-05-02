# MAHA Mortality Tracker — Schemas for Remaining Databases v1.0

**Status:** v1.0 — 2026-04-27 — All 6 databases created in Notion
**Project:** MAHA Mortality Tracker
**Parent doc:** `MAHA_Mortality_Tracker_Project_Instructions_v1.md`

This document specifies schemas for the six remaining Notion databases (everything except Kennedy Action Registry, which has its own dedicated schema doc). Each is designed for the mortality tracker workflow but kept lightweight for v1 — fields can be added in v1.1+ as the assessment pipeline matures.

## Live Notion IDs (created 2026-04-27)

All six databases live under MAHA Mortality Tracker parent page (`34fb9126-7234-8132-82fb-d1befcb5ef37`).

| Database | Notion URL | Data Source ID (for API/MCP) |
|---|---|---|
| Sources Library | [link](https://www.notion.so/561328d0e6494a2691bfeff94234a863) | `5ec90b0d-5f7c-46fa-9aec-b0222f0e0fbb` |
| Affected Populations | [link](https://www.notion.so/68a53ea0499e4710a6144fc0be43b91e) | `2df49cf1-c51c-4499-8c9c-fbb1408e22b1` |
| Mortality Models | [link](https://www.notion.so/63af173b158e4e27ad72d40a7997529c) | `e2e0dcc1-12fa-4c65-b73d-bb49cc5d601a` |
| Methodology Notes | [link](https://www.notion.so/cda0a4d4a2a84d4ca2ab909eb878df98) | `5b56c17f-5167-41b7-9846-9b5ff5bb21f9` |
| Mortality Assessments | [link](https://www.notion.so/baa3214569ce4dc98dfadcd32af2350b) | `7c1ad756-552e-4023-a018-801a65be6241` |
| Public Site Entries | [link](https://www.notion.so/2e7c56204ec142539cac043319aacc24) | `eae091eb-8d7e-4b82-9ae0-ef5afaba01e5` |

**Implementation deltas from spec:**

- Mortality Assessments `Supersedes` field implemented as `Supersedes Assessment ID` (RICH_TEXT) instead of self-relation. Self-relations require post-creation update via `update_data_source` and were deferred to v1.1.
- All other fields and relations match the spec exactly.

**Creation order** (forward relations only; back-relations added in v1.1 update pass):
1. Sources Library
2. Methodology Notes
3. Affected Populations
4. Mortality Models
5. Mortality Assessments (the central hub — depends on the four above)
6. Public Site Entries (depends on Mortality Assessments)

---

## Database 2 — Mortality Assessments

**Purpose:** Per-action mortality estimate with explicit tier, methodology, count, confidence interval, and editorial state. One assessment per Action Registry entry that passes eligibility gates. Revisions create new versions; superseded assessments are kept for audit.

**ID prefix:** `MA`

**Field schema:**

| Field | Type | Notes |
|---|---|---|
| Assessment Title | TITLE | `[Tier N] {Action} — {Population} — {Time Window}` |
| ID | UNIQUE_ID PREFIX 'MA' | Auto-increment |
| Related Action | RELATION → Kennedy Action Registry | REQUIRED |
| Tier | SELECT (Tier 1, Tier 2, Tier 3) | Inherits from Action's Tier Candidate; can refine |
| Status | SELECT (Draft, Internal Review, Methodology Review, Approved for Publication, Published, Superseded, Retracted) | Workflow state |
| Methodology Type | SELECT (documented_chain, excess_mortality, modeled, hybrid, other) | High-level method bucket |
| Methodology Notes | RELATION → Methodology Notes | One or more relevant methodology decisions |
| Counterfactual | RICH_TEXT | What would have happened without the action |
| Time Window Start | DATE | Bounds the period mortality is attributed to |
| Time Window End | DATE | Same |
| Affected Population | RELATION → Affected Populations | Reusable population definition |
| Mortality Count Point Estimate | NUMBER | Best single estimate |
| Mortality CI Lower | NUMBER | Lower bound |
| Mortality CI Upper | NUMBER | Upper bound |
| Mortality CI Type | SELECT (95%, 90%, 80%, IQR, range, other) | What kind of interval |
| Calculation Notes | RICH_TEXT | How the number was computed; key assumptions |
| Model Used | RELATION → Mortality Models | If a custom model produced the estimate |
| Primary Sources | RELATION → Sources Library | Citations |
| Reviewer | PEOPLE | Internal reviewer (and external when added) |
| Reviewer Decision | SELECT (Approved, Revisions Requested, Rejected, Pending) | |
| Reviewer Notes | RICH_TEXT | |
| Assessment Version | RICH_TEXT | Semantic version (v1.0, v1.1) for revisions |
| Supersedes | RELATION → Mortality Assessments (self) | Earlier version this replaces (one-way for v1; dual in v1.1) |
| Published Date | DATE | When this version went live on the public site |
| Last Reviewed | DATE | |
| Retraction Reason | RICH_TEXT | Required if Status = Retracted |
| Captured Date | CREATED_TIME | Auto |
| Captured By | PEOPLE | Auto on create |

---

## Database 3 — Affected Populations

**Purpose:** Reusable population definitions referenced by mortality assessments. A population (e.g., "Samoan children under 5, October 2019 – February 2020") may be the affected population for multiple assessments and for multiple tiers, so it lives as a first-class entity.

**ID prefix:** `AP`

**Field schema:**

| Field | Type | Notes |
|---|---|---|
| Population Name | TITLE | Concise descriptor |
| ID | UNIQUE_ID PREFIX 'AP' | |
| Description | RICH_TEXT | Full definition |
| Geographic Scope | MULTI_SELECT (federal, state, county, district, international, custom) | |
| Geographic Detail | RICH_TEXT | Free text — country, region, etc. |
| State | RELATION → MAHA Opps States (read-only) | |
| District | RELATION → MAHA Opps Districts (read-only) | |
| Demographic Filters | RICH_TEXT | Age, sex, race/ethnicity, condition, occupation, etc. |
| Population Size | NUMBER | Best estimate |
| Population Size Source | URL | Citation |
| Population Size As Of | DATE | Vintage of the size estimate |
| Time Window Applicability | RICH_TEXT | When this population definition applies |
| Notes | RICH_TEXT | |
| Captured Date | CREATED_TIME | Auto |

---

## Database 4 — Mortality Models

**Purpose:** Registry of models used or developed for mortality projection. Includes peer-reviewed models we adapt and custom models we build. Each entry tracks version, code location, validation status.

**ID prefix:** `MM`

**Field schema:**

| Field | Type | Notes |
|---|---|---|
| Model Name | TITLE | |
| ID | UNIQUE_ID PREFIX 'MM' | |
| Model Family | SELECT (coverage_to_outbreak, coverage_loss_mortality, response_capacity, trial_termination, hesitancy_to_coverage, custom, adapted_external) | Maps to Project Instructions §8 |
| Version | RICH_TEXT | Semantic versioning (v1.0) |
| Status | SELECT (Draft, In Development, Internal Validation, Peer Review, Validated, Published, Retired) | |
| Description | RICH_TEXT | |
| Inputs | RICH_TEXT | List of input variables and their sources |
| Outputs | RICH_TEXT | List of output variables and units |
| Methodology Reference | RICH_TEXT | Underlying paper(s), framework(s) |
| Sources Library | RELATION → Sources Library | Citations |
| Underlying Library | RICH_TEXT | e.g., `idmtools`, `epimodel`, custom Python |
| Code Location | URL | GitHub path |
| Validation Status | SELECT (Not Validated, Internal, Peer Reviewed, Published) | |
| Validation Notes | RICH_TEXT | |
| Owner | PEOPLE | |
| Created Date | CREATED_TIME | Auto |
| Last Updated | DATE | |

---

## Database 5 — Public Site Entries

**Purpose:** Curated entries approved for the public-facing site (*Bobby Kennedy Jr. Body Count*). One entry per published assessment version. Editorial state, retraction handling, and live-site fields all live here.

**ID prefix:** `PSE`

**Field schema:**

| Field | Type | Notes |
|---|---|---|
| Entry Title | TITLE | Public-facing title |
| ID | UNIQUE_ID PREFIX 'PSE' | |
| Slug | RICH_TEXT | URL slug for the live site |
| Related Assessment | RELATION → Mortality Assessments | REQUIRED |
| Tier Display | SELECT (Tier 1, Tier 2, Tier 3) | Inherits from Assessment |
| Display Status | SELECT (Draft, In Review, Approved, Live, Retracted) | |
| Public Body | RICH_TEXT | Prose displayed publicly |
| Mortality Count Display | RICH_TEXT | Formatted count, e.g., "83 deaths" |
| Confidence Interval Display | RICH_TEXT | Formatted CI text |
| Methodology Link | URL | Link to public methodology page |
| Sources Display | RICH_TEXT | Formatted citation block (rendered on site) |
| First Published | DATE | |
| Last Updated | DATE | |
| Editorial Approver | PEOPLE | |
| Approval Date | DATE | |
| Retraction Notice | RICH_TEXT | Public-facing retraction text if applicable |
| Retraction Date | DATE | |
| Public URL | URL | Live site URL once published |

---

## Database 6 — Sources Library

**Purpose:** Verified citation library. The same source (e.g., a CDC outbreak report, a peer-reviewed paper, an HHS press release) is often cited across multiple Registry actions, assessments, and public entries. Logging it once with verified URL and timestamp avoids re-verifying repeatedly.

**ID prefix:** `SRC`

**Field schema:**

| Field | Type | Notes |
|---|---|---|
| Source Title | TITLE | |
| ID | UNIQUE_ID PREFIX 'SRC' | |
| Author/Publisher | RICH_TEXT | |
| Publication Date | DATE | |
| URL | URL | Primary URL |
| Source Type | SELECT (matches Action Registry options) | official_document, press_release, federal_register, court_filing, news_article, social_media, ngo_filing, congressional_record, peer_reviewed, other |
| Authority Tier | SELECT (1, 2, 3) | |
| Topic Tags | MULTI_SELECT (vaccines, outbreaks, federal_policy, state_policy, funding, CHD, kennedy_statements, samoa, ACIP, OBBBA, hpai, environmental, mortality, methodology, other) | |
| Last Verified | DATE | |
| Verification Status | SELECT (Verified, Stale, Broken, Replaced) | |
| Replacement URL | URL | Set if status = Replaced |
| Archive URL | URL | Wayback Machine or other archive |
| Used In Actions | RELATION → Kennedy Action Registry | Back-reference |
| Notes | RICH_TEXT | |
| Captured Date | CREATED_TIME | Auto |

---

## Database 7 — Methodology Notes

**Purpose:** Protocol-level decisions and rationale, versioned and citable. When a methodological choice is made (how to define counterfactual for vaccine policy reversals, how to handle tier ambiguity in ACIP votes, etc.), it's recorded here with its rationale and the protocol version it applies to. Mortality Assessments link to relevant Methodology Notes so the reasoning chain is traceable.

**ID prefix:** `MN`

**Field schema:**

| Field | Type | Notes |
|---|---|---|
| Note Title | TITLE | |
| ID | UNIQUE_ID PREFIX 'MN' | |
| Topic | MULTI_SELECT (scope, attribution, tier, statistical_method, model_validation, retraction, citation, edge_case, other) | |
| Decision | RICH_TEXT | The decision itself |
| Rationale | RICH_TEXT | Why this decision was made |
| Date Decided | DATE | |
| Decided By | PEOPLE | |
| Status | SELECT (Active, Superseded, Withdrawn) | |
| Affects Protocol Version | RICH_TEXT | e.g., `v1.1+` |
| Related Actions | RELATION → Kennedy Action Registry | When the note pertains to specific actions |
| Sources | RELATION → Sources Library | Citations supporting the decision |
| Notes | RICH_TEXT | |
| Captured Date | CREATED_TIME | Auto |

---

## Cross-database relations planned for v1.1

These back-relations require adding fields to already-created databases via `update_data_source`. They are not blocking for v1 use:

| From | To | Purpose |
|---|---|---|
| Kennedy Action Registry | Mortality Assessments | Easy navigation from action to its assessment |
| Affected Populations | Mortality Assessments | Find all assessments using a given population |
| Mortality Models | Mortality Assessments | Find all assessments using a given model |
| Sources Library | Mortality Assessments, Public Site Entries | Find where a source is cited |
| Methodology Notes | Mortality Assessments | Find assessments governed by a decision |

Add in v1.1 once we have data flowing through and the most-used views become clear.

---

## Version history

| Version | Date | Changes |
|---|---|---|
| v1.0 | 2026-04-27 | Initial schemas for the six remaining databases. All six created in Notion same day. Live IDs added to top of document. Forward relations only. Cross-mortality back-relations and Mortality Assessments self-relation (Supersedes) deferred to v1.1. |
