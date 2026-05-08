# MAHA Mortality Tracker — Session Continuation Prompt

**Drafted:** 2026-04-27 — for use when continuing work on a new device or in a new Cowork project.

---

## Part 1 — Setup instructions (do these first on the new device)

### The simple path (iCloud-synced project folder — recommended)

The project folder `~/Documents/Claude/Projects/MAHA Opps Tracker/` is iCloud-synced, so on the new device the entire project — including this continuation prompt, all schema docs, the push script, and the GitHub PAT — is already there. No clone, no copy, no PAT regeneration needed.

**Steps on the new device:**

1. **Wait for iCloud to finish syncing.** Open Finder, navigate to `~/Documents/Claude/Projects/MAHA Opps Tracker/` and confirm you see the `MAHA Mortality Tracker/` subfolder, the `.gh_pat` file (it's hidden — press ⌘⇧. to show hidden files), and `push_to_github.py`. If you don't see them, give iCloud a few minutes.
2. **Create a new Cowork project** (suggested name: *MAHA Mortality Tracker*).
3. **Sign in to the Notion connector** with your Notion account (`angierasmussen@gmail.com`). All 7 mortality tracker databases will be accessible immediately — no per-database setup.
4. **Mount the iCloud folder** in the new Cowork project. Add `~/Documents/Claude/Projects/MAHA Opps Tracker/` (or just the `MAHA Mortality Tracker/` subfolder if you'd rather a tighter scope).
5. **Paste Part 2 of this doc into the project's instructions panel.** That gives the new session the full project context.
6. **Open a new chat and paste Part 3 as the first message.** That tells the new session to read this prompt, verify infrastructure access, and confirm the next-step decision.

That's it. Total time on the new device: ~3 minutes after iCloud has synced.

### The fallback path (iCloud not available, or you want a fresh PAT)

If iCloud isn't an option (different account, sync disabled, etc.) or you'd rather not have the PAT live in iCloud for security reasons, do this instead:

1. Create new Cowork project.
2. Sign in to Notion connector.
3. In Terminal:
   ```bash
   mkdir -p ~/Documents/Claude/Projects/"MAHA Mortality Tracker"
   cd ~/Documents/Claude/Projects/"MAHA Mortality Tracker"
   git clone https://github.com/a-rasmussen/maha-opps-tracker.git repo
   cp repo/mortality-tracker/push_to_github.py ./push_to_github.py
   ```
4. Generate a fresh fine-grained PAT for `a-rasmussen/maha-opps-tracker`:
   - https://github.com/settings/personal-access-tokens → Generate new (fine-grained)
   - Name: `Claude MAHA push (device 2)`
   - Resource owner: `a-rasmussen`
   - Repository access: "Only select repositories" → `maha-opps-tracker`
   - **Expand "Repository permissions"** (collapsed by default — this is the gotcha)
     - Contents: Read and write
     - Metadata: Read-only (auto)
   - Generate, copy the `github_pat_...` value
   - Save:
     ```bash
     echo 'github_pat_YOUR_TOKEN_HERE' > ~/Documents/Claude/Projects/"MAHA Mortality Tracker"/.gh_pat
     chmod 600 ~/Documents/Claude/Projects/"MAHA Mortality Tracker"/.gh_pat
     ```
5. Mount `~/Documents/Claude/Projects/MAHA Mortality Tracker/` in the new Cowork project.
6. Paste Part 2 into project instructions.
7. Use Part 3 as your first message.

### Security note on the iCloud path

Because the simple path puts `.gh_pat` (a fine-grained GitHub token) inside an iCloud-synced folder, the token is replicated to anywhere your iCloud account is signed in. Trade-off:
- **Pro:** zero-friction cross-device access, no token regeneration.
- **Con:** if your Apple ID is compromised, the GitHub PAT is exposed too. Mitigated by the PAT being fine-grained (read+write to one repo only — no broader account access) but worth knowing.
- If concerned, follow the fallback path and revoke the original PAT once the new device has its own.

---

## Part 2 — Project context (paste this into the Cowork project instructions)

### Project identity
- **Internal name:** MAHA Mortality Tracker
- **Public-facing site name:** Bobby Kennedy Jr. Body Count (working title; final review pending)
- **Owner:** Angie Rasmussen (`angierasmussen@gmail.com`)
- **Sister project:** MAHA Opps Tracker (independent; federated at database level only — Mortality Tracker does NOT write to MAHA Opps databases)
- **Phase:** Phase 0 (setup) complete as of 2026-04-27. Phase 1 (Mortality Assessment Protocol + Samoa methodology proving case) not yet started.

### What this project is
Estimates and reports mortality consequences attributable to actions by Robert F. Kennedy Jr., Children's Health Defense, allied state and federal officials, and HHS under Kennedy's leadership. Three-tier evidence framework. Aggregate counts only — no individual decedents named. Documented attribution chains. Public site presents counts with explicit tier, methodology, and source for every entry.

### Three-tier evidence framework (CRITICAL — every public count carries one)
- **Tier 1 — Documented causal chain.** Action documented; mechanism documented; affected population identified by name; deaths counted by official sources; chain defensible end-to-end without statistical inference. Example: Samoa 2019 measles outbreak, 83 deaths.
- **Tier 2 — Statistical attribution.** Action documented; mechanism documented at population level; excess mortality estimable via accepted epidemiological methods (counterfactual baseline) with confidence interval. Example: US measles deaths attributable to coverage decline; OBBBA Medicaid coverage-loss deaths.
- **Tier 3 — Projected mortality.** Action documented; mortality estimate from peer-reviewed forward-looking modeling; no retrospective deaths yet measurable; clearly labeled projected.

### Methodological commitments
1. Aggregate counts only. No named individual decedents.
2. Documented attribution chain. For influence-based actions (Kennedy → CHD → state actor → outcome), every link is documented with citations.
3. Eligibility gates before any action becomes a mortality count: (a) documentable causal mechanism, (b) definable affected population, (c) available data or model basis, (d) time window definable, (e) counterfactual specifiable.
4. Federated, not shared. Mortality Tracker does not write to MAHA Opps Tracker databases.
5. Tier discipline. Every public count carries tier + methodology link.
6. Sources at every step. Every data point links to a primary source. URLs verified before embedding and re-verified monthly.

### Resolved scope decisions (from v1.1)
- **Pre-HHS scope is BROAD.** Includes Samoa 2019, all CHD activity from CHD's founding (2018, rebranded from World Mercury Project), pre-CHD World Mercury Project (founded ~2007), and earlier Kennedy anti-vaccine writing/advocacy.
- **International scope IS IN.** Examples: CHD activity in low-coverage settings (Africa, Pacific, Europe), international conferences, international policy advocacy.
- **Substack monitoring is Claude-side** via site-restricted WebSearch (`site:substack.com "RFK Jr"` etc.), integrated into weekly synthesis. NOT user manual browsing.
- **Triggered-run latency:** within 48 hours of major events.
- **Registry vs. Assessment distinction.** Registry captures broadly; Assessment is gated by the five eligibility criteria. Many Registry entries stay as context without becoming mortality counts.

### Cadence
- Daily news scan (~15 min): Federal Register, HHS press, AP/Reuters/STAT, CIDRAP.
- Weekly synthesis (~1 hr): triage daily candidates, weekly source pass, Substack via WebSearch, LunarCrush sentiment.
- Monthly comprehensive (~half day): full source list, registry QC, held-item resolution, registry snapshot to GitHub.
- Triggered runs on major events.

### Notion infrastructure (all 7 DBs live)

**Parent page** (`34fb9126-7234-8132-82fb-d1befcb5ef37`): https://www.notion.so/34fb91267234813282fbd1befcb5ef37

| Database | Data Source ID (for API/MCP) | Page URL |
|---|---|---|
| Kennedy Action Registry | `24d2e420-e67b-4cd0-a07d-76500af40e72` | https://www.notion.so/6772d26e9ed24047bef0ba653b718e7c |
| Sources Library | `5ec90b0d-5f7c-46fa-9aec-b0222f0e0fbb` | https://www.notion.so/561328d0e6494a2691bfeff94234a863 |
| Affected Populations | `2df49cf1-c51c-4499-8c9c-fbb1408e22b1` | https://www.notion.so/68a53ea0499e4710a6144fc0be43b91e |
| Mortality Models | `e2e0dcc1-12fa-4c65-b73d-bb49cc5d601a` | https://www.notion.so/63af173b158e4e27ad72d40a7997529c |
| Methodology Notes | `5b56c17f-5167-41b7-9846-9b5ff5bb21f9` | https://www.notion.so/cda0a4d4a2a84d4ca2ab909eb878df98 |
| Mortality Assessments | `7c1ad756-552e-4023-a018-801a65be6241` | https://www.notion.so/baa3214569ce4dc98dfadcd32af2350b |
| Public Site Entries | `eae091eb-8d7e-4b82-9ae0-ef5afaba01e5` | https://www.notion.so/2e7c56204ec142539cac043319aacc24 |

**Read-only relations to MAHA Opps Tracker databases (federated):**

| MAHA Opps DB | Data Source ID |
|---|---|
| States | `ea0b4ffa-31f5-494c-96df-3855daab8d02` |
| Districts | `6f75352c-5d58-4f72-86cf-8c8fd9ec80b3` |
| Federal Policy Changes | `8d240e2d-df09-4a85-b3f3-bebb19b696ad` |
| State Legislation | `21fbfa22-4549-4a4f-8e2c-9cbdffdea1e2` |
| Disease Tracker | `494d1281-b008-4cee-93bf-697d30e6c4f3` |
| MAHA Connections | `06c950c7-9427-4ea4-93a1-b949df6e9ac1` |

### GitHub repo
**URL:** https://github.com/a-rasmussen/maha-opps-tracker
**Mortality tracker subfolder:** `mortality-tracker/`

**Files in repo:**
- `MAHA_Mortality_Tracker_Project_Instructions_v1.md` (v1.1 content)
- `Research_Protocol_v1.1.md`
- `Action_Registry_Schema_v1.md` (v1.1 content)
- `Other_Databases_Schemas_v1.0.md` (with live IDs)
- `Research_Protocol_Workflow_v1.0.svg`
- `Session_Continuation_Prompt.md` (this doc)

**Push workflow:** Use `push_to_github.py` script (in MAHA project root locally) with fine-grained PAT in `.gh_pat`. Never use the GitHub MCP write tools — they fail with `Bad credentials` / `Resource not accessible by personal access token`.

**Push command pattern:**
```bash
python3 ~/Documents/Claude/Projects/"MAHA Mortality Tracker"/push_to_github.py \
    --owner a-rasmussen --repo maha-opps-tracker \
    --source-dir ~/Documents/Claude/Projects/"MAHA Mortality Tracker"/repo/mortality-tracker \
    --repo-prefix mortality-tracker \
    --files file1.md file2.md \
    --message "commit message"
```

### Custom modeling architecture (planned, not yet built)
Five model families ranked by leverage:
1. Policy → coverage → outbreak mortality (SIR/SEIR adapted from IDM)
2. Coverage loss → mortality (extends KFF/CBPP/Penn LDI)
3. Outbreak response capacity (regression on staffing/funding)
4. Clinical trial termination mortality (per-trial counterfactual)
5. Hesitancy → coverage decline (Bayesian; adapt Larson et al. Vaccine Confidence Project)

Models 1 and 2 are v1 priorities. Owner designs methodology, implementation in Python via `idmtools`, `epimodel`, etc.

### Phased roadmap
- **Phase 0 — Setup.** ✅ DONE (2026-04-27). Project instructions, research protocol, schemas, Notion DBs, GitHub repo all live.
- **Phase 1 — Methodology proving case.** Two parallel tracks:
  - 1A. Mortality Assessment Protocol v0.1 (writing-heavy synthesis of decisions made).
  - 1B. Samoa 2019 Tier 1 case file (research-heavy: pull primary sources, document chain, populate Notion entries end-to-end).
  - Recommended order: 1A → 1B (so case file validates the methodology spec).
- **Phase 2 — Registry + first 10 assessments.** TX measles, ACIP MMRV, COVID vax recommendation, FL HepB, OBBBA Medicaid, DoW flu (Department of War — DoD renamed under Hegseth), 3 NIH trial halts, fluoride withdrawal.
- **Phase 3 — Public site launch.** Gated on legal review; hosting/attribution decision still open.
- **Phase 4 — Ongoing maintenance + model refinement.**

### Open project gates (need user decision before relevant phase)
1. **Hosting / public-site attribution** — your name / coalition site / shield org / pseudonymous. Affects legal target. Gates Phase 3.
2. **Coordinator role** — solo through Phase 2 or expand earlier?
3. **External methodology peer review** — who, when?
4. **Retraction / correction policy** — needs to be drafted before Phase 3.
5. **Domain name** — `bobbykennedyjrbodycount.org` and variants worth reserving early to prevent squatting.

### Where we left off (2026-04-27)
Phase 0 setup complete. Last conversation was about choice of Phase 1 next step:
- **Option A — Mortality Assessment Protocol v0.1 (writing-heavy).** Mostly synthesis. Defines per-tier methodology, counterfactual specification, CI standard, peer review workflow, retraction policy.
- **Option B — Samoa Tier 1 case file (research-heavy).** Build first real assessment end-to-end as the proving exercise.

Recommended order: A → B because the spec gaps will trip up Samoa work otherwise. User to confirm in new session.

### User context
- Virologist, 25 years' experience in host-pathogen interactions for emerging viruses.
- Co-Editor-in-Chief of *Vaccine*.
- Uses computational and AI approaches but does not code; methodology design is in scope, implementation is delegated/AI-assisted.
- Has ADHD. Communication preferences: direct and clear, no over-explaining or padding, flag problems early, friendly but not effusive, break complex tasks into clear steps with check-ins at decision points, don't ask multiple questions when a reasonable default with flag works, in-text scientific citation style with hyperlinks (not footnotes/endnotes), verify URLs by searching not from memory.
- Audience: public, journalists, policymakers, scientific community.

### Key documents to read at session start
1. `repo/mortality-tracker/MAHA_Mortality_Tracker_Project_Instructions_v1.md` — master doc, 18 sections.
2. `repo/mortality-tracker/Research_Protocol_v1.1.md` — surveillance / capture / triage workflow.
3. `repo/mortality-tracker/Action_Registry_Schema_v1.md` — schema for Kennedy Action Registry.
4. `repo/mortality-tracker/Other_Databases_Schemas_v1.0.md` — schemas for the other 6 DBs with live IDs.

---

## Part 3 — First-message template for the new session

Once Cowork is set up per Part 1 and Part 2 is in the project instructions, open a new chat and paste:

> Hi Claude — continuing the MAHA Mortality Tracker project on a new device.
>
> Please:
> 1. Read the continuation prompt. It's at one of these paths (iCloud path is primary; fallback path is the git clone):
>    - `~/Documents/Claude/Projects/MAHA Opps Tracker/MAHA Mortality Tracker/Session_Continuation_Prompt.md` (iCloud-synced — try this first)
>    - `~/Documents/Claude/Projects/MAHA Mortality Tracker/repo/mortality-tracker/Session_Continuation_Prompt.md` (fallback if I cloned the repo)
> 2. Verify Notion access by fetching the parent page (ID `34fb9126-7234-8132-82fb-d1befcb5ef37`).
> 3. Verify the GitHub push path works by listing files in the repo via `get_file_contents` and confirming `push_to_github.py` and `.gh_pat` exist locally.
> 4. Once verified, summarize the current project status and ask me whether we're starting Phase 1A (Mortality Assessment Protocol) or 1B (Samoa case file) first.

That's it. The new session should pick up cleanly.

---

## Part 4 — What does NOT transfer automatically

These are device-specific or session-specific and won't carry over:

- **Cowork auto-memory** (the per-project memory files in `~/Library/Application Support/Claude/...`). The Part 2 prompt is a hand-curated replacement for the most important memory entries.
- **Local working files** outside the GitHub repo. If you have unpushed local files in `~/Documents/Claude/Projects/MAHA Opps Tracker/MAHA Mortality Tracker/`, push them to GitHub before switching devices, or copy them manually. As of 2026-04-27, all canonical project files are in the repo.
- **Tab/conversation state.** Closed conversations don't transfer; the continuation prompt is the bridge.
- **TodoList state.** Tasks tracked via Cowork's task tools are session-scoped and won't carry over.

---

*End of continuation prompt.*
