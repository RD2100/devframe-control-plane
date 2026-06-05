HANDOFF.md — DevFrame Control Plane v0.1.0-rc

Purpose of this document:
This handoff is for a new GPT conversation or new agent with zero prior knowledge of the DevFrame Control Plane project. It is self-contained. The recipient should be able to understand the project identity, architecture, completed phases, safety boundaries, current state, and recommended next actions without reading any prior chat history.

1. Project Identity
1.1 Project Name

DevFrame Control Plane

1.2 Repository

Primary repository:

https://github.com/RD2100/devframe-control-plane

Related ecosystem repository:

https://github.com/RD2100/dev-frame-opencode
1.3 Project Role

DevFrame Control Plane is the workflow integration layer for the broader dev-frame-opencode ecosystem.

It was created to solve a structural problem discovered in earlier multi-phase agent workflows:

The project had many working components — evidence pack builder, guards, CDP submitter, route files, ledgers, review prompts, closure packs — but they were scattered across scripts and conversations. The workflow depended too heavily on human memory and GPT session context.

DevFrame Control Plane turns those scattered components into a coherent, portable, evidence-first workflow framework.

1.4 Core Problem Solved

Before this project, the workflow looked like this:

human remembers context
↓
human tells agent what to do
↓
agent executes
↓
human asks GPT to review
↓
GPT accepts/blocks
↓
human manually decides next step

This was functional but fragile. If a GPT conversation or agent session lost context, the workflow became hard to restart.

DevFrame Control Plane changes that into:

pipeline definition
↓
runner
↓
evidence pack
↓
submission adapter
↓
GPT/CDP review
↓
parse result
↓
state and safety checks
↓
closure

The project goal is not simply automation. The goal is controlled automation with evidence, state, safety gates, and reproducible handoff.

2. Architecture

DevFrame Control Plane is built around a declarative, YAML-driven pipeline model.

At a high level:

Pipeline Spec
   ↓
Runner
   ↓
State Machine / Safety Checks
   ↓
Evidence / Handoff / Submission Adapters
   ↓
CDP / GPT Interaction
   ↓
Captured Reply
   ↓
SHA256 + Parse
   ↓
Closure Evidence
2.1 Pipeline Spec

The pipeline spec defines stages such as:

YAML
stages:
  - authorization
  - execution
  - closure
  - audit
  - context_handoff

It declares:

stage id

stage type

dependencies

expected review mode

evidence requirements

safety boundaries

whether external submission is allowed

The pipeline spec is validated by schema files created during G1.

2.2 Runner

The runner reads the pipeline file and performs dry-run or controlled execution.

Current runner capabilities include:

parse pipeline YAML

validate basic schema expectations

print stage sequence

support dry-run execution

optionally trigger dry-run submission adapter per review stage

integrate with CLI

The runner is intentionally conservative. It does not mutate state by default.

2.3 State Machine

The state machine guards project state and prevents unsafe stage progression.

Key responsibilities:

ensure authorization precedes execution

ensure closure follows execution

prevent unauthorized state mutation

preserve blocked item boundaries

fail-closed on missing or inconsistent evidence

The state machine is one of the reasons guard_removal_approved and evidence_cleanup_approved remain false.

2.4 Submission Adapter

The submission adapter abstracts the idea of sending a review pack.

It supports dry-run behavior and structured submission results.

It separates:

runner logic
from
submission mechanism

This makes it possible to test pipelines without actually submitting to GPT.

2.5 CDP Adapter

The CDP adapter provides the controlled interface for Chrome DevTools Protocol workflows.

It supports safe modes such as:

dry_run

not_configured

unavailable

It is designed to avoid accidental live submission.

2.6 Playwright Bridge

The Playwright bridge is the optional layer that enables browser interaction through CDP when explicitly authorized.

Important properties:

Playwright is optional.

Live CDP is disabled by default.

Live behavior requires explicit safety flags.

No cookies, sessions, or browser profiles may be exported.

No state mutation is allowed without separate authorization.

2.7 Context Handoff Generator / Verifier

The handoff system solves the “new conversation has no memory” problem.

It supports:

generating a self-contained handoff document

validating the handoff document

submitting the handoff to a new conversation in dry-run or live mode

capturing the new conversation’s bootstrap reply

parsing whether the new conversation understood the context

failing closed if understanding is not verified

