from __future__ import annotations

from dataclasses import asdict, dataclass
import random
from typing import Any


@dataclass(frozen=True)
class TrialPlan:
    condition_id: str
    stage: str
    cue_roles: tuple[str, ...]
    food_labels: tuple[str, ...]
    outcome: str
    repetition: int
    is_test: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["cue_roles"] = "|".join(self.cue_roles)
        payload["food_labels"] = "|".join(self.food_labels)
        return payload


def _subject_number(subject_id: Any, fallback: int) -> int:
    digits = "".join(char for char in str(subject_id) if char.isdigit())
    return int(digits) if digits else int(fallback)


def _rotate(values: list[str], offset: int) -> list[str]:
    if not values:
        return values
    offset %= len(values)
    return values[offset:] + values[:offset]


def build_food_map(settings, subject_id: Any) -> dict[str, str]:
    """Counterbalance food names across cue roles without changing task semantics."""
    group = _subject_number(subject_id, int(settings.random_seed))
    blocking_roles = list("ABCDEFGH")
    pretraining_roles = list("IJKL")
    blocking_foods = _rotate(list(settings.blocking_foods), group % 8)
    pretraining_foods = _rotate(list(settings.pretraining_foods), group % 4)
    return {
        **dict(zip(blocking_roles, blocking_foods)),
        **dict(zip(pretraining_roles, pretraining_foods)),
    }


def make_phase_plans(settings, phase: str, food_map: dict[str, str], seed: int) -> list[TrialPlan]:
    counts = dict(settings.phase_trials[phase])
    specs = dict(settings.condition_specs)
    plans: list[TrialPlan] = []
    for condition_id, count in counts.items():
        spec = dict(specs[condition_id])
        roles = tuple(str(role) for role in spec["cue_roles"])
        for repetition in range(1, int(count) + 1):
            plans.append(
                TrialPlan(
                    condition_id=str(condition_id),
                    stage=str(spec["stage"]),
                    cue_roles=roles,
                    food_labels=tuple(food_map[role] for role in roles),
                    outcome=str(spec.get("outcome", "")),
                    repetition=repetition,
                    is_test=bool(spec.get("is_test", False)),
                )
            )
    phase_offset = list(settings.phase_order).index(phase) * 1009
    random.Random(int(seed) + phase_offset).shuffle(plans)
    return plans


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    learning = [row for row in rows if not bool(row.get("is_test"))]
    answered = [row for row in learning if row.get("response_key")]
    accuracy = (
        sum(bool(row.get("correct")) for row in answered) / len(answered)
        if answered
        else 0.0
    )
    ratings = {
        str(row.get("cue_roles")): row.get("causal_rating")
        for row in rows
        if bool(row.get("is_test")) and row.get("causal_rating") is not None
    }
    blocked = ratings.get("B")
    controls = [ratings.get("C"), ratings.get("D")]
    available_controls = [float(value) for value in controls if value is not None]
    control_mean = (
        sum(available_controls) / len(available_controls)
        if available_controls
        else None
    )
    blocking_score = (
        control_mean - float(blocked)
        if control_mean is not None and blocked is not None
        else None
    )
    return {
        "prediction_accuracy": accuracy,
        "blocked_rating": blocked,
        "control_mean": control_mean,
        "blocking_score": blocking_score,
    }
