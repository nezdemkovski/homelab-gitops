# Habitica

Habitica runs from the self-hosting images maintained by `awinterstein`.

Pinned images:

```text
awinterstein/habitica-server:5.46.0
mongo:8.0.23
```

Data is stored in:

```text
habitica/habitica-mongo-data
habitica/habitica-mongo-config
```

The first registered user gets admin rights. Registration is currently open for
initial testing; set `INVITE_ONLY=true` after creating the first user if this
stays deployed.
