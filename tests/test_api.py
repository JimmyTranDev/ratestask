from tests.test_base import TestBase
from ratestask.app import create_app
from flask import Flask
import unittest
import json


class ApiTest(TestBase):
    app: Flask

    def setUp(self):
        super(ApiTest, self).setUp()
        self.app = create_app()

    def test_rates_invalid_origin_destination(self):
        ''' Test rates api with invalid origin and destination'''

        client = self.app.test_client()
        queries = { "date_from": "2016-01-01", "date_to": "2016-01-02", "origin": "AAAA", "destination": "AAAA"}

        test_regions = [
            {"slug": "china_south_main", "name": "China South Main", "parent_slug": None },
            {"slug": "north_europe_main", "name": "North Europe Main", "parent_slug": None },
        ]

        test_ports = [
            {"code": "CNSGH", "name": "Shanghai", "parent_slug": "china_south_main"},
            {"code": "NLRTM", "name": "Rotterdam", "parent_slug": "north_europe_main"},
        ]

        test_rates = [
            {"day": "2016-01-01", "price": 1000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-01", "price": 3000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-01", "price": 2000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-02", "price": 1000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-02", "price": 1000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-02", "price": 1000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
        ]

        cur = self.cur
        self.insertWithDict(cur, table_name="regions", data_dicts=test_regions)
        self.insertWithDict(cur, table_name="ports", data_dicts=test_ports)
        self.insertWithDict(cur, table_name="prices", data_dicts=test_rates)

        resp = client.get("/rates", query_string=queries)
        self.assertEqual(resp.status_code, 200)
        daily_rates = json.loads(resp.data)
        self.assertEqual(len(daily_rates), 0)


    def test_rates_from_date_larger_than_to_date(self):
        ''' Test rates api with invalid dates'''

        client = self.app.test_client()
        queries = { "date_from": "2016-01-02", "date_to": "2016-01-01", "origin": "CNSGH", "destination": "NLRTM"}
        resp = client.get("/rates", query_string=queries)
        self.assertEqual(resp.status_code, 400)


    def test_rates_invalid_date(self):
        ''' Test rates api with invalid dates'''

        client = self.app.test_client()
        queries = { "date_from": "2016-01-01", "date_to": "2017-02-29", "origin": "CNSGH", "destination": "NLRTM"}
        resp = client.get("/rates", query_string=queries)
        self.assertEqual(resp.status_code, 400)
        
        client = self.app.test_client()
        queries = { "date_from": "2016-01-01", "date_to": "2016-02-29", "origin": "CNSGH", "destination": "NLRTM"}
        resp = client.get("/rates", query_string=queries)
        self.assertEqual(resp.status_code, 200)

        client = self.app.test_client()
        queries = { "date_from": "2016-01-01", "date_to": "30-01-2016", "origin": "CNSGH", "destination": "NLRTM"}
        resp = client.get("/rates", query_string=queries)
        self.assertEqual(resp.status_code, 400)

        client = self.app.test_client()
        queries = { "date_from": "2016-01-01", "date_to": "2016-01-66", "origin": "CNSGH", "destination": "NLRTM"}
        resp = client.get("/rates", query_string=queries)
        self.assertEqual(resp.status_code, 400)

        queries = { "date_from": "32016-01-01", "date_to": "2016-01-02", "origin": "CNSGH", "destination": "NLRTM"}
        resp = client.get("/rates", query_string=queries)
        self.assertEqual(resp.status_code, 400)

    def test_rates_missing_required_query(self):
        ''' Test rates api with missing queries'''

        client = self.app.test_client()
        
        queries = {
            # date_from missing
            "date_to": "2016-01-02", 
            "origin": "china_south_main", 
            "destination": "north_europe_main"
        }
        resp = client.get("/rates", query_string=queries)
        self.assertEqual(resp.status_code, 400)
        
        queries = { 
            "date_from": "2016-01-01",
            # date_to missing
            "origin": "china_south_main", 
            "destination": "north_europe_main"
        }
        resp = client.get("/rates", query_string=queries)
        self.assertEqual(resp.status_code, 400)
        
        queries = { 
            "date_from": "2016-01-01", 
            "date_to": "2016-01-02", 
            # origin missing
            "destination": "north_europe_main"
        }
        resp = client.get("/rates", query_string=queries)
        self.assertEqual(resp.status_code, 400)
        
        queries = { 
            "date_from": "2016-01-01", 
            "date_to": "2016-01-02", 
            "origin": "china_south_main"
            # destination missing
        }
        resp = client.get("/rates", query_string=queries)
        self.assertEqual(resp.status_code, 400)

    def test_rates_nested_region(self):
        ''' Test rates api with nested region'''

        client = self.app.test_client()
        queries = { "date_from": "2016-01-01", "date_to": "2016-01-03", "origin": "asia_main", "destination": "north_europe_main"}

        test_regions = [
            {"slug": "asia_main", "name": "asia", "parent_slug": None },
            {"slug": "china_south_main", "name": "China South Main", "parent_slug": "asia_main" },
            {"slug": "north_europe_main", "name": "North Europe Main", "parent_slug": None },
        ]

        test_ports = [
            {"code": "CNSGH", "name": "Shanghai", "parent_slug": "china_south_main"},
            {"code": "NLRTM", "name": "Rotterdam", "parent_slug": "north_europe_main"},
        ]

        test_rates = [
            {"day": "2016-01-01", "price": 1000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-01", "price": 3000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-01", "price": 2000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-02", "price": 1000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-02", "price": 1000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-02", "price": 1000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-03", "price": 5000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-03", "price": 5000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
        ]

        cur = self.cur
        self.insertWithDict(cur, table_name="regions", data_dicts=test_regions)
        self.insertWithDict(cur, table_name="ports", data_dicts=test_ports)
        self.insertWithDict(cur, table_name="prices", data_dicts=test_rates)

        resp = client.get("/rates", query_string=queries)
        self.assertEqual(resp.status_code, 200)

        daily_rates = json.loads(resp.data)
        self.assertEqual(len(daily_rates), 3)

        daily_rate_1, daily_rate_2, daily_rate_3 = daily_rates

        self.assertIsNotNone(daily_rate_1.get("average_price"))
        self.assertIsNotNone(daily_rate_2.get("average_price"))
        self.assertIsNone(daily_rate_3.get("average_price"))

        self.assertEqual(daily_rate_1["average_price"], 2000)
        self.assertEqual(daily_rate_2["average_price"], 1000)

        self.assertEqual(daily_rate_1["day"], "2016-01-01")
        self.assertEqual(daily_rate_2["day"], "2016-01-02")
        self.assertEqual(daily_rate_3["day"], "2016-01-03")


    def test_rates_region(self):
        ''' Test rates api with region'''

        client = self.app.test_client()
        queries = { "date_from": "2016-01-01", "date_to": "2016-01-03", "origin": "china_south_main", "destination": "north_europe_main"}

        test_regions = [
            {"slug": "china_south_main", "name": "China South Main", "parent_slug": None },
            {"slug": "north_europe_main", "name": "North Europe Main", "parent_slug": None },
        ]

        test_ports = [
            {"code": "CNSGH", "name": "Shanghai", "parent_slug": "china_south_main"},
            {"code": "NLRTM", "name": "Rotterdam", "parent_slug": "north_europe_main"},
        ]

        test_rates = [
            {"day": "2016-01-01", "price": 1000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-01", "price": 3000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-01", "price": 2000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-02", "price": 1000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-02", "price": 1000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-02", "price": 1000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-03", "price": 5000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-03", "price": 5000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
        ]

        cur = self.cur
        self.insertWithDict(cur, table_name="regions", data_dicts=test_regions)
        self.insertWithDict(cur, table_name="ports", data_dicts=test_ports)
        self.insertWithDict(cur, table_name="prices", data_dicts=test_rates)

        resp = client.get("/rates", query_string=queries)
        self.assertEqual(resp.status_code, 200)

        daily_rates = json.loads(resp.data)
        self.assertEqual(len(daily_rates), 3)

        daily_rate_1, daily_rate_2, daily_rate_3 = daily_rates

        self.assertIsNotNone(daily_rate_1.get("average_price"))
        self.assertIsNotNone(daily_rate_2.get("average_price"))
        self.assertIsNone(daily_rate_3.get("average_price"))

        self.assertEqual(daily_rate_1["average_price"], 2000)
        self.assertEqual(daily_rate_2["average_price"], 1000)

        self.assertEqual(daily_rate_1["day"], "2016-01-01")
        self.assertEqual(daily_rate_2["day"], "2016-01-02")
        self.assertEqual(daily_rate_3["day"], "2016-01-03")

    def test_rates_port_codes(self):
        ''' Test rates api with port codes'''
        client = self.app.test_client()
        queries = { "date_from": "2016-01-01", "date_to": "2016-01-03", "origin": "CNSGH", "destination": "NLRTM"}

        test_regions = [
            {"slug": "china_south_main", "name": "China South Main", "parent_slug": None },
            {"slug": "north_europe_main", "name": "North Europe Main", "parent_slug": None },
        ]

        test_ports = [
            {"code": "CNSGH", "name": "Shanghai", "parent_slug": "china_south_main"},
            {"code": "NLRTM", "name": "Rotterdam", "parent_slug": "north_europe_main"},
        ]

        test_rates = [
            {"day": "2016-01-01", "price": 1000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-01", "price": 3000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-01", "price": 2000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-02", "price": 1000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-02", "price": 1000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-02", "price": 1000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-03", "price": 5000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
            {"day": "2016-01-03", "price": 5000, "orig_code": "CNSGH", "dest_code": "NLRTM"},
        ]

        cur = self.cur
        self.insertWithDict(cur, table_name="regions", data_dicts=test_regions)
        self.insertWithDict(cur, table_name="ports", data_dicts=test_ports)
        self.insertWithDict(cur, table_name="prices", data_dicts=test_rates)

        resp = client.get("/rates", query_string=queries)
        self.assertEqual(resp.status_code, 200)

        daily_rates = json.loads(resp.data)
        self.assertEqual(len(daily_rates), 3)

        daily_rate_1, daily_rate_2, daily_rate_3 = daily_rates

        self.assertIsNotNone(daily_rate_1.get("average_price"))
        self.assertIsNotNone(daily_rate_2.get("average_price"))
        # Is none since the amount of prices < 3
        self.assertIsNone(daily_rate_3.get("average_price")) 

        self.assertEqual(daily_rate_1["average_price"], 2000)
        self.assertEqual(daily_rate_2["average_price"], 1000)

        self.assertEqual(daily_rate_1["day"], "2016-01-01")
        self.assertEqual(daily_rate_2["day"], "2016-01-02")
        self.assertEqual(daily_rate_3["day"], "2016-01-03")



if __name__ == "__main__":
    unittest.main(exit=False)
