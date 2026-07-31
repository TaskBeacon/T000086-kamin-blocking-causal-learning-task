# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| `variant` | `task.variant` | additive forward blocking | `W2058498316` | Experiment 1, Table 1 and Procedure | direct | Implements the additive group because demonstrated additivity strengthens blocking. |
| `phase_order` | `task.phase_order` | pretraining element → pretraining compound → element → compound → causal test | `W2058498316` | Experiment 1, Table 2 | direct | Forward order only; backward order is outside this baseline variant. |
| `pretraining_element_counts` | `task.phase_trials.pretraining_element` | I+, J+, K−, L− ×4 each | `W2058498316` | Experiment 1, Table 2 | direct | 16 trials. |
| `pretraining_compound_counts` | `task.phase_trials.pretraining_compound` | IJ++ / JK+ / KL− ×2 each | `W2058498316` | Experiment 1, Table 2 | direct | 6 trials; IJ++ directly demonstrates magnitude additivity. |
| `element_counts` | `task.phase_trials.element` | A+ ×6; E+, F−, GH− ×3 each | `W2058498316` | Experiment 1, Table 2 | direct | 15 trials. |
| `compound_counts` | `task.phase_trials.compound` | AB+, CD+ ×6; E+, F−, GH− ×3 each | `W2058498316` | Experiment 1, Table 2 | direct | 21 trials. |
| `training_total` | `task.total_training_trials` | 58 | `W2058498316` | Procedure: “At the end of all 58 trials” | direct | Exact human-profile total. |
| `test_scale` | `task.rating_keys` | 0–8 | `W2058498316` | Procedure: nine buttons, endpoints 0/4/8 | direct | Keyboard replaces mouse buttons while preserving the scale. |
| `food_sets` | `task.blocking_foods`, `task.pretraining_foods` | yogurt, mushrooms, carrots, grapes, walnuts, noodles, oranges, chicken; cheese, ham, pears, bread | `W2058498316` | Experiment 1 Procedure | direct | Chinese labels preserve the named food categories. |
| `prediction_keys` | `task.prediction_keys` | 1=no reaction, 2=allergic, 3=strong allergic | `W2058498316` | Additive group used a three-choice prediction format | adapted | Keyboard response substitutes for mouse selection. |
| `prediction_window` | `timing.prediction_window` | 10 s | `W2058498316`; `W1981033617` | Response was participant-paced; no deadline reported | inferred | Finite deadline supports unattended-session safety and simulation. |
| `feedback_duration` | `timing.feedback_duration` | 2 s | `W1981033617` | Accuracy feedback remained for 2 s | adapted | Food-allergy task reports feedback content but not duration. |
| `iti_duration` | `timing.iti_duration` | 0.5 s | `W2058498316` plus open human allergist-task practice | Trial separation not reported in primary source | inferred | Conservative fixed interval; separate from condition RNG. |
| `condition_generation` | `task.phase_trials` | exact counted plans shuffled within phase | `W2058498316` | Table 2: trial types intermixed within phase | adapted | Custom precompiled plans preserve phase boundaries and unequal exact counts. |

Decision type values: `direct`, `adapted`, `inferred`.
