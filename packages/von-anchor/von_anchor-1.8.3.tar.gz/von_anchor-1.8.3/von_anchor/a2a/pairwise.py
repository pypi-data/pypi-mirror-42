"""
Copyright 2017-2019 Government of Canada - Public Services and Procurement Canada - buyandsell.gc.ca

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import json

from von_anchor.canon import raw
from von_anchor.error import BadWalletQuery


TYPE_PAIRWISE = 'pairwise'
WQL_1_OPS = frozenset(('$in', '$not', '$neq', '$gt', '$gte', '$lt', '$lte', '$like'))


class PairwiseInfo:
    """
    Bundle for pairwise DID relation: DIDs, verification keys, and metadata.
    """

    def __init__(self, their_did: str, their_verkey: str, my_did: str, my_verkey: str, metadata: dict = None) -> None:
        """
        Initialize DIDs, verification keys, metadata.

        :param their_did: remote DID to store
        :param their_verkey: remote verification key to store
        :param my_did: local DID to store
        :param my_verkey: local verification key to store
        :param metadata: metadata associated with pairwise DID relationship
        """

        self._their_did = their_did
        self._their_verkey = their_verkey
        self._my_did = my_did
        self._my_verkey = my_verkey
        self._metadata = metadata

    @property
    def their_did(self) -> str:
        """
        Accessor for remote DID

        :return: remote DID
        """

        return self._their_did

    @property
    def their_verkey(self) -> str:
        """
        Accessor for remote verification key

        :return: remote verification key
        """

        return self._their_verkey

    @property
    def my_did(self) -> str:
        """
        Accessor for local DID

        :return: local DID
        """

        return self._my_did

    @property
    def my_verkey(self) -> str:
        """
        Accessor for local verification key

        :return: local verification key
        """

        return self._my_verkey

    @property
    def metadata(self) -> dict:
        """
        Accessor for metadata

        :return: metadata
        """

        return self._metadata

    @metadata.setter
    def metadata(self, value: dict) -> None:
        """
        Accessor for metadata

        :param value: metadata dict
        """

        self._metadata = value

    def __eq__(self, other: 'PairwiseInfo') -> bool:
        """
        Equivalence operator. Two PairwiseInfos are equivalent when their attributes are.

        :param other: PairwiseInfo to test for equivalence
        :return: whether PairwiseInfos are equivalent
        """

        return (
            self.their_did == other.their_did and
            self.their_verkey == other.their_verkey and
            self.my_did == other.my_did and
            self.my_verkey == other.my_verkey and
            self.metadata == self.metadata)

    def __repr__(self) -> str:
        """
        Return representation.

        :return: string representation evaluating to construction call
        """

        return 'PairwiseInfo({}, {}, {}, {}, {})'.format(
            self.their_did,
            self.their_verkey,
            self.my_did,
            self.my_verkey,
            self.metadata)


def pairwise_info2tags(pairwise: PairwiseInfo) -> str:
    """
    Given pairwise info with metadata mapping tags to values, return corresponding
    indy-sdk json to store same in wallet (via non_secrets) unencrypted (for WQL search options).
    Canonicalize metadata values to strings via raw() for WQL fitness.

    :param pairwise: pairwise info with metadata dict mapping tags to values
    :return: corresponding non_secrets tags json marked for unencrypted storage
    """

    rv = {
        canon_pairwise_tag(tag): raw(pairwise.metadata[tag]) for tag in pairwise.metadata or {}
    }
    rv['~their_did'] = pairwise.their_did
    rv['~their_verkey'] = pairwise.their_verkey
    rv['~my_did'] = pairwise.my_did
    rv['~my_verkey'] = pairwise.my_verkey
    return json.dumps(rv)


def record2pairwise_info(record: dict) -> PairwiseInfo:
    """
    Given indy-sdk non_secrets pairwise record dict, return corresponding PairwiseInfo.

    :param record: non_secrets pairwise record dict
    :return: PairwiseInfo on non_secrets pairwise record DIDs, verkeys, metadata
    """

    return PairwiseInfo(
        record['id'],  # = their did
        record['value'],  # = their verkey
        record['tags']['~my_did'],
        record['tags']['~my_verkey'],
        {
            tag[tag.startswith('~'):]: record['tags'][tag] for tag in record.get('tags', {})  # strip any leading '~'
        })


def canon_pairwise_tag(tag: str) -> str:
    """
    Canonicalize pairwise tag to specify unencrypted storage.

    :param tag: input tag
    :return: tag prefixed with '~' if not already
    """

    return '{}{}'.format('' if tag.startswith('~') else '~', tag)


def canon_pairwise_wql(query: dict = None) -> dict:
    """
    Canonicalize WQL tags to unencrypted storage specification.
    Canonicalize comparison values to strings via raw().

    Raise BadWalletQuery for WQL mapping '$or' to non-list.

    :param query: WQL query
    :return: canonicalized WQL query dict
    """

    if not query:
        return {
            '~their_did': {
                '$neq': ''
            }
        }

    for k in [qk for qk in query]:  # copy: iteration alters query keys
        if isinstance(query[k], dict):  # only subqueries are dicts: recurse
            query[k] = canon_pairwise_wql(query[k])
        if k == '$or':
            if not isinstance(query[k], list):
                raise BadWalletQuery('Bad WQL; $or value must be a list in {}'.format(json.dumps(query)))
            query[k] = [canon_pairwise_wql(subq) for subq in query[k]]
        elif k not in WQL_1_OPS:
            qkey = canon_pairwise_tag(k)
            query[qkey] = query.pop(k)
            tag_value = query[qkey]
            if isinstance(tag_value, dict) and len(tag_value) == 1:
                if '$in' in tag_value:
                    tag_value['$in'] = [raw(val) for val in tag_value['$in']]
                else:
                    wql_op = set(tag_value.keys()).pop()  # $neq, $gt, $gt, etc.
                    tag_value[wql_op] = raw(tag_value[wql_op])
            else:
                query[canon_pairwise_tag(k)] = raw(query.pop(qkey))

    return query
