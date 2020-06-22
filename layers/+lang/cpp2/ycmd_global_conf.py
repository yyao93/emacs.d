import os
from os import path
import ycm_core
import subprocess
import logging
import json
from itertools import dropwhile, takewhile

# These are the compilation flags that will be used in case there's no
# compilation database found
flags = [
    '-fexceptions', '-DNDEBUG', '-std=c++14', '-x', 'c++',
    '-Wno-unused-parameter', '-Wall', '-Wextra', '-Wpedantic', '-I', '.', '-I',
    '../', '-I', '../../'
]

# Flags that always get added
# -fspell-checking gives better fixits and has no downside
extra_flags = ['-fspell-checking']

SOURCE_EXTENSIONS = [
    '.x.cpp', '.cpp', '.cxx', '.cc', '.c', '.m', '.mm', '.t.cpp'
]

HEADER_EXTENSIONS = {'.h', '.hxx', '.hpp', '.hh'}

l = logging.getLogger()


def load_system_includes(gcc_toolchain=None):

    if gcc_toolchain is None:
        gcc_toolchain = "-stdlib=libc++"

    l.info("Calling clang at {}".format(subprocess.check_output(["which", "clang"])))
    l.info("Clang version: {}".format(subprocess.check_output(["clang", "--version"])))

    process = subprocess.Popen(
        ['clang', '-v', '-E', '-x', 'c++', '-', gcc_toolchain],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    process_out, process_err = process.communicate('')
    output = process_err.decode('utf8').split('\n')

    def not_start(s):
        return s != "#include <...> search starts here:"

    def not_end(s):
        return s != "End of search list."

    from_start = dropwhile(not_start, output)
    next(from_start)

    return ["-isystem" + x[1:] for x in takewhile(not_end, from_start)]


def find_in_parent_dir(original_file, target):
    d = os.path.abspath(original_file)

    while not os.path.ismount(d):
        d = os.path.dirname(d)

        if os.path.exists(os.path.join(d, target)):
            return d

    return None


def pairwise(iterable):
    it = iter(iterable)
    previous = next(it)

    for x in it:
        yield (previous, x)
        previous = x


def make_paths_absolute(flags, working_directory):

    path_flags = ['-isystem', '-I', '-iquote', '--sysroot=']

    if not working_directory:
        return list(flags)

    new_flags = []

    def make_path_absolute(path):
        if os.path.isabs(path):
            return path
        return os.path.join(working_directory, path)

    pair_iter = pairwise(flags)
    for flag, next_flag in pair_iter:

        path_flag = next((p for p in path_flags if flag.startswith(p)), None)

        if not path_flag:
            new_flags.append(flag)
            continue

        if flag == path_flag:
            new_flags.extend([flag, make_path_absolute(next_flag)])
            try:
                next(pair_iter)
            except StopIteration:
                break
            continue

        path = flag[len(path_flag):]
        new_flags.append(path_flag + make_path_absolute(path))

    return new_flags


def header_heuristic_source_file(header_file, database):
    l.info("Begin corresponding source file heuristic")
    basename = os.path.splitext(header_file)[0]
    for extension in SOURCE_EXTENSIONS:
        replacement_file = basename + extension
        if os.path.exists(replacement_file):
            compilation_info = database.GetCompilationInfoForFile(
                replacement_file)
            l.info(
                "Found corresponding source file {}".format(replacement_file))
            if compilation_info.compiler_flags_:
                return compilation_info
            l.warn("Did not find corresponding source file in database!")

    return None


def heuristic_same_dir(filename, database):
    file_dir = os.path.dirname(filename)
    dir_files = os.listdir(file_dir)
    extension = path.splitext(filename)[-1]

    # Prioritize same extension over different, helps with test files
    dir_files = [x for x in dir_files if x.endswith(extension)
                 ] + [x for x in dir_files if not x.endswith(extension)]

    for f in dir_files:
        if any(f.endswith(i) for i in SOURCE_EXTENSIONS):
            compilation_info = database.GetCompilationInfoForFile(
                os.path.join(file_dir, f))
            if compilation_info.compiler_flags_:
                l.info("Found samedir file for flags: {}".format(f))
                return compilation_info

    return None


def heuristic_closest_in_db(filename, database):
    l.info("Entering closest file in db heuristic")
    database_dir = find_in_parent_dir(filename, "compile_commands.json")
    with open(path.join(database_dir, "compile_commands.json")) as f:
        json_db = json.load(f)

    db_filenames = (path.join(x['directory'], x['file']) for x in json_db)

    extension = path.splitext(filename)[-1]

    def key_value(db_fn):
        distance = path.relpath(filename, db_fn).count('/')
        # Prioritize same extension; this can help with test files
        return distance - (0.5 if db_fn.endswith(extension) else 0)

    best_match = min(db_filenames, key=key_value)
    l.info("Best match found: {}".format(best_match))
    l.info("With value".format(key_value(best_match)))

    compilation_info = database.GetCompilationInfoForFile(best_match)

    if compilation_info.compiler_flags_:
        return compilation_info

    return None


def exact(filename, database):
    compilation_info = database.GetCompilationInfoForFile(filename)
    if compilation_info.compiler_flags_:
        return compilation_info

    return None


def apply_heuristics(filename, database, heuristics):
    for h in heuristics:
        compilation_info = h(filename, database)
        if compilation_info is not None:
            return compilation_info


HEADER_HEURISTICS = [
    header_heuristic_source_file, heuristic_same_dir, heuristic_closest_in_db
]
SOURCE_HEURISTICS = [exact, heuristic_same_dir, heuristic_closest_in_db]


def get_flags_from_database(filename, database_dir):

    database = ycm_core.CompilationDatabase(database_dir)

    if not os.path.splitext(filename)[1] in HEADER_EXTENSIONS:
        l.info("Source file, looking up flags in database")
        compilation_info = apply_heuristics(filename, database,
                                            SOURCE_HEURISTICS)
    else:
        l.info("Header file, starting heuristics")
        compilation_info = apply_heuristics(filename, database,
                                            HEADER_HEURISTICS)

    if compilation_info is None:
        return None

    final_flags = make_paths_absolute(compilation_info.compiler_flags_,
                                      compilation_info.compiler_working_dir_)

    # ycmd's heuristics are broken unfortunately, and decide that compiling
    # with clang means that we are compiling c code and not c++ code,
    # leading to marking every use of try/throw/catch as an error
    # final_flags[2] = 'c++'
    final_flags[0] = "clang++"

    # To get system includes, see if gcc toolchain option specified
    gcc_toolchain = next(
        (x for x in final_flags if x.startswith("--gcc-toolchain")), None)
    l.info("Gcc toolchain flag: {}".format(gcc_toolchain))
    final_flags = final_flags + load_system_includes(gcc_toolchain)

    return final_flags


def FlagsForFile(filename, **kwargs):

    l.info("Finding flags for file {}".format(filename))
    database_dir = find_in_parent_dir(filename, "compile_commands.json")

    final_flags = None

    if database_dir is not None:
        l.info("Database found at directory {}".format(database_dir))
        # Bear in mind that compilation_info.compiler_flags_ does NOT return a
        # python list, but a "list-like" StringVec object
        final_flags = get_flags_from_database(filename, database_dir)

    if final_flags is None:
        relative_to = os.path.dirname(os.path.abspath(filename))
        final_flags = make_paths_absolute(
            flags, relative_to) + load_system_includes()

    return {'flags': final_flags + extra_flags, 'do_cache': True}
