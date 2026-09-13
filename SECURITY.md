# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 2.x.x | Yes |
| < 2.0 | No |

## Architecture Security

AOE is designed with **privacy-first, local-first** architecture:

- **Zero cloud dependency**: All data stays on your local machine
- **No hardcoded credentials**: OAuth tokens, API keys, and personal data are strictly `.gitignore`d
- **Safe Mode default**: `DRY_RUN=true` prevents accidental email dispatch
- **Activation Passkey**: Optional security gate for live operations
- **SQLite isolation**: Database files never leave your computer

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT** open a public GitHub issue
2. Email the maintainer or open a private security advisory via [GitHub Security Advisories](https://github.com/lordpardonme/aoe/security/advisories/new)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will acknowledge receipt within 48 hours and provide a detailed response within 7 days.

## Security Checklist for Contributors

- [ ] Never commit `.env`, `.db`, `token.json`, or `credentials.json`
- [ ] Always use `DRY_RUN=true` during development
- [ ] Sanitize all user inputs in API endpoints
- [ ] Use parameterized SQL queries (no string concatenation)
