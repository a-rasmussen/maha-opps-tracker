# MAHA Mortality Tracker — Project Instructions v1.1

**Status:** v1.1 DRAFT — 2026-04-27 (updates v1.0 from 2026-04-26 with scope decisions, Substack tooling, infrastructure live)
**Owner:** Angie Rasmussen (angierasmussen@gmail.com)
**Public-facing site name:** Bobby Kennedy Jr. Body Count
**Sister project:** [MAHA Opps Tracker](../) — independent research project, federated at the database level only.

---

## 1. Purpose

The MAHA Mortality Tracker estimates and reports mortality consequences attributable to actions by Robert F. Kennedy Jr., Children's Health Defense, allied state and federal officials, and HHS under Kennedy's leadership. The project produces:

1. A **Kennedy Action Registry** — comprehensive, source-linked log of attributable actions.
2. **Mortality Assessments** — per-action mortality estimates with explicit methodology and confidence ranges.
3. **Custom mortality projection models** — open, peer-reviewable models for policy → coverage → mortality, coverage loss → mortality, response capacity → outbreak severity, and clinical trial termination mortality.
4. A **public-facing site** — *Bobby Kennedy Jr. Body Count* — presenting attributable mortality counts with full methodology transparency.

The project's core methodological commitment: **counts are aggregate, attribution is by accepted epidemiological methods, and every claim is documented end-to-end.** No individual decedents are named. No counts are presented without their tier, methodology, and source.

---

## 2. Context

- The project owner is a virologist with 25 years' experience specializing in host-pathogen interactions for emerging viruses, and co-Editor-in-Chief of *Vaccine*.
- The owner uses computational and AI approaches but does not code; methodology design is in scope, implementation is delegated or AI-assisted.
- The owner has ADHD; clear, direct communication and explicit checklists work best.
- The audience is the public, journalists, policymakers, and the public health/scientific community.
- The project starts with a methodology proving case (Samoa 2019) and scales out from there.

---

## 3. Three-Tier Evidence Framework (CRITICAL)

Every mortality claim on the public site carries a tier label and methodology link.

### Tier 1 — Documented causal chain
- Action documented in primary sources.
- Mechanism documented (specific intervention, measurable behavioral or coverage change, outbreak following).
- Affected population identified by name (specific country, state, county, cohort).
- Deaths counted and reported by official sources.
- Causal chain defensible end-to-end without statistical inference.

### Tier 2 — Statistical attribution
- Action documented.
- Mechanism documented at population level.
- Excess mortality estimable using accepted epidemiological methods (counterfactual baseline).
- Confidence interval can be specified.

### Tier 3 — Projected mortality
- Action documented.
- Mortality estimate based on peer-reviewed forward-looking modeling.
- No retrospective deaths yet measurable.
- Clearly labeled as projected.

**Counts on the public site are presented per tier, with combined totals shown only with explicit confidence bands.** No comingling of tier counts without disclosure.

---

## 4. Categorization Rules

### 4.1 What gets entered into the Kennedy Action Registry
See Research Protocol Section 2 (Scope).

### 4.2 What gets assessed (registry → assessment)
An action moves to mortality assessment only when ALL eligibility gates are met (Research Protocol Section 7):
1. Documentable causal mechanism
2. Definable affected population
3. Available mortality data or model basis
4. Time window definable
5. Counterfactual specifiable

Failed gates → status `Hold` with documented reason. Held items reviewed monthly.

### 4.3 What gets published
An assessed action is published only after:
- Methodology peer review (Tier 2/3) or chain documentation review (Tier 1)
- Citation completeness check
- URL re-verification immediately before publishing
- Editorial review for tone — factual reporting, not advocacy framing in the entry text itself (the *site name* may be pointed; entry copy is not)

### 4.4 What does NOT belong here
- Speculative attribution without documented mechanism
- Mortality "during Kennedy's tenure" without attribution chain
- Individual named decedents (aggregate counts only)
- Causation claims against named individuals beyond Kennedy himself

---

## 5. Output Architecture

### 5.1 Notion (federated)

**Read-only relations to MAHA Opps Tracker databases:**
- States
- Districts
- Disease Tracker
- Federal Policy Changes
- (No writes from this project to those databases.)

