import pytest
from run import create_user_details


def test_mask():
    """
    Unit testing if the data mask is working for device_type and ip.
    """
    user_details_list = []

    messages = [
        {
            "user_id": "neil_caffery",
            "device_type": "ios",
            "ip": "10.10.200.200",
            "device_id": "202315",
            "locale": "en",
            "app_version": "1.3",
            "date": "2023-09-21"
        },
        {
            "user_id": "peter_burke",
            "device_type": "android",
            "ip": "40.20.220.300",
            "device_id": "202318",
            "locale": "en",
            "app_version": "2",
            "date": "2023-09-22"
        }
    ]

    for message in messages:
        record = create_user_details(message)
        user_details_list.append(record)

    assert user_details_list[0].masked_ip == "8a2dc3f42a173040385ab044adf6e26f3ee772743b0c7524bd0fcc5ecb077051e5eae7e3d50395444154fd25c852f0d5edb7ca802aa84b61d7949112b1033e4f"
    assert user_details_list[0].masked_device_id == "394247e211c2664c3cd12ebae6c5b3a69711761b1b4c8d0930af7782da1e24058b7c8649170f62ba4b53e5b3332fc93b0529678f986326679bdf5468124252c3"
    assert user_details_list[1].masked_ip == "0d60eb7a01c81bf41783d79855db976cc718dfb659664c186c590d79cf9508658405d9bf1a5ae2538f3f14a7b095062ef1ee30ee04231b56e9f1a6a1c34c6808"
    assert user_details_list[1].masked_device_id == "c61ac3ed765c8039b0059b58223ddf0f705bc0cae2016ed604306a93be743bb1df6f4d2ba376292d112af022525873d2384a625eaa533943b72000074878dc47"