This was standardized in G8A and extended in T1/T2.

2.8 CLI

The CLI provides user-facing entry points.

Verified commands include:

Bash
devframe doctor
devframe init
devframe run
devframe handoff generate
devframe handoff validate
devframe handoff bootstrap --dry-run

The CLI is part of H1 productization and T1 context sync.

2.9 YAML-Driven Model

The project is designed around this principle:

Workflows should be declared, validated, and executed through structured files, not remembered from chat history.

Core configuration and state files include:

CURRENT_STATE.yaml
CURRENT_ROUTE.json
NEXT_TASK.md
PHASE_LEDGER.md
SAFETY_BOUNDARIES.md
PIPELINE.yaml
EVIDENCE_SPEC.yaml
HANDOFF.md
3. Completed Work

This section summarizes all major phases.

G-Series: Control Plane Foundation and Live CDP Verification
G0 — Bootstrap Skeleton

Status: accepted

G0 created the project’s cold-start skeleton.

Delivered:

README

QUICKSTART

PROJECT_BOOTSTRAP

CURRENT_STATE

NEXT_TASK

SAFETY_BOUNDARIES

PHASE_LEDGER

EVIDENCE_INDEX

docs directory

code_project template

paper_iteration template

examples

.gitignore

.env.example

Key lesson:

The project must be understandable from repository files, not from GPT chat history.

G1 — Schema Design

Status: accepted

G1 defined the project’s schema foundation.

Delivered:

pipeline schema

state transition schema

evidence spec schema

pipeline spec documentation

Key lesson:

Pipelines must be declared and validated before execution.

G2 — Runner Skeleton

Status: accepted after verification-only evidence

G2 implemented the initial dry-run runner.

Capabilities:

parse pipeline files

validate pipeline structure

print stage sequence

verify current state alignment

avoid state mutation

Key issue encountered:

evidence packs repeatedly included stale failing test output

resolved by clean verification-only evidence

Key lesson:

Closure evidence must reflect actual current test output, not stale logs.

G3 — Submission Adapter

Status: accepted with external/GitHub verification logic

G3 introduced submission abstraction.

Capabilities:

submission request/result model

dry-run submission adapter

deterministic submission output

adapter interface for future CDP/live implementations

Key lesson:

Submission should be abstracted away from runner logic.

G4 — Runner + Adapter + CLI Dry-run Integration

Status: accepted

G4 connected runner and submission adapter.

Capabilities:

runner can trigger submission dry-run per review stage

CLI dry-run integration

authorization/closure stages can be simulated

no live CDP

no GPT submission

no state mutation

Key lesson:

Dry-run integration is necessary before any live CDP pilot.

G5 — CDP Adapter

Status: accepted_with_evidence_limitation

G5 created CDP adapter interface and safety modes.

Capabilities:

dry_run mode

not_configured mode

unavailable mode

safety guard structure

no Playwright required

no live CDP by default

Evidence limitation:

closure packs had formatting/path issues

functionality was accepted based on tests and implementation evidence

Key lesson:

Adapter safety must be designed before live browser execution.

G6 — Playwright Bridge

Status: accepted_with_evidence_limitation

G6 introduced optional Playwright/CDP bridge.

Capabilities:

optional Playwright import

live mode disabled by default

safety flag required for live behavior

fallback to dry-run/unavailable states

no automatic GPT submission

Evidence limitation:

closure evidence had formatting inconsistencies

accepted based on functional completion

Key lesson:

Live browser capability must remain behind explicit safety gates.

G7 — Mechanical CDP Pilot

Status: accepted

G7 performed the first mechanical CDP verification.

What G7 proved:

CDP connection worked

target page was found

bounded payload was inserted

send button was located

send button was not clicked

no real GPT submission occurred

no state mutation occurred

What G7 did not prove:

no GPT reply capture

no real review submission

no parse of GPT judgment

Key lesson:

First live CDP step should be mechanical only, not a full review pilot.

G8 — Bounded GPT Review Pilot

Status: accepted_with_audit_note

G8 performed the first true live CDP review-chain pilot.

What G8 proved:

CDP send
→ GPT reply capture
→ SHA256
→ YAML parse
→ REVIEW_RUN_ID match

G8 used a synthetic prompt only.

No real user data, private paper, or confidential material was submitted.

Audit note:

