# Doomsday Clock API

This project hosts a web API that returns the current Doomsday Clock countdown, powered by the `countdoom` Python package.

Live Endpoint:

```
GET /api/doomsday
```

Returns JSON like:

```json
{
  "seconds": 89,
  "clock": "11:58",
  "sentence": "It is 89 seconds to midnight"
}
```
