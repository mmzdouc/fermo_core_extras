# Contributing to [fermo_core_extras]

Thank you for your interest in contributing to [fermo_core_extras]! Please take a 
moment to read this document to understand how you can contribute.

## Preamble

When contributing to this repository, please first discuss the change you wish to
make via issue, email, or any other method with the owners of this repository
before making a change. Please note we have a [Code of Conduct](CODE_OF_CONDUCT.md),
please follow it in all your interactions with the project.

## Getting Started/Pull Request Process

1. Fork the repository on GitHub.
2. Clone your forked repository to your local machine:
   - `git clone git@github.com:mmzdouc/fermo_core_extras.git`
3. Create a new branch for your contribution:
   - `git checkout -b feature/your-feature-name`
4. Install the package, its requirements, and the developer requirements. A python 
   installation is required - see the `pyproject.toml`
   - `poetry install --with dev`
5. Install `pre-commit` which applies formatting and code testing before every commit:
   - `poetry run pre-commit install`
6. Make your changes and keep track of them in the [CHANGELOG.md] file.
7. Before committing the changes, increase the version number in [pyproject.toml].
8. Commit your changes to your branch:
   - `git commit -m "Add your commit message here"`
9. Push your changes to your forked repository:
   - `git push origin feature/your-feature-name`
10. Create a Pull Request (PR) on GitHub with a clear title and description.
    Reference any related issues, if applicable. Your PR will be reviewed and, if
    approved, merged.

## Code style and Guidelines

We want to write well-documented, clear and concise code that is easily maintainable.
For our strategy to achieve our goal, see below.

*"Writing code for yourself is easy - but it is difficult to write code that other
people can easily understand."*

### Code style

- We use [Semantic Versioning](http://semver.org/) for versioning.
- For code style and documentation, we follow the
  [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html). An
  easy way to check for adherence is by using the `pycodestyle` package.
- We apply following design principles:
  - **OOP** (object-oriented programming)
  - **KISS** (keep it super simple)
  - **DRY** (don't repeat yourself)
  - **SOLID** (single responsibility, open/closed, Liskov's substitution, interface
    segregation, dependency inversion)
  - **TDD** (test-driven development)
  - **Logging**
  - **LCC** (Low cognitive complexity)
- We (try to) follow the Zen of Python (`import this`)

## Testing

- We write unit tests for our code using `pytest`.
- Addition of new functionality/modification of existent functionality goes in hand
  with addition/modification of the appropriate tests.
