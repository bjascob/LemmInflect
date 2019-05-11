#!/usr/bin/python3
import sys
sys.path.insert(0, '..')
import os
import time
from   fnmatch import fnmatch
from   importlib.util import spec_from_file_location
from   importlib.util import module_from_spec
import inspect
import unittest


# Get all python files below the base directory
def getAllPythonFiles(base_dir):
    test_fns = []
    for root, subdirs, files in os.walk(base_dir):
        for fn in files:
            if fnmatch(fn, '*.py') and not fn.startswith('_'):
                test_fns.append( os.path.join(root,fn) )
    return sorted(test_fns)


# Returns the loaded module/class and the name of the file (without the extension or path)
# !! Note: only one test class definition is allowed per file and it's required that it have
#          the same name as the file (ie.. TestXX.py has class TestXY(object) )
#          This restriction could be removed if the function were changed to return a list,
#          however, this also allows putting helper class defintions inside that will be ignored.
def getTestClass(fn):
    # Separate the filename into components to load the module
    prefix = os.path.splitext(fn)[0]
    parts  = prefix.split(os.sep)
    prefix = '.'.join(parts)
    class_name = parts[-1]
    # Load the actual module
    try:
        spec   = spec_from_file_location(prefix, fn)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
    except ModuleNotFoundError:
        return (None, None)
    # Loop through all classes that are part of the module.  Returns a tuple of (name, value)
    # ie.. the string name of the class and the actual class definition that can be instantiated
    # This is finding the class by assuming that the name of the class is the same as the name of the file
    my_class_tuple = (None, None)
    for class_tuple in inspect.getmembers(module, inspect.isclass):
        # check class name is the same as module name and return that class.
        if class_tuple[0] == class_name:
            my_class_tuple = class_tuple
    return my_class_tuple


# Note: to capture output, run: `./RunAllUnitTests.py | tee test.log`
if __name__ == '__main__':
    test_fns = getAllPythonFiles('..' + os.sep + 'tests' + os.sep + 'auto')
    assert test_fns, 'Error: no test files found'

    # Loop through all file names
    st = time.time()
    stats = []
    for fn in test_fns:
        test_name, test_class = getTestClass(fn)
        if not test_name or not test_class:
            print('No module loaded for ', fn)
            continue
        print('Running tests in: ', fn)
        print()
        # Run the test
        loader = unittest.TestLoader()
        test = loader.loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
        results = runner.run(test)
        # Accumulate results
        stats.append( (test_name, results.testsRun, len(results.errors), \
                len(results.failures), len(results.skipped) ) )
        print()
        print('*'*80)
    # Summary
    print()
    print('Complete.  Test run time is {:,} seconds'.format(int(time.time()-st)))
    print()
    print('Testing Summary:')
    print('   %-30s   %12s %12s %12s %12s' % ('Suite Name', 'Num Run', 'Errors', 'Fails', 'Skipped'))
    for stat in stats:
        print('   %-30s %12d %12d %12d %12d' % stat)
    total   = sum([x[1] for x in stats])
    errors  = sum([x[2] for x in stats])
    fails   = sum([x[3] for x in stats])
    skipped = sum([x[4] for x in stats])
    print('  ' + '-'*85)
    print('   %-30s %12d %12d %12d %12d' % ('Total:', total, errors, fails, skipped))
    print()
