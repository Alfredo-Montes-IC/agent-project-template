# Project budget planning

Use this workflow when initializing a project, selecting paid services, changing an architecture with cost implications, or checking actual spend. A solo developer can use a single budget record adapted from the [budget template](../templates/budget.template.md). The budget is a forecast and decision record; provider settings determine which limits are actually enforced.

## Establish the boundary

Record the billing period, currency, one-time and recurring spending authorization, and owner. Identify existing subscriptions and which project or account pays each cost. Record taxes, currency conversion and allocation assumptions where relevant. Keep credentials, account identifiers and private invoices out of committed documents; link only to a safe summary or authorized location.

Inventory the services the project actually uses:

- Agent and coding subscriptions, seats, credits and metered overages, including separate security/adversarial reviews, parallel agents, retries and long-running loops.
- API model usage by input, output, cache or other billed unit; built-in tools, search, images/audio, embeddings, storage and third-party API calls as applicable.
- CI runner time, operating systems, artifacts, caches and external build services.
- Hosting or serverless compute, databases, storage, network egress, traffic, backups, monitoring, domains and certificates where charged.
- Site builders and managed hosting such as ChatGPT Sites, plus any connected API, storage, database or payment services. Verify both building/editing usage and running/hosting terms for the actual workspace.

Do not add a service merely because it appears in this list. Mark unused categories not applicable with a reason.

## Verify terms and estimate

For each applicable service, use its current official pricing and the account's actual plan or agreement. Record the source URL, date checked, unit, rate, region and any unresolved assumptions. Check included allowances, shared limits, credits, expiration, overages and auto-recharge separately. Subscription access does not establish that API usage or another product is included; verify the particular account's terms. Do not hardcode transient rates or inclusion policies into the reusable template.

Estimate low, expected and high scenarios using explicit quantities. For metered components, estimate quantity multiplied by rate, including each distinct billed unit. Add fixed costs and applicable taxes or conversion assumptions. Apply allowances or credits only once and only where eligibility is confirmed. If usage or pricing is unknown, mark the estimate pending and state what evidence is needed; zero is an estimate only when its basis is verified.

Report both the total cost attributable to the project and its incremental cash cost. For an existing shared subscription, explain the allocation and avoid charging the full subscription again for each subagent or project. Keep one-time startup costs separate from recurring totals. Identify major cost drivers and provide a cheaper viable option when useful without changing the user's requirements.

## Authorize and monitor

Stay within the user's existing authorization. Before additional optional spending outside that authorization, present the concrete forecast, alternatives and limit requested. Do not purchase a plan, enable auto-recharge, raise limits or create billable resources merely to complete the estimate. A pricing lookup or estimate does not authorize expenditure.

Record the controls actually configured: request/token/retry/loop caps, concurrency and timeouts, provider quotas, enforced spending limits, and alerts where supported. Distinguish alerts from hard stops; delayed usage reporting and in-flight work can affect spend. Never claim the budget file itself blocks charges. Where workflows, E2E checks, or transformations are repeatable, prefer an "agent once, repeat deterministically" design: pay for agent discovery once per change, verify the outcome independently, save a readable deterministic script or test for zero-model-cost execution, and invoke the model again only when system drift breaks the saved check (then re-verify the repaired script).

Compare actual usage and invoices against the same period and billing account. Explain material variance, refresh stale rates and assumptions, and decide whether to reduce usage, revise the forecast or request more authorization. Preserve a concise decision record without committing private billing data.

## Starting sources

Verify the sources applicable to the selected providers rather than assuming these cover the whole project:

- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing)
- [ChatGPT plans](https://chatgpt.com/pricing/)
- [ChatGPT Sites usage and hosting](https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites)
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)

Add official pricing and billing documentation for other providers, and record the date checked in the project budget.
