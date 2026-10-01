# YUGA Platform — CodeGhost demo target

A deliberately buggy FastAPI service used to showcase **CodeGhost**:
production crash in → verified fix + pull request out.

## Demo scenario

1. `GET /rooms/huddle-0/occupancy` — the Huddle Room was provisioned with
   `capacity=0` (bad config row), so the occupancy calculation divides by
   zero → HTTP 500.
2. The crash interceptor signs the report (HMAC-SHA256) and ships it to the
   CodeGhost orchestrator.
3. Orchestrator: generates a failing pytest → proves it RED in an isolated
   Docker sandbox → generates a fix → proves it GREEN in the same sandbox →
   opens a pull request with both raw outputs attached.
4. `GET /explode` — crash message carrying a fake API key + admin email.
   Microsoft Presidio scrubs both to `<SCRUBBED>` before the data leaves
   the process.

## Run

```bash
uvicorn main:app --port 8003
curl http://127.0.0.1:8003/rooms/atlas/occupancy    # 200
curl http://127.0.0.1:8003/rooms/huddle-0/occupancy # 500 → pipeline
```

Human stays in the loop — merging the fix is one click.