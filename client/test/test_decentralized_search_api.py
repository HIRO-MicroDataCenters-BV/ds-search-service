# coding: utf-8

"""
    Data Space Search Service

    The Search Service is a service of the Data Space Node, designed to process search queries and aggregate results from decentralized catalogs.

    The version of the OpenAPI document: 0.1.0
    Contact: all-hiro@hiro-microdatacenters.nl
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from ds_search_service.api.decentralized_search_api import DecentralizedSearchApi


class TestDecentralizedSearchApi(unittest.TestCase):
    """DecentralizedSearchApi unit test stubs"""

    def setUp(self) -> None:
        self.api = DecentralizedSearchApi()

    def tearDown(self) -> None:
        pass

    def test_decentralized_search(self) -> None:
        """Test case for decentralized_search

        Search Local Catalog
        """
        pass


if __name__ == '__main__':
    unittest.main()
