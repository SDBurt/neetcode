import argparse
import importlib.util
import inspect
import sys
import ast
import json
import os
from typing import Any, Dict, List

# --- Auto-import helper classes ---
# This section dynamically finds and loads helper classes (like ListNode)
# from the 'common' directory so they are available in solution modules.
common_helpers: Dict[str, Any] = {}
try:
    if os.path.isdir('common'):
        for filename in os.listdir('common'):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = os.path.splitext(filename)[0]
                module_path = os.path.join('common', filename)
                spec = importlib.util.spec_from_file_location(f"common.{module_name}", module_path)
                if spec and spec.loader:
                    common_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(common_module)
                    for name, obj in inspect.getmembers(common_module, inspect.isclass):
                        common_helpers[name] = obj
except Exception as e:
    print(f"Warning: Could not load common helpers: {e}", file=sys.stderr)
# --- End auto-import ---


def inject_common_classes(solution_module):
    """Injects classes from the common_helpers dict into a module."""
    for name, obj in common_helpers.items():
        if not hasattr(solution_module, name):
            setattr(solution_module, name, obj)


def run_solution(file_path, input_args, test_mode=False):
    """
    Dynamically loads and runs a LeetCode solution from a file.
    """
    try:
        # Create a module spec from the file path and load it
        spec = importlib.util.spec_from_file_location(file_path, file_path)
        if spec is None or spec.loader is None:
            print(f"Error: Could not create module spec for {file_path}", file=sys.stderr)
            sys.exit(1)
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        inject_common_classes(module) # Inject helpers before execution
        spec.loader.exec_module(module)
    except FileNotFoundError:
        print(f"Error: Solution file not found at {file_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error loading module from {file_path}: {e}", file=sys.stderr)
        sys.exit(1)

    # Find the Solution class and instantiate it
    if not hasattr(module, 'Solution'):
        print(f"Error: 'Solution' class not found in {file_path}", file=sys.stderr)
        sys.exit(1)
    
    SolutionClass = getattr(module, 'Solution')
    solution_instance = SolutionClass()

    # Find the public method to run
    solution_method = None
    for name, method in inspect.getmembers(solution_instance, predicate=inspect.ismethod):
        if not name.startswith('_'):
            solution_method = method
            break
    
    if solution_method is None:
        print(f"Error: No public method found in 'Solution' class in {file_path}", file=sys.stderr)
        sys.exit(1)

    if test_mode:
        run_tests(solution_method, file_path)
    else:
        run_with_custom_input(solution_method, input_args)


def run_with_custom_input(solution_method, input_args):
    # Parse input arguments from string to Python literals
    parsed_args = []
    for arg in input_args:
        try:
            parsed_args.append(ast.literal_eval(arg))
        except (ValueError, SyntaxError):
            # If it's not a literal (e.g., a plain string), use it as is
            parsed_args.append(arg)

    # Run the method and print the result
    try:
        result = solution_method(*parsed_args)
        print("Result:", result)
    except TypeError:
        print(f"Error: Method signature mismatch for {solution_method.__name__}.", file=sys.stderr)
        print(f"Expected: {inspect.signature(solution_method)}", file=sys.stderr)
        print(f"Provided: {len(parsed_args)} arguments {tuple(type(arg).__name__ for arg in parsed_args)}", file=sys.stderr)
        sys.exit(1)


def run_tests(solution_method, solution_file_path):
    test_file_path = os.path.splitext(solution_file_path)[0] + '.test.json'
    if not os.path.exists(test_file_path):
        print(f"Error: Test file not found at {test_file_path}", file=sys.stderr)
        sys.exit(1)

    with open(test_file_path, 'r') as f:
        test_cases = json.load(f)

    # --- Get helper functions from our globally loaded helpers ---
    create_linked_list_fn = common_helpers.get('create_linked_list')
    linked_list_to_list_fn = common_helpers.get('linked_list_to_list')
    list_node_class = common_helpers.get('ListNode')
    # ---

    passed_count = 0
    for i, test_case in enumerate(test_cases):
        raw_inputs = test_case['inputs']
        expected = test_case['expected']

        # --- Input Conversion ---
        # This is a simple heuristic: if a parameter is type-hinted as 'ListNode',
        # we assume the corresponding list input should be converted to a linked list.
        processed_inputs = []
        params = list(inspect.signature(solution_method).parameters.values())
        for j, arg in enumerate(raw_inputs):
            # Check if type hint is 'ListNode' and we have a conversion function
            if (j < len(params) and params[j].annotation == 'ListNode' and 
                isinstance(arg, list) and create_linked_list_fn):
                processed_inputs.append(create_linked_list_fn(arg))
            else:
                processed_inputs.append(arg)
        # ---
        
        result = solution_method(*processed_inputs)

        # --- Output Conversion & Comparison ---
        final_result = result
        # If the result is a ListNode, convert it back to a list for comparison
        if list_node_class and isinstance(result, list_node_class) and linked_list_to_list_fn:
            final_result = linked_list_to_list_fn(result)

        is_correct = False
        if isinstance(expected, list) and isinstance(final_result, list):
            try:
                # For problems where order doesn't matter, sorting is a good check
                is_correct = sorted(final_result) == sorted(expected)
            except TypeError:
                # Fallback for non-sortable lists (e.g., list of lists)
                is_correct = final_result == expected
        else:
            is_correct = final_result == expected
        # ---

        if is_correct:
            passed_count += 1
            print(f"Test Case {i+1}: PASSED")
        else:
            print(f"Test Case {i+1}: FAILED")
            print(f"  Input:    {raw_inputs}")
            print(f"  Expected: {expected}")
            print(f"  Got:      {final_result}")
            
    print(f"\nSummary: {passed_count}/{len(test_cases)} test cases passed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run a LeetCode solution file with specified inputs or tests.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  # Run with custom input
  python runner.py arrays_and_hashing/two-sum.py '[2,7,11,15]' 9

  # Run tests from the associated .test.json file
  python runner.py problems/arrays_and_hashing/two-sum.py --test
"""
    )
    parser.add_argument("solution_file", help="Path to the Python file containing the Solution class.")
    parser.add_argument("inputs", nargs='*', help="Input arguments for the solution method. Ignored if --test is used.")
    parser.add_argument("--test", action="store_true", help="Run in test mode, using the corresponding .test.json file.")
    
    args = parser.parse_args()
    
    if args.test and args.inputs:
        print("Warning: Custom inputs are ignored when running in --test mode.", file=sys.stderr)

    run_solution(args.solution_file, args.inputs, args.test) 