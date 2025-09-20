# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.0   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by:

1. Opening a GitHub issue
2. Or email: [akash.mbu32@gmail.com]

Please do not report security vulnerabilities through public GitHub issues.

## Security Best Practices

- API keys are passed at runtime, not baked into the image
- Docker container runs with minimal privileges
- Dependencies are pinned to specific versions
- Regular security updates via CI/CD pipeline