**New databases under MAHA Mortality Tracker parent page:**

| Database | Purpose |
|---|---|
| Kennedy Action Registry | Master action log (input pipeline) |
| Mortality Assessments | Per-action mortality estimates with tier, method, count, CI |
| Affected Populations | Reusable population definitions referenced by assessments |
| Mortality Models | Model registry — versioning, inputs, outputs, validation status |
| Public Site Entries | Curated entries approved for publication, with editorial state and retraction tracking |
| Sources Library | Verified citation library with URL verification timestamps |
| Methodology Notes | Protocol-level decisions and rationale, versioned |

Schema details: `Action_Registry_Schema_v1.md` (and forthcoming schema docs for the other DBs).

### 5.2 GitHub
- **Repo:** `maha-mortality-tracker` (private during build; public at Phase 3)
- **Layout:** see `Research_Protocol_v1.0.md` Section 12.

### 5.3 Google Drive
- New folder, sister to MAHA Opps Tracker folder.
- Master Summary doc.
- Methodology working files.
- External references library (PDFs, agency docs, etc.).

### 5.4 Public-facing site
- Static site generated from `site/public/`.
- Hosted on GitHub Pages initially; revisit hosting at Phase 3 if traffic / legal calculus changes.
- Reads from curated `Public Site Entries` Notion DB via export.

---

## 6. Action Registry Schema (high-level)
See `Action_Registry_Schema_v1.md`.

## 7. Mortality Assessment Schema (high-level)
TBD in v1.1 alongside the Mortality Assessment Protocol.

---

## 8. Custom Modeling Architecture

Five model families, ranked by leverage. Owner designs methodology; implementation in Python/R, peer-reviewable.

| # | Model | Approach | Library basis | Validation |
|---|---|---|---|---|
| 1 | Policy → coverage → outbreak mortality | SIR / SEIR with policy-driven coverage parameters | IDM open-source measles/pertussis modules | Japan 1993 MMR withdrawal; UK 1998 Wakefield-era drop |
| 2 | Coverage loss → mortality | Insurance-status–to–mortality regression | KFF/CBPP/Penn LDI methodology adapted | Sommers et al. Medicaid expansion; Card/Dobkin Medicare |
| 3 | Outbreak response capacity | Staffing/funding → duration & attack rate | Empirical regression on historical responses | TX/NM 2025 measles as anchor |
| 4 | Clinical trial termination mortality | Per-trial counterfactual on completed-trial outcomes | Standard clinical trial modeling | NCT-level cohort tracking |
| 5 | Hesitancy → coverage decline | Bayesian, multivariable | Larson et al. Vaccine Confidence Project | Adapt rather than build new |

Model registry tracked in Notion `Mortality Models` DB with: model name, version, inputs, outputs, validation status, last run date, code location (GitHub path).

---

## 9. Research Protocol
See `Research_Protocol_v1.1.md`.

## 10. Mortality Assessment Protocol
TBD — `assessment_protocol_v0.1.md` in development. Will define:
- Methodology selection per tier
- Counterfactual specification process
- Confidence interval reporting
- Peer-review process (internal review for v1; external for v2+)
- Editorial workflow to public site

---

## 11. Workflow Rules

1. **Verify URLs before embedding.** Never embed a URL from memory. Verify it resolves at the time of capture and re-verify monthly.
2. **Exhaust tools before declaring a data gap.** WebSearch → WebFetch → MCP servers (PubMed, ClinicalTrials.gov, etc.) → LunarCrush → Chrome browser tools → alternative sources. Only flag gaps after all are tried.
3. **Aggregate-only attribution.** Counts only. No named individual decedents.
4. **Documented attribution chain.** For influence-based actions (Kennedy → CHD → state actor → outcome), the chain must be documented in the registry entry.
5. **Tier discipline.** Each entry carries its tier; site never displays a count without tier and methodology link.
6. **Federated, not shared.** This project does not write to MAHA Opps Tracker databases.
7. **Version everything.** Protocols, registry snapshots, model runs, public site entries.
8. **Editorial discipline.** Entry copy is factual. Site name is pointed. The two are kept separate by design.
9. **Sources at every step.** Every data point links to a primary source.
10. **Pre-HHS actions are in scope** when the operating mechanism (platform-driven coverage decline, CHD activity) is the same one operating during the federal tenure.