raw artifact hash and LF-normalized text hash differed due to newline normalization

future live captures should record both:

raw_artifact_sha256

normalized_text_sha256

Key lesson:

For captured GPT replies, hash policy must distinguish raw artifact bytes from normalized text.

G8A — Context Handoff Protocol

Status: accepted

G8A standardized new-conversation context transfer.

Delivered:

docs/context-handoff-protocol.md

HANDOFF template

bootstrap prompt template

context handoff schema

G8 handoff example

bootstrap reply example

tests

Key lesson:

New GPT conversations have no memory. Context must be transferred through a structured handoff document.

H-Series: Productization, Integration, Governance, Templates
H1 — Productization

Status: accepted_with_evidence_limitation

H1 turned the project into a user-facing tool.

Capabilities verified:

devframe doctor → 9/9 PASS
devframe init → functional
devframe run → dry-run functional
tests → 43/43 PASS

Delivered or verified:

CLI entry point

install/setup support

doctor command

init command

dry-run command

GitHub main branch state

Evidence limitation:

some verification packs lacked tree snapshots or clean closure formatting

accepted based on functional, reproducible facts

Key lesson:

Productization must be evaluated by reproducible commands, not just closure pack formatting.

H2 — dev-frame-opencode Integration Design

Status: accepted

H2 designed how DevFrame Control Plane maps onto dev-frame-opencode.

Delivered:

integration design

pipeline mapping

dry-run example

no migration

no live batch CDP

no evidence cleanup

no guard removal

Key lesson:

Integration should start as design and dry-run mapping before touching historical project state.

H3 — Paper Template Test

Status: accepted

H3 verified the paper_iteration template.

Generated files include:

PAPER_PROFILE.yaml
PAPER_STATE.yaml
PAPER_NEXT_TASK.md
PAPER_LEDGER.md
PAPER_SAFETY.md
PAPER_REVIEW_SPEC.md

No real paper content was used.

Key lesson:

The framework can support non-code workflows such as academic writing, but real paper workflows require additional templates and safeguards.

H4 — Archive Governance

Status: accepted

H4 created a read-only evidence archive governance policy.

Allowed:

read evidence

index evidence

classify evidence

cross-reference evidence

monitor counts

Prohibited:

delete evidence

move evidence

rename evidence

cleanup evidence

overwrite historical evidence

Key lesson:

Archive governance is allowed; evidence cleanup remains prohibited.

H5 — Broader 2-Pack CDP Pilot

Status: deferred / optional / post-release hardening

H5 was proposed as a two-pack broader CDP pilot.

Recommended acceptable scope:

exactly 2 synthetic bounded packs

no real user data

capture reply for both

compute SHA256 for both

parse YAML for both

verify REVIEW_RUN_ID for both

no state mutation

no guard removal

no evidence cleanup

Current disposition:

H5 is not required for v0.1.0-rc completion. It is optional post-release hardening.

Important note:

Some prompt/reply-level H5 testing occurred, but no final accepted H5 verification pack was recorded in the main accepted release disposition. Treat H5 as optional unless a clean verification pack is provided.

H6 — Guard Retirement After Replacement Design

Status: accepted

H6 created a design-only policy for possible future guard retirement.

Important:

no guard was removed

no guard was weakened

guard_removal_approved remains false

Future guard retirement requires:

replacement
→ shadow-run
→ parity verification
→ fallback path
→ explicit retirement review

Key lesson:

Direct guard removal is prohibited. Only replacement-verified retirement may be considered in the future.

T-Series: Post-Release Context Sync Automation
T1 — Context Sync Dry-run

Status: accepted

T1 implemented dry-run context sync automation.

Capabilities:

devframe handoff generate
devframe handoff validate
devframe handoff bootstrap --dry-run

Verified:

55/55 tests passed

handoff generation works

handoff validation works

bootstrap dry-run works

handoff_verified gate works

no live CDP

no GPT submission

no state mutation

Key lesson:

Handoff automation must first be proven in dry-run before live CDP new conversation bootstrap.

T2 — Live New Conversation Bootstrap

Status: accepted_with_evidence_limitation

T2 demonstrated live CDP new-conversation bootstrap.

Verified chain:

devframe handoff generate
→ CDP new page / new conversation
→ paste handoff
→ send
→ GPT reply
→ capture SHA256
→ parse
→ handoff_verified=True

