# Five-minute video narration

AI-generated narration. Review the final upload before submission.

## Segment 1

A maintenance planner has twenty-five weekly review slots. Which wells should make the queue? We are Data Titans, and this is WellGuard. In an eighteen-week historical replay, our ranking surfaced one hundred and sixteen eligible recorded events. A rule based on time since the last logged failure surfaced seventy-five. Both used exactly four hundred and fifty review slots. This measures prioritization before a recorded date. It does not measure failures prevented.

## Segment 2

We combined daily production with records of equipment failures. Maintenance jobs provide context during review. The failure logs show a sharp coverage change. There are no logged events in twenty twenty-three or twenty twenty-four in this extract, even though wells were producing. We used the later period for supervised evaluation. Unrecorded events remain possible, so our result applies to the recorded outcome and the eligible wells.

## Segment 3

Every Sunday, we summarize recent production, downtime and available pump telemetry. The target is whether a failure is recorded during the next fourteen days. We train on earlier weeks, tune on a separate validation period, and evaluate on the later eighteen-week holdout. Gaps between periods exceed the label horizon. Dates establish the retrospective feature cutoff. The source does not tell us when every record was first available to the planner.

## Segment 4

This chart compares distinct event recall at equal weekly capacity. At twenty-five reviews the full model surfaced eighteen percent of eligible recorded events, versus eleven point seven percent for recency. A paired event-date block sensitivity interval puts the gap at roughly four to eight percentage points. The operating-only reconstruction surfaced one hundred and eleven events. Our most important limitation is timeliness. With inputs aged by seven days, the refit full model surfaced sixty-six events at twenty-five slots, versus seventy-five for lagged recency. Weekly input availability needs to be verified before operational use.

## Segment 5

Here is the actual offline demonstration using synthetic wells. The planner selects a historical week, then changes capacity from twenty-five to fifty slots. The queue updates, keeping review effort visible. A cooldown explores avoiding repeat assignments on consecutive snapshots. These results are exploratory, so the default comparison does not use a cooldown. The planner can open a well and trace its earlier oil, downtime, and pump signals. The investigator labels absent readings and gives the operator checks to perform. The view supports review and gives a path back to evidence. It makes no causal diagnosis.

## Segment 6

The simulator asks what would have to be true for a queue to pay for itself. In the example, twenty-five reviews at fifty Canadian dollars cost twelve hundred and fifty dollars. Three candidate events, with assumptions for addressability, effectiveness, volume and value, give eighteen hundred dollars of hypothetical gross benefit. Break-even intervention effectiveness is about twenty-one percent for those inputs. None of these inputs represents verified Strathcona costs or savings. The point is to make the economic assumptions inspectable.

## Segment 7

Our next step is a shadow pilot with no changes to field operations. First verify when the daily measurements and event history actually arrive. Freeze both queues at the same weekly cutoff. Ask planners to log whether each review was actionable and have events adjudicated independently. Compare event recall, workload, repeat alerts and lead time. Use recency as the comparator, and test it as a fallback if recent operational inputs are unavailable. A controlled intervention study would be needed to estimate realized benefit.

## Segment 8

WellGuard gives the maintenance planner a reviewable queue, an evidence trail, and an honest account of where the ranking loses its advantage. The historical comparison is one hundred and sixteen versus seventy-five at the same capacity. The project source reproduces both the headline result and the reporting-delay stress test. The public demonstration uses synthetic well records. Artificial intelligence assisted the development and this narration. Thank you.
