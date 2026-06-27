import pytest
from utils.api_helper import APIHelper
from utils.config_reader import ConfigReader

class TestDummyJSONProductsAPI:
    """API tests for the DummyJSON products resource."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.api_helper = APIHelper(base_url= ConfigReader.get_api_base_url())
        yield
        self.api_helper.close_session()

    @pytest.mark.get
    def test_get_product(self):
        # call api  voi endpoint la "/products/1" de lay thong tin san pham co id = 1
        response = self.api_helper.get("/product/1")

        # response = self.api_helper.get("/products",params={"limit":2},)
        assert response.status_code == 200
        product = response.json()
        assert product["id"] == 1
        assert product["title"] == 'Essence Mascara Lash Princess'


    # @pytest.mark.post
    # def test_create_product(self):
    #     payload = {
    #         "title": "Automation Test Product",
    #         "price": 99.99,
    #         "category": "test",
    #     }

    #     response = self.api_helper.post("/products/add", json_data=payload)

    #     assert response.status_code in (200, 201)
    #     created_product = response.json()
    #     print("print full reponse", response.json())
    #     assert created_product["id"] > 0
    #     assert created_product["title"] == payload["title"]
    #     assert created_product["price"] == payload["price"]

    # def test_update_product(self):
    #     payload = {
    #         "title": "Updated Automation Test Product",
    #         "price": 149.99,
    #     }

    #     response = self.api_helper.put("/products/1", json_data=payload)

    #     assert response.status_code == 200
    #     updated_product = response.json()
    #     assert updated_product["id"] == 1
    #     assert updated_product["title"] == payload["title"]
    #     assert updated_product["price"] == payload["price"]

    # def test_delete_product(self):
    #     response = self.api_helper.delete("/products/1")

    #     assert response.status_code == 200
    #     deleted_product = response.json()
    #     assert deleted_product["id"] == 1
    #     assert deleted_product["isDeleted"] is True
    #     assert deleted_product["deletedOn"]