"""
Validation script to verify all page scripts and core modules can be compiled and loaded.
"""
import py_compile
import glob

def test_all_python_files_compile():
    py_files = glob.glob("**/*.py", recursive=True)
    assert len(py_files) > 0
    for f in py_files:
        py_compile.compile(f, doraise=True)
        print(f"Compiled successfully: {f}")

if __name__ == "__main__":
    test_all_python_files_compile()
