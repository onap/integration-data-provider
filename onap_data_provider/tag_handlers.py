"""Custom yaml tag handlers module."""
"""
   Copyright 2021 Deutsche Telekom AG

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
import yaml
import uuid


def join(loader: yaml.SafeLoader, node: yaml.Node) -> str:
    """Concatinates the nodes fields for !join tag.

    Concatinates multiple strings in yaml value f.e. !join [a, b, c] results in 'abc'.
    join supports separator syntax f.e. !join ['_', [a, b, c]] results in 'a_b_c'.

    Args:
        node (yaml.Node): the yaml node

    Returns:
        str: the joined string of node

    """
    seq = loader.construct_sequence(node, deep=True)  # type: ignore
    if len(seq) == 2 and isinstance(seq[0], str) and isinstance(seq[1], list):
        sep = seq[0]
        return sep.join([str(i) for i in seq[1]])
    else:
        return "".join([str(i) for i in seq])


def generate_random_uuid(*_) -> str: # type: ignore
    """Random UUID generator.

    Args:
        loader (yaml.SafeLoader): SafeLoader object
        node (yaml.Node): Node object

    Returns:
        str: randomly generated UUID
    """
    return str(uuid.uuid4())
