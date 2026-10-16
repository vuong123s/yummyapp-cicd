import unittest
from unittest.mock import patch
from yummy_app import YummyApp
import gps_service


# ================================================================
# CAP DO 1: Bo test co ban cho san (Moi chi dat ~35% Coverage)
# ================================================================
class TestEasyLevel(unittest.TestCase):
    """Kiem thu chuc nang co ban tinh tien don hang"""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}
        self.assertEqual(self.app.calculate_order_total(cart), 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}
        self.assertEqual(self.app.calculate_order_total(cart), 0.0)


# ================================================================
# CAP DO 2 (TIET 3): SINH VIEN TU TAY LAP TRINH TEST CASE DUOI DAY
# (Sau khi da hoan thanh Ban thiet ke test case viet tay tren giay)
# ================================================================
class TestMediumLevel(unittest.TestCase):
    """Kiem thu cac kich ban cho apply_promo_code"""

    def test_apply_promo_online_valid(self):
        """Kich ban 1: Online hop le, ap dung ma GIAM10 thanh cong (giam 10%)"""
        app = YummyApp(network_status="online", os_version=15)
        result = app.apply_promo_code(100000.0, "GIAM10")
        self.assertEqual(result, 90000.0)

    def test_apply_promo_offline_raises_connection_error(self):
        """Kich ban 2: Offline nem ConnectionError"""
        app = YummyApp(network_status="offline", os_version=15)
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000.0, "GIAM10")

    def test_apply_promo_special_code_os15(self):
        """Kich ban 3: Ma dac biet NEW_OS_ONLY tren OS 15 thanh cong (giam 20%)"""
        app = YummyApp(network_status="online", os_version=15)
        result = app.apply_promo_code(100000.0, "NEW_OS_ONLY")
        self.assertEqual(result, 80000.0)

    def test_apply_promo_special_code_os14_raises_value_error(self):
        """Kich ban 4: Ma dac biet NEW_OS_ONLY tren OS 14 nem ValueError"""
        app = YummyApp(network_status="online", os_version=14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000.0, "NEW_OS_ONLY")

    def test_apply_promo_invalid_code_raises_value_error(self):
        """Kich ban bo sung: Ma khuyen mai khong ton tai trong he thong"""
        app = YummyApp(network_status="online", os_version=15)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000.0, "INVALID_CODE")


class TestHardLevel(unittest.TestCase):
    """Kiem thu chuc nang tim nha hang su dung Mocking GPS"""

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_nearby_restaurants_in_range(self, mock_get_location):
        """Kich ban 5: Mock GPS trong vung (10.0, 105.0) -> tra ve danh sach nha hang"""
        mock_get_location.return_value = (10.0, 105.0)
        app = YummyApp()
        restaurants = app.get_nearby_restaurants()
        self.assertEqual(
            restaurants,
            ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"]
        )
        mock_get_location.assert_called_once()

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_nearby_restaurants_out_of_range(self, mock_get_location):
        """Kich ban 6: Mock GPS ngoai vung (20.0, 110.0) -> tra ve danh sach rong"""
        mock_get_location.return_value = (20.0, 110.0)
        app = YummyApp()
        restaurants = app.get_nearby_restaurants()
        self.assertEqual(restaurants, [])
        mock_get_location.assert_called_once()

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_nearby_restaurants_signal_lost(self, mock_get_location):
        """Kich ban 7: Mock GPS nem GPSSignalLostError -> tra ve thong bao loi"""
        mock_get_location.side_effect = gps_service.GPSSignalLostError()
        app = YummyApp()
        result = app.get_nearby_restaurants()
        self.assertEqual(result, "Khong the xac dinh vi tri.")
        mock_get_location.assert_called_once()

    def test_gps_service_direct_call(self):
        """Kiem thu ham goc get_current_location de dat 100% coverage"""
        coords = gps_service.get_current_location()
        self.assertEqual(coords, (10.0, 105.0))


if __name__ == '__main__':
    unittest.main()
