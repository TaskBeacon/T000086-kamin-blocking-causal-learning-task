# Task Logic Audit

## 1. Paradigm Intent

- Task: Kamin Blocking and Causal Learning Task, additive forward-blocking food-allergy variant.
- Primary construct: cue competition in human causal learning; reduced causal attribution to redundant cue B after A+ then AB+.
- Manipulated factors: phase, elemental versus compound food cues, outcome magnitude (none/allergic/strong allergic), cue role (blocking/blocked/control/filler).
- Dependent measures: prediction accuracy/RT during learning; 0–8 causal ratings; primary blocking score = mean(C,D) − B.
- Key citations: `W2058498316` primary protocol; `W1981033617` matched within-subject blocking logic; `W2024675017` learned-inattention interpretation; `W2154904563` cue-competition construct.

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: five sequential phases (four learning phases plus causal test).
- Trials per block: 16, 6, 15, 21, and 8; total 66 including test.
- Randomization/counterbalancing: exact condition counts are independently shuffled within each phase using the task seed; food-to-role assignments rotate deterministically by participant number.
- Condition weight policy: unequal exact counts are defined in `task.phase_trials`; `task.condition_weights` is omitted because label weights cannot enforce phase boundaries and exact per-phase totals.
- Condition generation method: custom precompiled `TrialPlan` lists are passed to `BlockUnit.add_condition`. Simple global label scheduling is insufficient because the cited procedure has fixed sequential phases, different admissible conditions per phase, and unequal exact counts within each phase.
- Generated condition shape: immutable plan with `condition_id`, `stage`, cue roles, participant-facing food labels, outcome, repetition, and test flag.
- Runtime-generated trial values: none. `run_trial.py` only realizes the supplied plan.

### Trial State Machine

1. `prediction`
   - Onset trigger: phase-specific prediction trigger.
   - Stimuli shown: meal heading, one centered food or two horizontally separated foods, and three-choice response prompt.
   - Valid keys: `1`, `2`, `3`.
   - Timeout behavior: record missing response and continue to feedback.
   - Next state: `feedback`.
2. `feedback`
   - Onset trigger: outcome-specific trigger.
   - Stimuli shown: the same food cue(s) plus green single-box “no reaction,” red single-box “allergic reaction,” or red double-box “strong allergic reaction.”
   - Valid keys: none.
   - Timeout behavior: fixed-duration offset.
   - Next state: `iti`.
3. `causal_rating` (test trials only, replaces prediction/feedback)
   - Onset trigger: causal-rating trigger.
   - Stimuli shown: one food and anchored 0–8 likelihood scale.
   - Valid keys: `0`–`8`.
   - Timeout behavior: record missing rating and continue.
   - Next state: `iti`.
4. `iti`
   - Onset trigger: ITI trigger.
   - Stimuli shown: blank white screen.
   - Valid keys: none.
   - Timeout behavior: fixed-duration offset.
   - Next state: next trial or phase transition.

## 3. Condition Semantics

- Pretraining elements: `pre_i_pos`, `pre_j_pos`, `pre_k_none`, `pre_l_none` teach two causal and two noncausal foods.
- Pretraining compounds: `pre_ij_strong` demonstrates additive magnitude; `pre_jk_pos` and `pre_kl_none` demonstrate mixed and noncausal compounds.
- Element phase: `a_pos` establishes blocking cue A; `e_pos_element`, `f_none_element`, `gh_none_element` maintain discriminative filler structure.
- Compound phase: `ab_pos` is the blocking trial; `cd_pos` is its novel-cue control; `e_pos_compound`, `f_none_compound`, `gh_none_compound` prevent an “all compounds cause allergy” rule.
- Test: `test_a` through `test_h` obtain individual causal ratings; B is compared against C and D.
- Participant-facing source: food names and all wording are in `config/*.yaml`; plans carry formatted labels from config only.
- Localization: swapping config labels/instructions changes language without editing Python trial logic.

## 4. Response and Scoring Rules

- Prediction mapping: config defines `1=no reaction`, `2=allergic reaction`, `3=strong allergic reaction`.
- Causal rating mapping: config defines numeric keys `0`–`8` with anchors 0 definitely not, 4 possibly, 8 definitely would.
- Missing-response policy: log timeout/missing; still reveal the learning outcome; causal-test timeout remains missing.
- Correctness logic: prediction key equals the outcome’s configured key; causal ratings have no correct answer.
- Reward/penalty: none.
- Running metrics: prediction accuracy; B rating; control mean of C/D; blocking score control mean minus B.

## 5. Stimulus Layout Plan

- Instruction/phase screens: one centered text block, `pos [0,0]`, height 0.58–0.64 deg, wrap width 24 deg.
- Single-food prediction: heading at `[0,4.2]`, food card centered `[0,1.2]`, prompt `[0,-3.2]`; vertical gaps exceed 2 deg.
- Compound prediction: heading `[0,4.2]`, left/right food cards at `[-4.2,1.2]` and `[4.2,1.2]`, prompt `[0,-3.2]`; cards have 6.2 deg separation between inner edges.
- Feedback: food layout unchanged; outcome box at `[0,-2.5]`; strong outcome uses two nested red rectangles.
- Causal test: food at `[0,2.2]`, question at `[0,-0.2]`, 0–8 scale at `[0,-2.5]`; anchored scale stays within 24 deg wrap width.
- QA and final plot are used to check overlap, readable scale, and correct single/compound proportions.

## 6. Trigger Plan

- 1 experiment start; 10/11 block start/end.
- 20/21/22/23 prediction onset for the four learning phases.
- 30/31/32 prediction response for none/allergy/strong; 33 prediction timeout.
- 40/41/42 feedback onset for none/allergy/strong.
- 50 causal-rating onset; 50–58 rating response codes are represented as 60–68 to avoid collision; 69 rating timeout.
- 80 ITI; 98 experiment end; 99 block end.

## 7. Architecture Decisions (Auditability)

- `main.py`: one mode-aware flow with a small `_run_block` helper; phase order remains explicit.
- `utils.py`: yes, only for immutable plan construction, deterministic within-phase shuffling, participant counterbalancing, and summary computation.
- Custom controller: no.
- Legacy/backward-compatibility fallback logic: no.

## 8. Inference Log

- Prediction deadline: primary protocol was participant-paced and reports no deadline; 10 s is a conservative safety bound for automated operation.
- Feedback duration: food-allergy paper specifies content but not duration; 2 s is adapted from the cited Chapman–Robbins human blocking procedure.
- ITI: primary protocol omits it; 0.5 s is a conservative separation used in related human allergist tasks.
- Input device: mouse buttons are adapted to keyboard keys while preserving all response alternatives and scale values.
- Fixed visual styling: outcome color/box conventions are direct, while sizes/positions are inferred for 1280×800 legibility.
- QA/simulation profiles: one repetition of every condition (24 trials) is used for mechanism-complete smoke testing; the human profile retains all cited repetitions.
