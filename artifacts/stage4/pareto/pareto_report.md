# s4r003 Pareto Report

Status: `complete`

The SVG plots each Stage3d run/checkpoint by intended-axis delta versus IFEval prompt-strict regression.

Interpretation:

- Step50 points should be treated as preferred candidates over final/loss-best points.
- noised_gold points use BFCL core as the intended axis.
- behavior points use When2Call macro F1 as the intended axis.
- Points to the upper-right are better: higher intended gain and less negative instruction-following regression.
