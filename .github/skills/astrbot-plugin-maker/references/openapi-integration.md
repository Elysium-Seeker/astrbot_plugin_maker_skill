# AstrBot OpenAPI Integration Notes

Use this reference when plugin requirements include calling AstrBot HTTP APIs.

## Baseline Facts
- Server default: http://localhost:6185
- API namespace: /api/v1/*
- Authentication: API Key header `X-API-Key`
- OpenAPI doc page: https://docs.astrbot.app/scalar.html

## Observed Endpoint Groups
- GET /api/v1/im/bots
- POST /api/v1/file
- GET /api/v1/file
- POST /api/v1/chat
- GET /api/v1/chat/sessions
- POST /api/v1/im/message
- GET /api/v1/configs

## Known Response/Status Patterns
- Standard success shape often contains: status, message, data
- Common auth failures: 401 Unauthorized, 403 Forbidden

## Implementation Guidance
1. Read API key from config or environment variables; never hardcode.
2. Keep base URL configurable.
3. Wrap API calls with clear timeout and exception handling.
4. Return user-friendly diagnostics for 401/403 and network failures.

## Testing Guidance
- Add test for missing/invalid API key behavior.
- Add test for handling 401 and 403.
- Add test for parsing canonical success shape.
- Keep tests offline by mocking HTTP responses.

## Curl Example
```bash
curl http://localhost:6185/api/v1/im/bots \
  --header 'X-API-Key: YOUR_SECRET_TOKEN'
```
