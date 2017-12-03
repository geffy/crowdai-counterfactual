#!/usr/bin/env python

from __future__ import print_function
import utils
import hashlib
import gzip

class CriteoDataset:
    def __init__(self, filepath, isTest=False, isGzip=False, id_map=False, debug=False):
        if filepath.endswith(".gz") or isGzip:
            self.fp = gzip.open(filepath, "rb")
        else:
            self.fp = open(filepath, "rb")
        self.debug = debug
        self.isTest = isTest
        """
            `isTest` is a boolean value which signals that this file does not
            have `cost` and `propensity` information available for any impressions
        """
        self.id_map = id_map
        """
            id_map is an optional function which can be used to transform the `impression_id` to another value
            a simple example could be :
            ```
            def _f(x):
                return x+"_postfix"
            ```
        """
        self.line_buffer = []

    def __iter__(self):
        return self

    def next(self):
        next_block = self.get_next_impression_block()
        if next_block:
            return next_block
        else:
            raise StopIteration

    def __next__(self):
        return self.next()

    def get_next_line(self):
        try:
            line = self.fp.readline()
            return str(line, 'utf-8')
        except StopIteration:
            return False

    def get_next_impression_block(self):
        # Obtain the first line of an impression block
        assert len(self.line_buffer) <= 1
        if len(self.line_buffer) == 0:
            line = self.get_next_line()
            if not line:
                return False
        else:
            line = self.line_buffer.pop()

        block_impression_id = utils.extract_impression_id(line)
        if self.id_map:
            block_impression_id = self.id_map(block_impression_id)

        if not self.isTest:
            cost, propensity = utils.extract_cost_propensity(line)

        candidate_features = [utils.extract_features(line, self.debug)]

        while True:
            line = self.get_next_line()
            if not line: #EOF
                break

            line_impression_id = utils.extract_impression_id(line)
            if self.id_map:
                line_impression_id = self.id_map(line_impression_id)

            if line_impression_id != block_impression_id:
                # Save the line in the line_buffer
                self.line_buffer.append(line)
                break
            else:
                candidate_features.append(utils.extract_features(line, debug=self.debug))

        _response = {}
        _response["id"] = block_impression_id
        _response["candidates"] = candidate_features
        if not self.isTest:
            _response["cost"] = cost
            _response["propensity"] = propensity
        return  _response

    def close(self):
        self.__del__()

    def __del__(self):
        self.fp.close()
