# Recipe: the range in CI

```yaml
- run: PYTHONPATH=src python -m pathvariance report runs/task.json
```

Exit 1 means the run count is below the stability gate, which is a data
problem, not a regression. Fail the job only on exit 2 or on an unexpected
modal shift between two committed reports.