Important result:

A truly new ChatGPT conversation was used.

The new conversation confirmed understanding of project state and H5 safety boundaries.

This proves that context can be synchronized into a new conversation.

Evidence limitation:

formal closure evidence had parse/test formatting issues

accepted based on functional live bootstrap demonstration

Key lesson:

Automatic new-conversation context sync is now operational, but future T2-like closures should produce clean structured parse JSON and explicit EXIT: 0 test output.

4. Current State
4.1 Release
YAML
release: v0.1.0-rc
project: devframe-control-plane
status: released
feature_complete: true
live_cdp_verified: true
context_sync_verified: true
4.2 Test and Doctor Status
YAML
tests:
  latest_count: 55/55 PASS

doctor:
  latest_status: 9/9 PASS

Earlier release core also had:

YAML
core_tests:
  release_phase: 43/43 PASS

After T1/T2 context sync work, the test count increased to 55.

4.3 CURRENT_ROUTE / Blocked Items

Final route concept:

YAML
unlocked_items:
  production_promotion_approved: true
  broader_real_chain_testing_unblocked: true
  hardcoded_driver_replacement_approved: true

permanently_blocked_items:
  guard_removal_approved: false
  evidence_cleanup_approved: false

The two remaining blocked items are not unfinished tasks. They are long-term safety gates.

4.4 Final Blocked Item Disposition
YAML
guard_removal_approved:
  value: false
  final_disposition: permanently_blocked
  future_path: guard_retirement_after_replacement_only

evidence_cleanup_approved:
  value: false
  final_disposition: permanently_blocked
  future_path: archive_governance_only
5. Key Protocols
5.1 Evidence-First Workflow

The project follows Evidence-First review.

Meaning:

Do not accept agent claims without verifiable evidence.

Evidence may include:

test output

doctor output

captured GPT reply

SHA256

parse JSON

route state

safety attestation

tree snapshot

dry-run output

manifest verification

Rules:

YAML
evidence_first_rules:
  - agent summary is not enough
  - evidence pack must be internally consistent
  - stale failed logs must not be mixed with passing claims
  - hash values must match the artifact or clearly specify normalization
  - missing evidence leads to blocked or accepted_with_evidence_limitation
5.2 Authorization → Execution → Closure Cycle

Canonical phase structure:

authorization
↓
execution
↓
closure
Authorization

Defines:

what may be done

what is prohibited

expected evidence

safety boundaries

retry limits

fail-closed conditions

Execution

Performs only the authorized scope.

Closure

Submits evidence for review.

Closure should include:

result summary

tests

safety attestation

relevant output

parse/hash evidence when applicable

5.3 CDP Submission via Playwright

CDP live behavior is always controlled.

Required principles:

YAML
cdp_safety:
  live_disabled_by_default: true
  explicit_safety_flag_required: true
  no_cookie_export: true
  no_session_export: true
  no_browser_profile_export: true
  no_real_user_data_by_default: true
  fail_closed_on_uncertainty: true

G7 verified mechanical CDP interaction.

G8 verified real send/capture/hash/parse.

T2 verified new conversation bootstrap through CDP.

5.4 Context Handoff Protocol

Context Handoff Protocol solves new conversation memory loss.

Standard flow:

generate HANDOFF.md
↓
validate handoff
↓
open / target new conversation
↓
submit handoff
↓
capture bootstrap reply
↓
parse handoff verification
↓
proceed only if handoff_verified=true

The recipient GPT must confirm:

YAML
handoff_understood: yes
current_status_understood: yes
safety_boundaries_understood: yes
next_task_understood: yes

If not, fail closed.

6. Safety Boundaries
6.1 Permanently Prohibited in This Release Line

The following must not be done as ordinary tasks:

YAML
permanently_prohibited:
  - direct guard removal
  - evidence cleanup
  - deleting evidence
  - moving evidence
  - renaming evidence
  - overwriting historical evidence
  - weakening submission guards
6.2 Requires Separate Authorization

The following require explicit separate authorization:

YAML
requires_separate_authorization:
  - live CDP execution
  - GPT submission
  - state mutation
  - CURRENT_ROUTE modification
  - CURRENT_STATE modification
  - DECISION_LEDGER write
  - multi-pack live CDP pilot
  - real user data processing
  - private paper processing
  - guard retirement-after-replacement review
