# -*- coding: utf-8 -*-
import os
import sys
import unittest

from mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import shippo

from shippo.test.helper import ShippoTestCase, DUMMY_CUSTOMS_DECLARATION,\
    INVALID_CUSTOMS_DECLARATION, DUMMY_CUSTOMS_ITEM


class CustomsDeclarationTests(ShippoTestCase):
    request_client = shippo.http_client.RequestsClient

    def setUp(self):
        super(CustomsDeclarationTests, self).setUp()

        def get_http_client(*args, **kwargs):
            return self.request_client(*args, **kwargs)

        self.client_patcher = patch(
            'shippo.http_client.new_default_http_client')

        client_mock = self.client_patcher.start()
        client_mock.side_effect = get_http_client

    def tearDown(self):
        super(CustomsDeclarationTests, self).tearDown()

        self.client_patcher.stop()
        
    def test_invalid_create(self):
        self.assertRaises(shippo.error.InvalidRequestError, shippo.CustomsDeclaration.create,
                          **INVALID_CUSTOMS_DECLARATION)

    def test_create(self):
        customs_item = shippo.CustomsItem.create(**DUMMY_CUSTOMS_ITEM)
        customs_declaration_parameters = DUMMY_CUSTOMS_DECLARATION.copy()
        customs_declaration_parameters["items"][0] = customs_item.object_id
        CustomsDeclaration = shippo.CustomsDeclaration.create(**customs_declaration_parameters)
        self.assertEqual(CustomsDeclaration.object_state, 'VALID')

    def test_retrieve(self):
        customs_item = shippo.CustomsItem.create(**DUMMY_CUSTOMS_ITEM)
        customs_declaration_parameters = DUMMY_CUSTOMS_DECLARATION.copy()
        customs_declaration_parameters["items"][0] = customs_item.object_id
        CustomsDeclaration = shippo.CustomsDeclaration.create(**customs_declaration_parameters)
        # Test Retrieving Object
        retrieve = shippo.CustomsDeclaration.retrieve(CustomsDeclaration.object_id)
        self.assertItemsEqual(CustomsDeclaration, retrieve)
        
    def test_invalid_retrieve(self):
        self.assertRaises(shippo.error.APIError, shippo.CustomsDeclaration.retrieve, 
            'EXAMPLE_OF_INVALID_ID')

    def test_list_all(self):
        customs_declaration_list = shippo.CustomsDeclaration.all()
        self.assertTrue('count' in customs_declaration_list)
        self.assertTrue('results' in customs_declaration_list)

    def test_list_page_size(self):
        pagesize = 1
        customs_declaration_list = shippo.CustomsDeclaration.all(size=pagesize)
        self.assertEquals(len(customs_declaration_list.results), pagesize)

if __name__ == '__main__':
    unittest.main()