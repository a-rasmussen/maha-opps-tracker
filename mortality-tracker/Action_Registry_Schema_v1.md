# Kennedy Action Registry — Notion Database Schema v1.0

**Status:** v1.0 DRAFT — 2026-04-26
**Project:** MAHA Mortality Tracker
**Parent doc:** `MAHA_Mortality_Tracker_Project_Instructions_v1.md`
**Used by:** Research Protocol v1.0 (capture pipeline)

---

## 1. Purpose

Defines the Notion schema for the **Kennedy Action Registry** — the master log of all actions attributable to Kennedy, CHD, and the broader network that may have mortality consequences. The Registry is the input pipeline to the Mortality Assessment Protocol.

---

## 2. Database identity

- **Name:** Kennedy Action Registry
- **Parent page:** MAHA Mortality Tracker (Notion workspace)
- **ID prefix for entries:** `KAR-NNNN` (zero-padded 4-digit)
- **Entry creation:** via Research Protocol Section 6 capture workflow

---

## 3. Field schema

### 3.1 Identification

| Field | Type | Required | Notes |
|---|---|---|---|
| ID | Formula or auto-number, displayed as `KAR-NNNN` | Yes | Stable identifier; never reused on retraction |
| Action Name | Title | Yes | Short descriptive label (≤ 80 chars). Format: `[YYYY-MM-DD] {Actor}: {Verb-phrase action}`. Example: `[2025-09-18] ACIP: 8-3 vote against MMRV before age 4` |
| Date | Date | Yes | Date the action occurred (not the date captured) |
| Captured Date | Created time (auto) | Yes | When entry was created in Notion |
| Captured By | Person | Yes | User who logged the entry |
| Last Reviewed | Date | No | Last time the entry was reviewed in QC |

### 3.2 Action characterization

| Field | Type | Options |
|---|---|---|
| Type | Select (single) | `schedule_change` / `funding_cut` / `staffing_cut` / `regulatory_action` / `executive_order` / `communication` / `state_proxy` / `clinical_trial_action` / `program_termination` / `nominee_action` / `CHD_activity` / `other` |
| Actor | Multi-select | `kennedy_direct` / `hhs_subagency` / `chd_org` / `state_official` / `dod_official` / `nominee` / `congressional_ally` / `other` |
| Sub-Actor | Text | Specific person or agency, e.g., `ACIP`, `FL DOH (Ladapo)`, `NIH`, `Tamasese (Samoa)` |
| Description | Rich text | Plain-language description of what happened |
| Mechanism | Rich text | Biological / epidemiological pathway from action to mortality. Example: `Reduced MMR coverage in target population → measles susceptibility → outbreak → measles deaths in unvaccinated children under 5` |
| Mechanism Tag | Multi-select | `coverage_decline` / `access_loss` / `surveillance_degradation` / `response_capacity_loss` / `treatment_disruption` / `disinformation_amplification` / `regulatory_withdrawal` / `program_elimination` / `other` |

### 3.3 Source / verification

| Field | Type | Notes |
|---|---|---|
| Source URL | URL | Primary source URL — must be specific page, not a homepage |
| Source Type | Select | `official_document` / `press_release` / `federal_register` / `court_filing` / `news_article` / `social_media` / `ngo_filing` / `congressional_record` / `peer_reviewed` / `other` |
| Source Authority Tier | Select | `1` (primary) / `2` (verified reporting / academic) / `3` (secondary analysis / advocacy / social) |
| Source Verification Date | Date | Last date URL was confirmed to resolve |
| Secondary Source URLs | URLs (multiple) | Corroborating sources, especially required when primary is Tier 3 |
| Sources Library | Relation to Sources Library DB | For sources used repeatedly across entries |

### 3.4 Affected population & geography

| Field | Type | Notes |
|---|---|---|
| Affected Population (text) | Rich text | Free-text description |
| Affected Population (relation) | Relation to Affected Populations DB | Reusable structured population definition |
| Geographic Scope | Multi-select | `federal` / `state` / `county` / `district` / `international` |
| State (relation) | Relation to MAHA Opps States DB (read-only) | When applicable |
| District (relation) | Relation to MAHA Opps Districts DB (read-only) | When applicable |
| Geographic Detail | Rich text | Free-text geographic specificity (e.g., `Samoa` / `Gaines County, TX (TX-19)` / `DoD active duty + dependents worldwide`) |
| Population Size (estimate) | Number | Best estimate of population at risk |
| Population Size Source | URL | Citation for population estimate |

