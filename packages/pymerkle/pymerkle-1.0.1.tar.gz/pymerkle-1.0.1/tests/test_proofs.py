import pytest
from pymerkle import merkle_tree, validate_proof
from pymerkle.proof import proof
import json

# Generate proofs from a one-thousand leaves Merkle-tree
tree = merkle_tree(*(bytes('{}-th record'.format(i), 'utf-8')
                     for i in range(0, 1000)))
p = tree.audit_proof(666)  # Genuine index-based proof
q = tree.audit_proof(1000)  # Empty index-based proof

# ------------------- Check replicates in all possible ways -------------------

p_1 = proof(from_json=p.JSONstring())
p_2 = proof(from_dict=json.loads(p.JSONstring()))
q_1 = proof(from_json=q.JSONstring())
q_2 = proof(from_dict=json.loads(q.JSONstring()))


@pytest.mark.parametrize('replicate', (p_1, p_2))
def test_p_replicates_via_serialization(replicate):
    assert p.serialize() == replicate.serialize()


@pytest.mark.parametrize('replicate', (q_1, q_2))
def test_q_replicates_via_serialization(replicate):
    assert q.serialize() == replicate.serialize()

# ----------------------- Check record based generations -----------------


p_3 = tree.audit_proof('665-th record')
p_4 = tree.audit_proof(b'665-th record')


@pytest.mark.parametrize('r', (p_3, p_4))
def test_record_based_audit_proof(r):
    assert tree.multi_hash(
        p.body['proof_path'],
        p.body['proof_index']) == tree.multi_hash(
        r.body['proof_path'],
        p.body['proof_index'])
