---
title: "The Hard Pocket Problem"
date: 2026-06-11
tags: [hard-pocket, coordination, failure-modes]
---

The IRIS framework produces a clear, measurable improvement in coordination outcomes — ToMCoordScore rising from 0.11 (baseline) to 0.38 (best candidate at 140k episodes), collision rate dropping from 0.34 to 0.11. These are the headline numbers.

What the framework also surfaces — and this is perhaps its more important contribution — is the region where improvement does not happen.

Under operational pressure — high urgency, narrow safety margins, throughput-biased norms — the agent's policy is pushed toward regretful tradeoffs. It has correctly identified the partner as cooperative, but the situation demands assertiveness. It has correctly identified the partner as assertive, but the situation demands yielding. The belief state is accurate. The context is read correctly. The two conflict, and the agent makes a decision that produces a suboptimal outcome.

We call this the *hard pocket*: a bounded region of the coordination space where better inference does not translate into better outcomes, because the inference and the correct action are in tension.

The hard pocket is not a bug. It is an empirical discovery — a measurable operational constraint on what Theory of Mind can achieve in multi-agent coordination under partial observability. It mirrors a recognised problem in agentic AI deployment (Shapira et al., 2026): systems that perform well under standard conditions degrade under the specific combination of time pressure, conflicting demands, and incomplete information.

The practical significance is that a well-characterised hard pocket is more useful than an unexamined claim of general coordination ability. An evaluation framework that reports *where it does not work* alongside *where it does* enables deployment decisions that account for operational boundaries. The IRIS hard pocket taxonomy — urgency-pressure regime, margin-narrow regime, norm-conflict regime — provides exactly this boundary specification.

Phase 1 of the IRIS development roadmap tests whether the hard pocket is architectural (specific to GRU-based learners) or fundamental (an information-theoretic limit on coordination under partial observability). Both outcomes are publishable and practically useful.



---
title: "What Does It Mean for an AI to Have a Theory of Mind?"
date: 2026-06-11
tags: [theory-of-mind, evaluation, coordination]
---

Current AI theory of mind research mostly asks one question: can the model predict what another agent will do? Static benchmarks — false-belief tasks, intention prediction from vignettes — measure inference accuracy in isolation. An agent watches a clip and guesses the next move. Success is a higher F1 score.

But prediction is not coordination. An agent that can identify a cooperative partner is not the same as an agent that *coordinates better* when it has identified one. That gap — between inference and applied coordination — is where the IRIS framework sits.

The distinction matters because the failure modes are different. An inference-only agent can achieve high prediction accuracy while pursuing policies that produce worse real outcomes: yielding to every assertive partner regardless of urgency, or committing to cooperative partners who turn out to be opportunistic. It knows *who* the partner is, but not *what to do about it*.

IRIS measures the bridge. The ToMCoordScore composite weights not just whether the agent identified the partner correctly (F1) but whether that identification improved success rate, reduced collisions, and enabled context-sensitive strategy switching. An agent that predicts perfectly but coordinates poorly scores lower than one that predicts adequately but adapts effectively.

This is not a criticism of inference benchmarks — they serve their purpose. But an AI evaluation methodology that stops at "can it guess what happens next?" misses the operational question that matters for deployed systems: *does it work better with people in the loop?* The inference-to-coordination gap is the research object, not a bug to be engineered around.



---
title: "REBUS as a Machine Learning Method"
date: 2026-06-11
tags: [rebus, reinforcement-learning, belief-updating]
---

The REBUS model (Carhart-Harris & Friston, 2019) describes how psychedelics relax the precision-weighting of high-level priors, allowing prediction errors to propagate upward and update beliefs faster. It is a theory of belief updating in the brain under uncertainty.

It is also a description of a machine learning parameter that can be formalised, implemented, and tested.

The IRIS framework uses a GRU-based recurrent belief-state estimator to maintain a distribution over partner types. In the standard configuration, belief update speed is fixed — the learning rate parameter does not change regardless of whether the agent's predictions are accurate or wildly wrong. This is computationally efficient but biologically implausible and operationally limiting: an agent that updates its beliefs at the same speed whether it is colliding every episode or sailing through smoothly cannot adapt to regime changes.

REBUS suggests a different approach. When prediction errors spike — collisions, unexpected partner switches, persistent deadlock — the precision of existing priors should relax, and the effective learning rate should increase. The agent should update its beliefs *faster* when it discovers its model of the world is wrong.

This is implementable as a dynamic learning rate parameter on the belief logits:

$$\alpha_t = \alpha_{base} + k \cdot \sigma(|\text{collision}_t - \text{expected}|)$$

The prediction error signal — already computed in the training loop as the cross-entropy between the belief state and the true partner type — modulates the confidence with which beliefs are updated. High surprise means high update rate. Low surprise means stable priors.

Importantly, the mechanism is general. It does not depend on the presence of any pharmacological agent. It is a formal description of how a system should update its beliefs under uncertainty — applicable whether the system is a biological brain, a POMDP policy, or a multi-agent orchestrator. The psychedelic science provides the mechanistic hypothesis and the empirical parameters (Kanen et al., 2023, measured LSD's effect on prediction-error sensitivity in a computational RL model). The IRIS framework provides the testbed.

The experimental design compares three conditions: a standard fixed-rate belief update, a REBUS-informed agent with precision-modulated belief update, and a combined condition in which all agents in the environment follow REBUS principles. The question is not whether REBUS works in the brain — it does. The question is whether a REBUS parameterisation of a machine learning belief update produces measurably better coordination outcomes than a fixed-rate alternative.

---
title: "Sixteen Thousand Parameters"
date: 2026-06-11
tags: [architecture, efficiency, evaluation]
---

The IRIS framework runs at approximately 16,000 parameters. A single GRU cell with 64 hidden units, a belief head, a partner-action prediction head, and a policy head — fewer parameters than a single convolutional filter in a production vision model.

This is not a limitation. It is a methodological commitment.

The current AI evaluation landscape is dominated by benchmarks that require frontier-scale infrastructure to participate. A researcher testing a new coordination architecture must either have access to a GPU cluster or rely on results published by labs that do. This creates a structural bias toward compute-intensive approaches and away from the kinds of questions that can be answered with careful, small-scale experimentation.

A 16,000-parameter architecture changes the terms. Training runs complete in hours on consumer hardware. Full experimental sweeps — five seeds, two horizons, multiple conditions — cost pennies in cloud compute. Every result is reproducible on a laptop. Every finding can be challenged, extended, or falsified by any researcher with a PyTorch install and an afternoon.

The question the framework is designed to answer — *under what conditions does improved inference produce better coordination?* — does not require a 70-billion-parameter model. It requires a clean experimental design, a fixed evaluation protocol, and a metric that penalises false safety as heavily as it rewards correct prediction. These are engineering and scientific questions, not scaling questions.

Lightweight architectures also surface problems that larger models can mask. The ~0.38 ToMCoordScore ceiling that appears across both benchmark variants is visible *because* the architecture is small enough that the ceiling cannot be blamed on insufficient capacity. If a 16,000-parameter model plateaus, the plateau is informational or structural, not computational. That is a useful thing to know.
