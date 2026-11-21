# Agent instruction evaluation template

Use this optional experiment to evaluate whether project-specific agent instructions improve outcomes. This is a template, not a claim that an experiment has been performed.

## Hypothesis and scope

- Question: [What instruction or behavior is being evaluated?]
- Project and task: [sanitized task with measurable acceptance criteria]
- Constraints: [permissions, environment and relevant project rules]
- Comparison: [instructions being evaluated and control condition]

## Method

1. Prepare equivalent isolated checkouts and record their starting revisions. Protect secrets and user data in both conditions.
2. Give each independent session the same task, context and allowed tools, changing only the instruction under evaluation where practicable.
3. Run the same project checks and inspect both diffs against the acceptance criteria. Record models, client versions and relevant conditions when known.
4. Compare correctness, security, test evidence, deviations, time and cost without disclosing private prompts or credentials.

## Results

| Criterion | Control | Candidate | Evidence and limitation |
|---|---|---|---|
| [Criterion] | [Result] | [Result] | [Safe link or summary] |

## Decision and limitations

Record the observed result, uncertainty, known confounders and next action. A single example does not prove a universal benefit; avoid inventing results or implying security certification.