---

## 12. Citation Rules

Every data point and claim has an inline hyperlinked source pointing to the **specific page or document** containing the data. No generic domain links.

**Format:** `[Source: {Publisher}, {Document Title}, {Date}]({specific URL})`

Verify URLs before embedding. Re-verify monthly per Research Protocol Section 9.2.

For modeled estimates, cite both the model documentation (in `Mortality Models` DB) and the underlying methodology source.

---

## 13. Formatting Spec for Doc Generation
Inherits from MAHA Opps Tracker formatting spec (DXA-only widths, helper functions, ShadingType.CLEAR, etc.). When generating any docx output for this project, read the docx skill `SKILL.md` first.

---

## 14. Visualization Standards

Every public-facing visualization must include:
- Tier label
- Methodology link
- Source citation
- Confidence interval where applicable
- Time window
- Affected population definition

Avoid:
- "Body count" framing within data labels (this lives in the site name only — labels stay technical)
- Mortality counts without tier labels
- Ranges presented as point estimates

---

## 15. Data Sources Directory

Inherits the MAHA Opps Tracker source directory plus:
- ClinicalTrials.gov (NCT-level data for trial termination assessments)
- NIH RePORTER terminated-grants endpoint
- DoD MSMR (Medical Surveillance Monthly Report) for military-population baselines
- WHO measles outbreak reports (for international cases including Samoa)
- Samoan Ministry of Health (for Samoa 2019 retrospective)
- IDM (Institute for Disease Modeling) open-source modules
- Vaccine Confidence Project / Larson group publications

Detailed list lives in Sources Library Notion DB.

---

## 16. Phased Roadmap

| Phase | Duration (est.) | Output | Status |
|---|---|---|---|
| **0 — Setup** | 2026-04-26 to ongoing | Project instructions, research protocol, schema docs, Notion DB structure, GitHub repo | **Mostly done.** v1.1 docs in repo. Notion parent + Kennedy Action Registry live. 6 additional DBs pending (Mortality Assessments, Affected Populations, Mortality Models, Public Site Entries, Sources Library, Methodology Notes). |
| **1 — Methodology proving case** | 4–6 weeks | Samoa 2019 Tier 1 case file, full assessment workflow demonstrated end-to-end | Not started |
| **2 — Registry + first 10 assessments** | 8–12 weeks | Action Registry populated; 10 assessments mixing Tiers 1/2/3 (TX measles, ACIP MMRV, COVID vax recommendation, FL HepB, OBBBA Medicaid, DoW flu, 3 NIH trial halts, fluoride withdrawal) | Not started |
| **3 — Public site launch** | 12–16 weeks | Site live with 10–15 entries; methodology pages; legal review complete | Not started |
| **4 — Ongoing maintenance + model refinement** | Ongoing | Periodic surveillance per protocol; model v2 development | Not started |

---

## 17. Open Project Questions

1. Hosting/legal exposure — who hosts the public site? Recommend a media-law conversation before Phase 3.
2. Coordinator role — solo through Phase 2 or expand earlier?
3. Funding for sustained model development?
4. External methodology peer review — who? When?
5. Retraction/correction policy on the public site — needs to be drafted before Phase 3.
6. Data-protection/security — repo private during build, but registry contains opposition-research-style content. Threat model?

---

## 18. Version History

| Version | Date | Changes |
|---|---|---|
| v1.0 DRAFT | 2026-04-26 | Initial project instructions. Three-tier evidence framework. Federated Notion architecture. Phased roadmap. References Research Protocol v1.0 and Action Registry Schema v1. |
| v1.1 DRAFT | 2026-04-27 | Synced to Research Protocol v1.1 reference. Updated Phase 0 status to reflect live Notion infrastructure (parent page + Kennedy Action Registry). Pre-HHS scope expanded broad. International scope in. Substack monitoring on Claude side via WebSearch (no user manual browsing). GitHub push workflow uses `push_to_github.py` script with fine-grained PAT (see project memory `feedback_github_push.md`). |

---

*End of Project Instructions v1.1 DRAFT.*