6.3 Always Prohibited Unless Explicitly Scoped
YAML
sensitive_data_prohibited:
  - cookies
  - session tokens
  - browser profile export
  - API keys
  - real private manuscripts
  - confidential user files
  - hidden browser credentials
6.4 Fail-Closed Conditions

The system or reviewer must fail closed on:

YAML
fail_closed_on:
  - review_unverified
  - REVIEW_RUN_ID mismatch
  - missing capture
  - empty capture
  - unparseable YAML
  - SHA256 mismatch without raw/normalized explanation
  - timeout after retries
  - unauthorized state mutation
  - guard removal attempt
  - evidence cleanup attempt
  - real user data detected
  - cookies/session/profile access
7. Repository Info
7.1 Main Repository
https://github.com/RD2100/devframe-control-plane
7.2 Ecosystem Repository
https://github.com/RD2100/dev-frame-opencode
7.3 File Structure Overview

Expected high-level layout:

devframe-control-plane/
  README.md
  QUICKSTART.md
  INSTALL.md
  PROJECT_BOOTSTRAP.md
  CURRENT_STATE.yaml
  NEXT_TASK.md
  PHASE_LEDGER.md
  SAFETY_BOUNDARIES.md
  EVIDENCE_INDEX.md

  control_plane/
    pipeline_runner.py
    pipeline_spec.py
    state_machine.py
    submission_adapter.py
    submission_result.py
    cdp_adapter.py
    playwright_bridge.py
    cli.py
    handoff_generator.py
    handoff_verifier.py
    conversation_bootstrap.py

  schemas/
    pipeline.schema.json
    state_transition.schema.json
    evidence_spec.schema.json
    context_handoff.schema.json

  docs/
    pipeline-spec.md
    context-handoff-protocol.md
    archive-governance.md
    cdp-adapter.md
    conversation-bootstrap.md
    h2-integration-design.md
    guard-retirement-design.md

  templates/
    code_project/
    paper_iteration/
    context_handoff/

  examples/
    minimal_code_project/
    context_handoff_g8/
    h2_integration/

  tests/
    test_pipeline_runner.py
    test_state_machine.py
    test_submission_adapter.py
    test_cdp_adapter.py
    test_context_handoff_schema.py
    test_handoff_generator.py
    test_handoff_verifier.py
    test_conversation_bootstrap_dry_run.py

  .github/
    workflows/
      ci.yml

  setup.py
  RELEASE_CHECKLIST.md

Note: exact filenames may vary slightly, but this is the conceptual layout.

8. Known Issues and Lessons Learned
8.1 Closure Evidence Formatting Pattern

Across several phases, especially G2, G5, G6, H1, and T2, closure packs sometimes had:

flattened paths

stale smoke files

manifest/zip count mismatch

stale failing test logs

route labels still saying authorization_only

missing EXIT: 0

raw hash vs normalized text hash confusion

This caused repeated blocked reviews.

Lesson:

For future closure packs, prefer verification-only evidence packs with minimal, clean, current evidence.

Recommended minimal verification pack:

GITHUB_COMMIT.txt
TREE_SNAPSHOT.txt
TEST_OUTPUT.txt
DRY_RUN_OUTPUT.txt or EXECUTION_OUTPUT.txt
SAFETY_ATTESTATION.md
8.2 accepted_with_evidence_limitation

Some phases were accepted despite imperfect closure evidence because functionality was sufficiently demonstrated.

Known phases:

YAML
accepted_with_evidence_limitation:
  G5: CDP adapter
  G6: Playwright bridge
  G8: bounded GPT review pilot with hash normalization audit note
  H1: productization
  T2: live new conversation bootstrap

Meaning:

The functional capability was accepted, but future audit should remember that closure evidence formatting was imperfect.

8.3 Max-2 Iteration Policy

To avoid infinite evidence formatting loops, a policy was introduced:

YAML
max_closure_iterations: 2

Interpretation:

If the core functionality is verified and remaining issues are formatting-only, accept_with_evidence_limitation may be appropriate.

If the core evidence is wrong, such as failed tests or hash mismatch without explanation, do not accept.

If a phase is safety-critical, do not let iteration fatigue override Evidence-First principles.

8.4 Raw vs Normalized Hash Rule

