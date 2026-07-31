from __future__ import annotations

from psyflow.sim.contracts import Action


class ScriptedResponder:
    def start_session(self, session, rng):
        pass

    def on_feedback(self, feedback):
        pass

    def end_session(self):
        pass

    def act(self, observation):
        keys = [str(key) for key in (observation.valid_keys or [])]
        factors = dict(getattr(observation, "task_factors", {}) or {})
        phase = str(factors.get("stage", getattr(observation, "phase", "")))
        if not keys:
            return Action(key=None, rt_s=None)
        if phase in {"instruction", "good_bye"} or phase.endswith("_instruction"):
            return Action(key="space", rt_s=0.02)
        if phase == "prediction":
            outcomes = {"none": "1", "allergy": "2", "strong": "3"}
            return Action(key=outcomes.get(str(factors.get("outcome")), "2"), rt_s=0.02)
        if phase == "causal_rating":
            role = str(factors.get("cue_roles", ""))
            ratings = {"A": "8", "B": "2", "C": "6", "D": "6", "E": "7", "F": "1", "G": "1", "H": "1"}
            return Action(key=ratings.get(role, "4"), rt_s=0.02)
        return Action(key=keys[0], rt_s=0.02)


class TaskSamplerResponder:
    def __init__(self, prediction_accuracy=0.9, blocking_strength=3.0):
        self.prediction_accuracy = float(prediction_accuracy)
        self.blocking_strength = float(blocking_strength)
        self.rng = None

    def start_session(self, session, rng):
        self.rng = rng

    def on_feedback(self, feedback):
        pass

    def end_session(self):
        pass

    def act(self, observation):
        keys = [str(key) for key in (observation.valid_keys or [])]
        factors = dict(getattr(observation, "task_factors", {}) or {})
        phase = str(factors.get("stage", getattr(observation, "phase", "")))
        if not keys:
            return Action(key=None, rt_s=None)
        if phase in {"instruction", "good_bye"} or phase.endswith("_instruction"):
            return Action(key="space", rt_s=0.02)
        if phase == "prediction":
            outcomes = {"none": "1", "allergy": "2", "strong": "3"}
            correct = outcomes.get(str(factors.get("outcome")), "2")
            choose_correct = (self.rng.random() if self.rng else 0.0) <= self.prediction_accuracy
            key = correct if choose_correct else (self.rng.choice([k for k in keys if k != correct]) if self.rng else keys[0])
            return Action(key=key, rt_s=0.55)
        if phase == "causal_rating":
            role = str(factors.get("cue_roles", ""))
            center = 2.0 if role == "B" else 5.0 if role in {"C", "D"} else 4.0
            jitter = self.rng.choice([-1, 0, 0, 1]) if self.rng else 0
            return Action(key=str(max(0, min(8, round(center + jitter)))), rt_s=0.65)
        return Action(key=keys[0], rt_s=0.02)
