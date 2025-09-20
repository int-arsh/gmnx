# Contributing to gmnx

Thank you for your interest in contributing to gmnx!

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/int-arsh/gmnx.git
   cd gmnx
   ```

2. **Set up development environment**
   ```bash
   make install-deps
   ```

3. **Run tests**
   ```bash
   make test
   ```

## Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**
   ```bash
   make test
   make test-coverage
   ```

4. **Submit a pull request**
   - Describe what you changed
   - Reference any related issues
   - Ensure all tests pass

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings for functions
- Keep functions small and focused

## Testing

- All new features must have tests
- Maintain or improve test coverage
- Test both success and error cases
