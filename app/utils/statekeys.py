from enum import Enum


class StateKeys(str, Enum):
    REGIONS_PAGINATION = "regions_pagination"
    PLACES_PAGINATION = "places_pagination"
    PLACES = "places"
    REGIONS = "regions"
    MAIN_MENU = "main_menu"
    BACK_TO_PLACES_LIST = "back_to_places_list"