### 3.5 Tier and assessment routing

| Field | Type | Options |
|---|---|---|
| Tier Candidate | Select | `Tier 1` / `Tier 2` / `Tier 3` / `Not Yet Determined` |
| Status | Select | `Candidate` / `Logged — No Mortality Pathway` / `Hold — Population` / `Hold — Data` / `Queued for Assessment` / `Under Assessment` / `Assessed` / `Published` / `Retracted` |
| Status Reason | Rich text | Required when Status is any `Hold` value or `Logged — No Mortality Pathway` |
| Edge Case Flag | Checkbox | True if action falls under Research Protocol Section 2.3 edge cases |
| Edge Case Type | Select | `swing_vote` / `mixed_motivation` / `international` / `allied_actor` / `other` |
| Priority | Select | `High` / `Medium` / `Low` — for assessment queue ordering |

### 3.6 Attribution chain (for influence-based actions)

| Field | Type | Notes |
|---|---|---|
| Attribution Chain | Rich text | Required for actions tied to Kennedy via influence rather than direct act. Document each link in the chain (Kennedy → CHD → state actor → outcome) with citations |
| Attribution Strength | Select | `Direct` (Kennedy or HHS act) / `Strong` (CHD act with documented Kennedy direction) / `Documented influence` (state actor with multiple documented Kennedy/CHD ties) / `Allied actor` (network member acting in coordination) |
| Attribution Sources | URLs (multiple) | Sources that establish the chain (separate from action source) |

### 3.7 Cross-database relations

| Field | Type | Notes |
|---|---|---|
| Related Federal Policy Change | Relation to MAHA Opps Federal Policy Changes DB (read-only) | When this action is also logged there |
| Related State Legislation | Relation to MAHA Opps State Legislation DB (read-only) | Same |
| Related MAHA Connection | Relation to MAHA Opps MAHA Connections DB (read-only) | When the action is also Tier 1 or Tier 2 MAHA-tagged in MAHA Opps |
| Related Mortality Assessment | Relation to Mortality Assessments DB | The downstream assessment for this action, when one exists |
| Related Disease Tracker Entry | Relation to MAHA Opps Disease Tracker DB (read-only) | When action ties to a tracked disease event |

### 3.8 QC

| Field | Type | Notes |
|---|---|---|
| URL Verified | Checkbox | True if Source URL has been verified to resolve since last QC pass |
| Duplicate Check Performed | Checkbox | True after duplicate-check workflow |
| QC Notes | Rich text | Reviewer notes |
| Protocol Version at Capture | Text | Records which version of the Research Protocol governed the entry (e.g., `v1.0`) |

---

## 4. Views

| View Name | Filter | Sort | Purpose |
|---|---|---|---|
| All Candidates | Status = `Candidate` | Captured Date desc | Triage queue |
| Held — Population | Status = `Hold — Population` | Last Reviewed asc | Reopen when new population data found |
| Held — Data | Status = `Hold — Data` | Last Reviewed asc | Reopen when new data sources identified |
| Queued for Assessment | Status = `Queued for Assessment` | Priority desc, Date asc | Pipeline to Mortality Assessment |
| Assessed (not yet published) | Status = `Assessed` | Captured Date desc | Editorial review queue |
| Published | Status = `Published` | Date desc | Public-facing inventory |
| By Type | Group by Type | Date desc | Coverage check across action types |
| By Geographic Scope | Group by Geographic Scope | Date desc | Geographic coverage check |
| Recent Captures (30 days) | Captured Date in last 30 days | Captured Date desc | Weekly synthesis pass |
| URL Re-verification Queue | URL Verified = false OR Source Verification Date > 30 days old | Source Verification Date asc | Monthly QC |
| Edge Cases | Edge Case Flag = true | Date desc | Monthly review |
| Retracted | Status = `Retracted` | Captured Date desc | Retraction log |

---

## 5. Templates

When creating a new entry, Notion offers templates pre-populated with required fields and helper text:

### 5.1 Template: HHS Official Action
- Type: `regulatory_action` (default; change as needed)
- Actor: `hhs_subagency` (default)
- Source Type: `federal_register` or `press_release` (prompt)
- Mechanism placeholder: `Describe biological or epidemiological pathway from this regulatory action to potential mortality outcomes.`

