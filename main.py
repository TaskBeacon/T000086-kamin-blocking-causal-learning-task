from __future__ import annotations

from contextlib import nullcontext
from functools import partial
from pathlib import Path

import pandas as pd
from psychopy import core
from psyflow import (
    BlockUnit,
    StimBank,
    StimUnit,
    SubInfo,
    TaskSettings,
    context_from_config,
    initialize_exp,
    initialize_triggers,
    load_config,
    parse_task_run_options,
    runtime_context,
)

from src import build_food_map, make_phase_plans, run_trial, summarize

MODES = ("human", "qa", "sim")
DEFAULT_CONFIG_BY_MODE = {
    "human": "config/config.yaml",
    "qa": "config/config_qa.yaml",
    "sim": "config/config_scripted_sim.yaml",
}


def _run_block(name, index, plans, settings, win, kb, bank, triggers, rows):
    (
        BlockUnit(
            block_id=name,
            block_idx=index,
            settings=settings,
            window=win,
            keyboard=kb,
        )
        .add_condition(plans)
        .on_start(lambda _: triggers.send(settings.triggers.get("block_start")))
        .on_end(lambda _: triggers.send(settings.triggers.get("block_end")))
        .run_trial(
            partial(
                run_trial,
                stim_bank=bank,
                trigger_runtime=triggers,
                block_id=name,
                block_idx=index,
            )
        )
        .to_dict(rows)
    )


def run(options):
    root = Path(__file__).resolve().parent
    config = load_config(str(options.config_path))
    output_dir, scope, context = None, nullcontext(), None
    if options.mode in ("qa", "sim"):
        context = context_from_config(task_dir=root, config=config, mode=options.mode)
        output_dir, scope = context.output_dir, runtime_context(context)

    with scope:
        if options.mode == "qa":
            subject = {"subject_id": "qa086"}
        elif options.mode == "sim":
            subject = {"subject_id": str(context.session.participant_id or "sim086")}
        else:
            subject = SubInfo(config["subform_config"]).collect()

        settings = TaskSettings.from_dict(config["task_config"])
        settings.add_subinfo(subject)
        if output_dir is not None:
            settings.save_path = str(output_dir)
        if options.mode == "qa" and output_dir is not None:
            output_dir.mkdir(parents=True, exist_ok=True)
            settings.res_file = str(output_dir / "qa_trace.csv")
            settings.log_file = str(output_dir / "qa_psychopy.log")
            settings.json_file = str(output_dir / "qa_settings.json")

        settings.triggers = config["trigger_config"]
        triggers = (
            initialize_triggers(mock=True)
            if options.mode in ("qa", "sim")
            else initialize_triggers(config)
        )
        win, kb = initialize_exp(settings)
        bank = StimBank(win, config["stim_config"]).preload_all()
        settings.save_to_json()
        triggers.send(settings.triggers.get("experiment_start"))

        StimUnit("instruction", win, kb, runtime=triggers).add_stim(
            bank.get("instruction")
        ).wait_and_continue()

        food_map = build_food_map(settings, subject.get("subject_id"))
        rows = []
        seed = int(settings.random_seed)
        for block_index, phase in enumerate(settings.phase_order):
            StimUnit(f"{phase}_instruction", win, kb, runtime=triggers).add_stim(
                bank.get(f"{phase}_instruction")
            ).wait_and_continue()
            plans = make_phase_plans(settings, str(phase), food_map, seed)
            _run_block(
                str(phase), block_index, plans, settings, win, kb, bank, triggers, rows
            )

        metrics = summarize(rows)
        StimUnit("good_bye", win, kb, runtime=triggers).add_stim(
            bank.get_and_format(
                "good_bye",
                prediction_accuracy=f"{metrics['prediction_accuracy']:.1%}",
                blocked_rating="--" if metrics["blocked_rating"] is None else metrics["blocked_rating"],
                control_mean="--" if metrics["control_mean"] is None else f"{metrics['control_mean']:.2f}",
                blocking_score="--" if metrics["blocking_score"] is None else f"{metrics['blocking_score']:.2f}",
            )
        ).wait_and_continue(terminate=True)

        triggers.send(settings.triggers.get("experiment_end"))
        pd.DataFrame(rows).to_csv(settings.res_file, index=False)
        triggers.close()
        core.quit()


def main():
    run(
        parse_task_run_options(
            task_root=Path(__file__).resolve().parent,
            description="Run the Kamin Blocking and Causal Learning Task",
            default_config_by_mode=DEFAULT_CONFIG_BY_MODE,
            modes=MODES,
        )
    )


if __name__ == "__main__":
    main()
