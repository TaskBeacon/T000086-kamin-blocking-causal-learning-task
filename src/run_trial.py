from __future__ import annotations

from typing import Any

from psyflow import StimUnit, next_trial_id, set_trial_context

from .utils import TrialPlan


def _set_context(
    unit: StimUnit,
    *,
    trial_id: int,
    block_id: str,
    plan: TrialPlan,
    phase: str,
    deadline: float,
    keys: list[str],
    stim_id: str,
) -> None:
    set_trial_context(
        unit,
        trial_id=trial_id,
        phase=phase,
        deadline_s=deadline,
        valid_keys=keys,
        block_id=block_id,
        condition_id=plan.condition_id,
        task_factors={**plan.to_dict(), "stage": phase},
        stim_id=stim_id,
    )


def _food_stimuli(stim_bank, plan: TrialPlan):
    if len(plan.food_labels) == 1:
        return [stim_bank.get_and_format("food_single", food=plan.food_labels[0])]
    return [
        stim_bank.get_and_format("food_left", food=plan.food_labels[0]),
        stim_bank.get_and_format("food_right", food=plan.food_labels[1]),
    ]


def _outcome_stimuli(stim_bank, outcome: str):
    if outcome == "strong":
        frames = [
            stim_bank.get("outcome_strong_outer"),
            stim_bank.get("outcome_strong_inner"),
        ]
    else:
        frames = [stim_bank.get(f"outcome_{outcome}_frame")]
    return [*frames, stim_bank.get(f"outcome_{outcome}")]


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    plan: TrialPlan = condition
    trial_id = next_trial_id()
    block_name = str(block_id or plan.stage)
    data: dict[str, Any] = {
        "trial_id": trial_id,
        "block_id": block_name,
        "block_idx": int(block_idx or 0),
        **plan.to_dict(),
    }
    food_stimuli = _food_stimuli(stim_bank, plan)

    if plan.is_test:
        rating_keys = [str(key) for key in settings.rating_keys]
        rating = StimUnit("causal_rating", win, kb, runtime=trigger_runtime).add_stim(
            stim_bank.get("test_heading"),
            *food_stimuli,
            stim_bank.get("causal_prompt"),
        )
        _set_context(
            rating,
            trial_id=trial_id,
            block_id=block_name,
            plan=plan,
            phase="causal_rating",
            deadline=float(settings.rating_window),
            keys=rating_keys,
            stim_id=f"rating_{plan.cue_roles[0].lower()}",
        )
        rating.capture_response(
            keys=rating_keys,
            duration=float(settings.rating_window),
            onset_trigger=settings.triggers.get("causal_rating"),
            response_trigger={
                key: settings.triggers.get(f"rating_{key}") for key in rating_keys
            },
            timeout_trigger=settings.triggers.get("rating_timeout"),
            terminate_on_response=True,
        ).to_dict(data)
        response = rating.get_state("response", None)
        data.update(
            response_key=str(response or ""),
            response_rt=rating.get_state("rt", None),
            causal_rating=int(response) if response is not None else None,
            correct=None,
        )
    else:
        prediction_keys = [str(key) for key in settings.prediction_keys]
        prediction = StimUnit("prediction", win, kb, runtime=trigger_runtime).add_stim(
            stim_bank.get("meal_heading"),
            *food_stimuli,
            stim_bank.get("prediction_prompt"),
        )
        _set_context(
            prediction,
            trial_id=trial_id,
            block_id=block_name,
            plan=plan,
            phase="prediction",
            deadline=float(settings.prediction_window),
            keys=prediction_keys,
            stim_id=f"{plan.condition_id}_meal",
        )
        prediction.capture_response(
            keys=prediction_keys,
            duration=float(settings.prediction_window),
            onset_trigger=settings.triggers.get(f"prediction_{plan.stage}"),
            response_trigger={
                "1": settings.triggers.get("predict_none"),
                "2": settings.triggers.get("predict_allergy"),
                "3": settings.triggers.get("predict_strong"),
            },
            timeout_trigger=settings.triggers.get("prediction_timeout"),
            terminate_on_response=True,
        ).to_dict(data)
        response = prediction.get_state("response", None)
        correct_key = str(settings.outcome_keys[plan.outcome])
        data.update(
            response_key=str(response or ""),
            response_rt=prediction.get_state("rt", None),
            causal_rating=None,
            correct=(str(response) == correct_key) if response is not None else None,
            correct_key=correct_key,
        )

        feedback = StimUnit("feedback", win, kb, runtime=trigger_runtime).add_stim(
            stim_bank.get("feedback_heading"),
            *food_stimuli,
            *_outcome_stimuli(stim_bank, plan.outcome),
        )
        _set_context(
            feedback,
            trial_id=trial_id,
            block_id=block_name,
            plan=plan,
            phase="feedback",
            deadline=float(settings.feedback_duration),
            keys=[],
            stim_id=f"outcome_{plan.outcome}",
        )
        feedback.show(
            duration=float(settings.feedback_duration),
            onset_trigger=settings.triggers.get(f"feedback_{plan.outcome}"),
        ).to_dict(data)

    iti = StimUnit("iti", win, kb, runtime=trigger_runtime).add_stim(
        stim_bank.get("blank")
    )
    _set_context(
        iti,
        trial_id=trial_id,
        block_id=block_name,
        plan=plan,
        phase="iti",
        deadline=float(settings.iti_duration),
        keys=[],
        stim_id="blank",
    )
    iti.show(
        duration=float(settings.iti_duration),
        onset_trigger=settings.triggers.get("iti"),
    ).to_dict(data)
    return data
