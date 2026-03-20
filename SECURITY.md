# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please email the maintainers directly. Do not open a public issue.

## Security Measures

### API Security
- API keys stored in environment variables
- No hardcoded credentials
- Rate limiting implemented
- Input validation on all endpoints
- CORS properly configured

### Data Protection
- No user data stored permanently
- Generated videos auto-deleted after 24 hours
- No personal information collected
- Temporary files cleaned regularly
- Cache cleared periodically

### Network Security
- WebSocket connections validated
- HTTPS recommended for production
- No sensitive data in URLs
- Secure headers configured
- XSS protection enabled

### Code Security
- Dependencies regularly updated
- No eval() or exec() usage
- Input sanitization
- Error messages sanitized
- Logging without sensitive data

## Best Practices

### For Developers
1. Never commit API keys
2. Use environment variables
3. Validate all inputs
4. Sanitize error messages
5. Keep dependencies updated

### For Users
1. Keep API keys private
2. Use strong passwords
3. Don't share credentials
4. Monitor API usage
5. Report suspicious activity

## Known Limitations

### Current Scope
- Single-user deployment
- Local network only
- No authentication system
- Basic rate limiting
- File-based storage

### Future Improvements
- User authentication
- Role-based access
- Database encryption
- Advanced rate limiting
- Audit logging
