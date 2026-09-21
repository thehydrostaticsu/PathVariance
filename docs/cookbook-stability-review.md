# Cookbook: reading a stability report

```
python -m pathvariance report samples/task-repeat.json
```

Read the modal share first, then the divergence index. A high modal share with
late divergence is a healthy agent; an early divergence means it disagrees
about how to start, which is a prompt or tool description problem.
