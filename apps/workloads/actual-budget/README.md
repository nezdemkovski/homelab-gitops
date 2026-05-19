# Actual Budget

Actual Budget runs from the local Helm chart in:

```text
charts/actual-budget
```

The image version is pinned in `charts/actual-budget/values.yaml`:

```text
actualbudget/actual-server:26.5.2-alpine
```

Data is stored in:

```text
actual-budget/actual-budget-data
```

Actual stores server metadata under `/data/server-files` and budget files under
`/data/user-files`.

The first visit initializes the server password. The password hash is stored in
the persistent data volume, not in Git.
