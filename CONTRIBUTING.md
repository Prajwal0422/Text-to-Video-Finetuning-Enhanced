# Contributing to NEXUS VISION

Thank you for your interest in contributing to NEXUS VISION! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/Prajwal0422/Text-to-Video-Finetuning-Enhanced/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Error messages and logs

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Create a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Text-to-Video-Finetuning-Enhanced.git
cd Text-to-Video-Finetuning-Enhanced

# Install dependencies
pip install -r requirements.txt

# Run tests
cd backend
python test_system.py

# Start development server
python start_project.py
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Write docstrings for functions and classes

## Testing

- Test your changes thoroughly
- Add tests for new features
- Ensure existing tests pass
- Test on multiple platforms if possible

## Commit Messages

Use clear, descriptive commit messages:

```
feat: Add new video effect
fix: Resolve WebSocket connection issue
docs: Update API documentation
style: Format code with black
refactor: Optimize video processing
test: Add unit tests for generator
```

## Code Review

- Be respectful and constructive
- Respond to feedback promptly
- Make requested changes
- Keep discussions focused

## License

By contributing, you agree that your contributions will be licensed under the project's license.

## Questions?

Feel free to ask questions in:
- GitHub Issues
- Pull Request comments
- Project discussions

Thank you for contributing! 🚀
