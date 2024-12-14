from enum import Enum

default_email = "splitzy.official@gmail.com"
DEFAULT_VERIFICATION_MESSAGE = (
    "Verification Email has been sent successfully to the user. Please verify your email to"
    " access the account."
)


class EnvironmentSettings(Enum):
    dev = "DEV"
    stg = "STAGING"
    prod = "PRODUCTION"
    qa = "QA"


TRUTH_LIST = [True, "True", "T", "true", "Y", "y", 1, "1", "Yes", "yes"]
