"""A set of constants relating to UK taxing."""
import numpy as np
from enum import Enum

DEFAULT_TAX_FREE_ALLOWANCE = 12570


class TIME_SCALES(Enum):
    PER_ANUM = 0
    WEEKLY = 1
    MONTHLY = 2
    QUARTERLY = 3
    YEARLY = 4


class IN_OUT_GOINGS(Enum):
    MONTHLY_FIXED = 0
    MONTHLY_ALLOWED = 1
    MONTHLY_FIXED_LEISURE = 2
    ENTERTAINMENT = 3
    PLANNED_PAYMENT = 4


INCOME_TAX = {  # https://www.gov.uk/income-tax-rates
    TIME_SCALES.PER_ANUM: {
        "Lower": {"Value": DEFAULT_TAX_FREE_ALLOWANCE, "Rate": 0},
        "Upper": {"Value": 50271, "Rate": 0.2},
        "Higher": {"Value": 150000, "Rate": 0.4},
        "Highest": {"Value": np.inf, "Rate": 0.45},
    }
}

NATIONAL_INSURANCE = {  # https://www.gov.uk/national-insurance
    TIME_SCALES.WEEKLY: {
        "Lower": {"Value": 184, "Rate": 0},
        "Upper": {"Value": 967, "Rate": 0.12},
        "Higher": {"Value": np.inf, "Rate": 0.02},
    }
}
