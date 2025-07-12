# Contributing to Streaming Pattern Matching Optimization

Thank you for your interest in contributing to this project! This guide will help you get started.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/streaming-pattern-matching-optimization.git
   cd streaming-pattern-matching-optimization
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run tests to ensure everything works:**
   ```bash
   python main.py
   ```

## 🎯 Areas for Contribution

### Algorithm Implementations
- **Boyer-Moore Algorithm**: Add streaming implementation
- **Rabin-Karp Algorithm**: Implement rolling hash approach
- **Aho-Corasick**: Multiple pattern matching
- **Z-Algorithm**: Alternative to KMP with different characteristics

### Performance Optimizations
- **Memory profiling**: Add detailed memory usage tracking
- **Parallel processing**: Multi-threaded pattern matching
- **GPU acceleration**: CUDA implementation for massive datasets
- **Cache optimization**: Improve data locality

### Visualization Enhancements
- **Interactive plots**: Add Plotly/Bokeh interactive charts
- **Real-time monitoring**: Live performance dashboards
- **3D visualizations**: Multi-dimensional analysis
- **Animation**: Show algorithm execution step-by-step

### Dataset Extensions
- **More network datasets**: Additional cybersecurity data sources
- **Synthetic data generation**: Configurable pattern complexity
- **Streaming data sources**: Real-time network feeds
- **Benchmark datasets**: Standard algorithm comparison sets

### Applications
- **Bioinformatics**: DNA sequence matching
- **Log analysis**: System log pattern detection
- **Text processing**: Document similarity
- **IoT security**: Device communication pattern analysis

## 📋 Development Guidelines

### Code Style
- Follow **PEP 8** Python style guide
- Use **type hints** for function parameters and returns
- Add **docstrings** for all functions and classes
- Keep functions **focused and small** (< 50 lines)

### Testing
- Add **unit tests** for new functions
- Include **performance benchmarks** for algorithms
- Test with **edge cases** (empty patterns, single characters)
- Validate **streaming behavior** with large datasets

### Documentation
- Update **README.md** with new features
- Add **inline comments** for complex logic
- Include **usage examples** in docstrings
- Update **requirements.txt** for new dependencies

## 🔧 Code Examples

### Adding a New Algorithm
```python
def boyer_moore_stream_matching_with_counts(stream, pattern):
    """
    Boyer-Moore algorithm for streaming pattern matching.
    
    Args:
        stream: Generator yielding characters
        pattern: String pattern to search for
    
    Returns:
        tuple: (matches, comparisons)
    """
    # Your implementation here
    pass
```

### Adding New Visualizations
```python
def create_algorithm_comparison_3d(results_df):
    """
    Create 3D visualization of algorithm performance.
    
    Args:
        results_df: DataFrame with algorithm performance data
    """
    # Your visualization code here
    pass
```

## 📊 Performance Benchmarking

When adding new algorithms:

1. **Run comprehensive tests:**
   ```bash
   python benchmark_new_algorithm.py
   ```
2. **Compare against existing algorithms**
3. **Document performance characteristics**
4. **Add results to analysis directory**

## 🐛 Bug Reports

When reporting bugs:

1. **Use the issue template**
2. **Include minimal reproduction case**
3. **Provide system information:**
   - Python version
   - Operating system
   - Package versions
4. **Include error messages and stack traces**

## 💡 Feature Requests

For new features:

1. **Check existing issues** to avoid duplicates
2. **Describe the use case** and motivation
3. **Provide implementation suggestions** if possible
4. **Consider backward compatibility**

## 🔄 Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** following the guidelines above
3. **Test thoroughly:**
   ```bash
   python -m pytest tests/
   python main.py  # Integration test
   ```
4. **Update documentation** as needed
5. **Commit with clear messages:**
   ```bash
   git commit -m "Add Boyer-Moore streaming implementation
   
   - Implement bad character heuristic
   - Add performance benchmarking
   - Include visualization updates"
   ```
6. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Commit Message Guidelines

- **Use present tense**: "Add feature" not "Added feature"
- **Be descriptive**: Explain what and why, not just what
- **Reference issues**: "Fixes #123" or "Relates to #456"
- **Keep first line under 50 characters**
- **Use bullet points** for multiple changes

## 🎉 Recognition

Contributors will be:
- **Listed in README.md** acknowledgements
- **Tagged in release notes** for significant contributions
- **Invited as collaborators** for ongoing contributors

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Email**: sahel.azzam@gmail.com for private matters

## 📚 Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Git Commit Best Practices](https://chris.beams.io/posts/git-commit/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Pattern Matching Algorithms](https://en.wikipedia.org/wiki/String-searching_algorithm)

---

**Thank you for contributing to make this project better!** 🙏 