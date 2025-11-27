# Contributing to SME-ERPSim

Thank you for your interest in contributing to SME-ERPSim! This document outlines the process for making contributions and the standards we maintain.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. All contributors are expected to:
- Be respectful and professional in all interactions
- Provide constructive feedback
- Focus on the code and ideas, not individuals
- Help maintain a harassment-free community

## How to Contribute

### Reporting Issues

If you encounter a bug or have a feature request:

1. **Check existing issues** to avoid duplicates
2. **Create a new issue** with:
   - A clear, descriptive title
   - Detailed description of the problem or feature
   - Steps to reproduce (for bugs)
   - Python version, OS, and package versions
   - Any relevant error messages or logs

### Submitting Pull Requests

We welcome pull requests for bug fixes, documentation improvements, and new features. Follow this process:

1. **Fork the repository** and create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Install development dependencies**:
   ```bash
   pip install -e .[test]
   ```

3. **Make your changes**:
   - Follow the code style guidelines (see below)
   - Add tests for new functionality
   - Update documentation as needed
   - Ensure all tests pass: `pytest`

4. **Commit with clear messages**:
   ```bash
   git commit -m "Add descriptive commit message"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a pull request**:
   - Provide a clear description of changes
   - Reference related issues using `#issue_number`
   - Ensure CI checks pass

## Code Style and Standards

### Python Code Style

- **PEP 8 compliance**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- **Type hints**: Use type annotations for all function parameters and return types
- **Docstrings**: Use Google-style docstrings for all public functions and classes

Example:

```python
def calculate_lead_time(order: Order, completion_time: float) -> float:
    """Calculate lead time for an order.

    Args:
        order: The order object with arrival time.
        completion_time: The simulation time when order was completed.

    Returns:
        Lead time in hours.

    Raises:
        ValueError: If completion_time is before order arrival.
    """
    if completion_time < order.arrival_time:
        raise ValueError("Completion time cannot be before arrival time")
    return completion_time - order.arrival_time
```

### Testing Requirements

- **Test coverage**: Aim for >80% code coverage
- **Test structure**: One test file per module (e.g., `test_process_model.py` for `process/model.py`)
- **Test naming**: Use descriptive names starting with `test_`
- **Assertions**: Use clear, specific assertions

Example:

```python
def test_process_model_add_activity():
    """Test adding activities to a process model."""
    model = ProcessModel("test_process")
    activity = Activity("test_activity", duration=lambda rng: 1.0)

    model.add_activity(activity, is_start=True)

    assert "test_activity" in model.activities
    assert model.start_activity == "test_activity"
```

### Documentation Standards

- **Docstring format**: Google style for all public APIs
- **README updates**: Include examples for new features
- **Configuration examples**: Update YAML/JSON examples in `examples/` directory
- **Comments**: Use only for complex logic; favor self-documenting code

## Architecture and Design Principles

### Core Principles

1. **Simplicity**: Keep interfaces simple; hide complexity
2. **Domain-driven**: Use business language (orders, resources, activities)
3. **Extensibility**: Allow subclassing and composition
4. **Validation**: Catch errors early with Pydantic schemas
5. **Reproducibility**: Deterministic random seeds for all stochastic operations

### Module Organization

- **config/**: Configuration validation and loading
- **process/**: Process modeling (activities, transitions, routing)
- **simulation/**: Simulation engine and event handling
- **resources/**: Resource modeling (workers, machines, calendars)
- **demand/**: Demand generation and arrival processes
- **io/**: External data integration (CSV, ERP exports)
- **kpi/**: Performance metrics and reporting
- **calibration/**: Parameter estimation from data
- **experiments/**: Experimental design helpers
- **visualization/**: Plotting and chart generation

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/sme_erpsim tests/

# Run specific test file
pytest tests/test_simulation_engine.py

# Run with verbose output
pytest -v
```

### Local Testing of Examples

```bash
# Install in development mode
pip install -e .

# Run CLI example
sme-erpsim run-config examples/make_to_stock.yaml

# Run Jupyter notebook
jupyter notebook examples/small_trading_company.ipynb
```

## Documentation

All documentation should be:
- **Clear and concise**: Avoid jargon where possible
- **Complete**: Include all parameters, return values, and exceptions
- **Tested**: Verify that code examples in documentation actually work

## Release Process

When maintainers prepare a release:

1. Update version in `pyproject.toml`
2. Update `CITATION.cff` with new version
3. Create a tag: `git tag -a v0.x.0 -m "Release version 0.x.0"`
4. Push tag: `git push origin v0.x.0`

## Questions or Need Help?

- **Open an issue** for questions or clarifications
- **Start a discussion** for design feedback
- **Check the README** and existing code for examples

## Acknowledgments

Thank you for contributing to SME-ERPSim! All contributions, no matter how small, help improve the project for the entire community.

## License

By contributing to SME-ERPSim, you agree that your contributions will be licensed under the MIT License.
