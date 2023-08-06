#
# Copyright 2015 Quantopian, Inc.
# Modifications Copyright 2018 Alpaca
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pickle
import os

VERSION_LABEL = '_stateversion_'
CHECKSUM_KEY = '__state_checksum'


class StateStore:

    def __init__(self, path):
        self.path = path

    def save(self, context, checksum, exclude_list):
        state = {}
        fields_to_store = list(set(context.__dict__.keys()) -
                               set(exclude_list))

        for field in fields_to_store:
            state[field] = getattr(context, field)

        state[CHECKSUM_KEY] = checksum

        with open(self.path, 'wb') as f:
            pickle.dump(state, f)

    def load(self, context, checksum):
        if not os.path.exists(self.path) or not os.stat(self.path).st_size:
            return

        with open(self.path, 'rb') as f:
            try:
                loaded_state = pickle.load(f)
            except (pickle.UnpicklingError, IndexError):
                raise ValueError("Corrupt state file: {}".format(self.path))

        if CHECKSUM_KEY not in loaded_state or \
                loaded_state[CHECKSUM_KEY] != checksum:
            raise ValueError(
                "Checksum mismatch during state load. "
                "The given state file was not created "
                "for the algorithm in use")

        del loaded_state[CHECKSUM_KEY]

        for k, v in loaded_state.items():
            setattr(context, k, v)