G8 exposed newline normalization issues.

Future live capture evidence should record both:

YAML
hashes:
  raw_artifact_sha256: "<hash of exact file bytes>"
  normalized_text_sha256: "<hash of normalized text used for parse>"

This prevents false hash mismatch disputes.

9. Recommended Next Steps

The project is released and feature-complete. The next phase should be post-release enhancement, not core completion.

9.1 Recommended T3
YAML
T3:
  name: "Auto New Conversation Handoff — Clean Evidence and Release Integration"
  type: "post-release hardening"
  goal: "turn T1/T2 context sync into a polished user-facing workflow"

Suggested T3 actions:

Add clear documentation:

docs/auto-new-conversation-context-sync.md

Ensure CLI help covers:

Bash
devframe handoff generate
devframe handoff validate
devframe handoff bootstrap --dry-run

Add a design-only path for:

Bash
devframe handoff bootstrap --live-cdp --safety-flag

Add verification output format:

HANDOFF_VERIFICATION.json
BOOTSTRAP_REPLY.txt
BOOTSTRAP_REPLY.sha256

Formalize T2 evidence requirements:

YAML
required:
  - structured JSON parse
  - EXIT: 0 test output
  - no cookies/session/profile attestation
  - no state mutation attestation
9.2 Optional H5 Post-Release Hardening

H5 remains optional.

If pursued, it should be a new conversation with a strict scope:

YAML
H5:
  pack_count: exactly_2
  pack_type: synthetic_only
  target: bootstrapped_new_conversation
  required_per_pack:
    - submit
    - capture
    - sha256
    - parse
    - rid_match
  prohibited:
    - real_user_data
    - state_mutation
    - guard_removal
    - evidence_cleanup

H5 should not block release status.

9.3 Paper Workflow Expansion

A valuable future direction is to turn paper_iteration from an initialization template into a full academic writing workflow.

Potential phases:

YAML
paper_workflow_future:
  - paper review pipeline
  - CSSCI journal-fit review
  - thesis midterm review
  - versioned paper ledger
  - citation verification
  - context handoff for long writing sessions

Important:

Do not use real private paper content unless the user explicitly provides it and the workflow is scoped with confidentiality safeguards.

10. Expected Response Schema

The new GPT conversation or new agent receiving this handoff must confirm understanding using YAML only.

YAML
overall_judgment: accepted | blocked | review_unverified
handoff_understood: yes | no
project_identity_understood: yes | no
architecture_understood: yes | no
completed_phases_understood: yes | no
current_state_understood: yes | no
safety_boundaries_understood: yes | no
next_steps_understood: yes | no
ready_for_next_authorization: yes | no
rationale: "<brief explanation>"
Acceptance Conditions

The handoff is understood only if:

YAML
handoff_understood: yes
project_identity_understood: yes
architecture_understood: yes
completed_phases_understood: yes
current_state_understood: yes
safety_boundaries_understood: yes
next_steps_understood: yes
ready_for_next_authorization: yes
Fail-Closed Conditions

The new conversation or agent must return review_unverified or blocked if it:

cannot identify the project

does not understand completed phases

confuses H5 with required release work

suggests guard removal

suggests evidence cleanup

requests cookies/session/browser profile

suggests live CDP without separate authorization

requests real user data without explicit scoped permission

cannot distinguish accepted vs accepted_with_evidence_limitation phases

11. Final Status Summary
YAML
project: devframe-control-plane
release: v0.1.0-rc
feature_complete: true
live_cdp_verified: true
context_handoff_protocol: standardized
auto_context_sync:
  dry_run: verified
  live_bootstrap: demonstrated_with_evidence_limitation

tests:
  current_reported: 55/55 PASS

doctor:
  current_reported: 9/9 PASS

current_route:
  production_promotion_approved: true
  broader_real_chain_testing_unblocked: true
  hardcoded_driver_replacement_approved: true
  guard_removal_approved: false
  evidence_cleanup_approved: false

remaining_items:
  H5: optional_post_release_hardening
  T3: recommended_context_sync_polish
12. One-Sentence Summary

DevFrame Control Plane is a released v0.1.0-rc workflow control framework that converts scattered agent/GPT/CDP workflow components into a schema-driven, evidence-first, safety-gated, context-handoff-capable orchestration layer for dev-frame-opencode and future code or paper workflows.