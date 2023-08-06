from atomic_hpc.utils import walk_path, glob_path, splitall, fnmatch_path
import pytest


def dummy_listdir(path):

    if not path:
        return ["a", "b", "c"]
    elif path.endswith("a"):
        return ["d", "c"]
    elif path.endswith("d"):
        return ["e", "c"]
    elif path.endswith("e"):
        return ["f"]
    else:
        return []


def dummy_isfile(path):
    if path.endswith("c"):
        return True
    return False


def dummy_isfolder(path):
    if not path.endswith("c"):
        return True
    return False


def dummy_walk_path(path):
    return walk_path(path, dummy_listdir, dummy_isfile, dummy_isfolder)


def test_splitall():
    assert splitall('a/b/c') == ['a', 'b', 'c']


@pytest.mark.parametrize("path,pattern", [
    ("a", "a"), ("a/bee", "a/bee"),
    ("a", "**"), ("a/b", "**"), ("a/b/c", "**"),
    ("a", "**/*"), ("a/b", "**/*"), ("a/b/c", "**/*"),
    ("a/b/c/d/e/f/ghi", "a/b/**/f/g*"),
])
def test_fnmatch_path(path, pattern):
    assert fnmatch_path(path, pattern)


@pytest.mark.parametrize("path,pattern", [
    ("a", "b"),
])
def test_fnmatch_path_fail(path, pattern):
    assert not fnmatch_path(path, pattern)


def test_glob_path():
    # print(list(dummy_walk_path("")))
    assert list(glob_path("", "**", dummy_walk_path)) == ['a', 'b', 'a/d', 'a/d/e', 'a/d/e/f']
    assert list(glob_path("", "./**", dummy_walk_path)) == ['a', 'b', 'a/d', 'a/d/e', 'a/d/e/f']
    assert list(glob_path("", "**/*", dummy_walk_path)) == ['c', 'a', 'b', 'a/c', 'a/d', 'a/d/c', 'a/d/e', 'a/d/e/f']
    assert list(glob_path("", "a/**/*", dummy_walk_path)) == ['a/c', 'a/d', 'a/d/c', 'a/d/e', 'a/d/e/f']
    assert list(glob_path("", "a/**/d", dummy_walk_path)) == ['a/d']
    assert list(glob_path("", "a/**/f", dummy_walk_path)) == ['a/d/e/f']
    assert list(glob_path("", "a/**/*/f", dummy_walk_path)) == ['a/d/e/f']
    assert list(glob_path("", "*/*", dummy_walk_path)) == ['a/c', 'a/d']
    assert list(glob_path("", "a/**/c", dummy_walk_path)) == ['a/c', 'a/d/c']
    assert list(glob_path("", "a/d/**/*", dummy_walk_path)) == ['a/d/c', 'a/d/e', 'a/d/e/f']
