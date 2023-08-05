import pytest
import os
from pymerkle import merkle_tree, hashing, encodings

# --------- Test intermediate success case for all possible tree types ---

HASH_TYPES = hashing.HASH_TYPES
ENCODINGS = encodings.ENCODINGS

# Directory containing this script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Generate trees (for all combinations of hash and encoding types)
# along with valid parameters for inclusion test
trees_and_subtrees = []
for security in (True, False):
    for hash_type in HASH_TYPES:
        for encoding in ENCODINGS:
            tree = merkle_tree(
                hash_type=hash_type,
                encoding=encoding,
                security=security,
                log_dir=os.path.join(current_dir, 'logs'))
            tree.encrypt_log('short_APACHE_log')
            old_hash, sublength = tree.root_hash(), tree.length()
            tree.encrypt_log('RED_HAT_LINUX_log')
            trees_and_subtrees.append((tree, old_hash, sublength))


@pytest.mark.parametrize("tree, old_hash, sublength", trees_and_subtrees)
def test_inclusion_test_with_valid_parameters(tree, old_hash, sublength):
    assert tree.inclusion_test(old_hash, sublength) is True

# -------------- Test success edge case with standard Merkle-Tree --------


tree = merkle_tree(log_dir=os.path.join(current_dir, 'logs'))
tree.encrypt_log('short_APACHE_log')
old_hash, sublength = tree.root_hash(), tree.length()
tree.encrypt_log("RED_HAT_LINUX_log")


def test_inclusion_test_edge_success_case():
    assert tree.inclusion_test(tree.root_hash(), tree.length()) is True

# ---------------- Test failure cases with standard Merkle-tree ----------


def test_inclusion_test_with_zero_sublength():
    assert tree.inclusion_test('anything...', 0) is False


def test_inclusion_test_with_sublength_exceeding_length():
    assert tree.inclusion_test('anything...', tree.length()) is False


@pytest.mark.parametrize("sublength", list(i for i in range(1, tree.length())))
def test_inclusion_test_with_invalid_old_hash(sublength):
    assert tree.inclusion_test(
        'anything except for the hash corresponding to the provided sublength',
        sublength) is False