### 5.2 Template: Public Statement / Communication
- Type: `communication`
- Actor: `kennedy_direct` (default)
- Source Type: `press_release` or `social_media`
- Mechanism placeholder: `For statements, mortality pathway typically operates through measurable downstream effect on health behavior or coverage. Document the linkage with citations.`
- **Note**: communications often fail the eligibility gates without measurable downstream effect. Default Status: `Hold — Data` until reach/effect is documented.

### 5.3 Template: CHD Activity
- Type: `CHD_activity`
- Actor: `chd_org`
- Attribution Chain placeholder: `Document Kennedy's role in or direction of this CHD activity if applicable, or note that CHD acted independently of direct Kennedy involvement.`

### 5.4 Template: State Proxy Action
- Type: `state_proxy`
- Actor: `state_official`
- Attribution Chain: REQUIRED. State actor connection to Kennedy/CHD must be documented (campaign contributions, joint appearances, public endorsements, shared funding sources).
- Attribution Strength prompt: must specify.

### 5.5 Template: Clinical Trial Termination
- Type: `clinical_trial_action`
- Actor: `hhs_subagency` (typically NIH)
- Mechanism placeholder: `Counterfactual mortality among trial cohort or future patient population.`
- Required: NCT identifier in Description field.

### 5.6 Template: Pre-HHS / Samoa-style action
- Type: `CHD_activity` or `communication`
- Actor: `kennedy_direct` and/or `chd_org`
- Edge Case Flag: TRUE
- Attribution Chain: REQUIRED. Document the mechanism (platform-driven coverage decline) and how it parallels current federal-tenure mechanisms.

---

## 6. Required-field validation

The following fields are blocking — an entry cannot move out of `Candidate` status without them populated:

- ID (auto)
- Action Name
- Date
- Captured By
- Type
- Actor
- Description
- Mechanism (or `n/a` with reason)
- Source URL
- Source Type
- Source Authority Tier
- Source Verification Date
- Geographic Scope
- URL Verified = true

For status `Queued for Assessment`, additionally required:
- Mortality Pathway populated (cannot be `n/a`)
- Affected Population (text or relation)
- Tier Candidate

For Tier 3 sources, additionally required:
- Secondary Source URLs (≥1 corroborating Tier 1 or 2 source)

---

## 7. Relations to other databases

### 7.1 Within MAHA Mortality Tracker (writable)
- `Affected Populations` — many-to-many (a population may be referenced by many actions)
- `Mortality Assessments` — one-to-one (an action has at most one canonical assessment; assessments may be revised in version history)
- `Sources Library` — many-to-many
- `Methodology Notes` — many-to-many

### 7.2 To MAHA Opps Tracker (read-only)
- `States` — many-to-many
- `Districts` — many-to-many
- `Federal Policy Changes` — one-to-many (a federal action may map to multiple Registry entries if mortality pathways differ)
- `State Legislation` — same
- `MAHA Connections` — many-to-many
- `Disease Tracker` — many-to-many

The Registry never writes to MAHA Opps databases.

---

## 8. Retraction handling

When an entry must be retracted (factual error, source withdrawal, etc.):
1. Set `Status = Retracted`.
2. Populate `QC Notes` with reason and date.
3. If the entry was already `Published`, retraction also propagates to Public Site Entries DB and triggers a public correction (workflow defined in Mortality Assessment Protocol).
4. The entry ID is **not reused** — the retracted record stays as a permanent log.

---

## 9. Schema versioning

Schema changes follow the same versioning as the Research Protocol:
- **Major** (v1 → v2): Field removals, type changes, view restructures.
- **Minor** (v1.0 → v1.1): Field additions, new options in select fields.

Field history tracked in this document under Section 11.

---

## 10. Implementation notes (for setup)

When creating the Notion database:
1. Create database under MAHA Mortality Tracker parent page.
2. Add fields per Section 3 in order.
3. Configure relations to MAHA Opps databases (read-only). In Notion, this means relations are added without the reverse-relation enabled, and the Mortality Tracker side never edits the linked MAHA Opps entries directly.
4. Configure templates per Section 5.
5. Configure views per Section 4.
6. Save data source ID for use in scripts and reference docs.
7. Add database ID to project reference doc (`reference_notion_databases.md` in user memory).

Manual setup is fine for v1. Automation (Notion API for entry creation) can be built later if cadence requires it.

---

## 11. Schema version history

| Version | Date | Changes |
|---|---|---|
| v1.0 DRAFT | 2026-04-26 | Initial schema. 8 field groups, 12 views, 6 entry templates. Federated relations to MAHA Opps Tracker (read-only). |

---

*End of Action Registry Schema v1.0 DRAFT.*
