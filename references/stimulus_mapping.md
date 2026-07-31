# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `pre_i_pos` | pretraining_element | `food_single`, `prediction_prompt`, `outcome_allergy` | cheese; predict reaction; allergic reaction in red box | `W2058498316` | Procedure and Table 2: I+ (4) | `psychopy_builtin` | n/a | Food role counterbalanced. |
| `pre_j_pos` | pretraining_element | `food_single`, `prediction_prompt`, `outcome_allergy` | ham; predict reaction; allergic reaction in red box | `W2058498316` | Procedure and Table 2: J+ (4) | `psychopy_builtin` | n/a | Food role counterbalanced. |
| `pre_k_none` | pretraining_element | `food_single`, `prediction_prompt`, `outcome_none` | pears; predict reaction; no reaction in green box | `W2058498316` | Procedure and Table 2: K− (4) | `psychopy_builtin` | n/a | Food role counterbalanced. |
| `pre_l_none` | pretraining_element | `food_single`, `prediction_prompt`, `outcome_none` | bread; predict reaction; no reaction in green box | `W2058498316` | Procedure and Table 2: L− (4) | `psychopy_builtin` | n/a | Food role counterbalanced. |
| `pre_ij_strong` | pretraining_compound | `food_left`, `food_right`, `prediction_prompt`, `outcome_strong` | cheese + ham; strong allergic reaction in double red box | `W2058498316` | Procedure and Table 2: IJ++ (2) | `psychopy_builtin` | n/a | Additivity demonstration. |
| `pre_jk_pos` | pretraining_compound | `food_left`, `food_right`, `prediction_prompt`, `outcome_allergy` | ham + pears; allergic reaction | `W2058498316` | Procedure and Table 2: JK+ (2) | `psychopy_builtin` | n/a | One causal plus one noncausal cue. |
| `pre_kl_none` | pretraining_compound | `food_left`, `food_right`, `prediction_prompt`, `outcome_none` | pears + bread; no reaction | `W2058498316` | Procedure and Table 2: KL− (2) | `psychopy_builtin` | n/a | Two noncausal cues. |
| `a_pos` | element | `food_single`, `prediction_prompt`, `outcome_allergy` | yogurt; allergic reaction | `W2058498316` | Procedure and Table 2: A+ (6) | `psychopy_builtin` | n/a | Blocking cue. |
| `e_pos_element` | element | `food_single`, `prediction_prompt`, `outcome_allergy` | walnuts; allergic reaction | `W2058498316` | Procedure and Table 2: E+ (3) | `psychopy_builtin` | n/a | Filler. |
| `f_none_element` | element | `food_single`, `prediction_prompt`, `outcome_none` | noodles; no reaction | `W2058498316` | Procedure and Table 2: F− (3) | `psychopy_builtin` | n/a | Filler. |
| `gh_none_element` | element | `food_left`, `food_right`, `prediction_prompt`, `outcome_none` | oranges + chicken; no reaction | `W2058498316` | Procedure and Table 2: GH− (3) | `psychopy_builtin` | n/a | Compound filler prevents simple rules. |
| `ab_pos` | compound | `food_left`, `food_right`, `prediction_prompt`, `outcome_allergy` | yogurt + mushrooms; allergic reaction | `W2058498316` | Procedure and Table 2: AB+ (6) | `psychopy_builtin` | n/a | B is the blocked target. |
| `cd_pos` | compound | `food_left`, `food_right`, `prediction_prompt`, `outcome_allergy` | carrots + grapes; allergic reaction | `W2058498316` | Procedure and Table 2: CD+ (6) | `psychopy_builtin` | n/a | C/D are within-subject controls. |
| `e_pos_compound` | compound | `food_single`, `prediction_prompt`, `outcome_allergy` | walnuts; allergic reaction | `W2058498316` | Procedure and Table 2: E+ (3) | `psychopy_builtin` | n/a | Filler continued across phases. |
| `f_none_compound` | compound | `food_single`, `prediction_prompt`, `outcome_none` | noodles; no reaction | `W2058498316` | Procedure and Table 2: F− (3) | `psychopy_builtin` | n/a | Filler continued across phases. |
| `gh_none_compound` | compound | `food_left`, `food_right`, `prediction_prompt`, `outcome_none` | oranges + chicken; no reaction | `W2058498316` | Procedure and Table 2: GH− (3) | `psychopy_builtin` | n/a | Filler continued across phases. |
| `test_a` | causal_test | `food_single`, `causal_prompt` | rate yogurt from 0 to 8 | `W2058498316` | Postexperiment causal rating task A–H | `psychopy_builtin` | n/a | No outcome feedback. |
| `test_b` | causal_test | `food_single`, `causal_prompt` | rate mushrooms from 0 to 8 | `W2058498316` | Primary blocked-cue rating | `psychopy_builtin` | n/a | Primary blocked target. |
| `test_c` | causal_test | `food_single`, `causal_prompt` | rate carrots from 0 to 8 | `W2058498316` | Control-cue rating | `psychopy_builtin` | n/a | Control comparator. |
| `test_d` | causal_test | `food_single`, `causal_prompt` | rate grapes from 0 to 8 | `W2058498316` | Control-cue rating | `psychopy_builtin` | n/a | Control comparator. |
| `test_e` | causal_test | `food_single`, `causal_prompt` | rate walnuts from 0 to 8 | `W2058498316` | Postexperiment causal rating task A–H | `psychopy_builtin` | n/a | Filler rating. |
| `test_f` | causal_test | `food_single`, `causal_prompt` | rate noodles from 0 to 8 | `W2058498316` | Postexperiment causal rating task A–H | `psychopy_builtin` | n/a | Filler rating. |
| `test_g` | causal_test | `food_single`, `causal_prompt` | rate oranges from 0 to 8 | `W2058498316` | Postexperiment causal rating task A–H | `psychopy_builtin` | n/a | Filler rating. |
| `test_h` | causal_test | `food_single`, `causal_prompt` | rate chicken from 0 to 8 | `W2058498316` | Postexperiment causal rating task A–H | `psychopy_builtin` | n/a | Filler rating. |
