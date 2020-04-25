import os


def load_token() -> str:
    if is_prod_test_mode():
        return os.environ["SLACK_SDK_TEST_GRID_ORG_ADMIN_USER_TOKEN"]
    else:
        return "xoxp-123-123"


def is_prod_test_mode() -> bool:
    return "SLACK_SCIM_TEST_MODE" in os.environ and \
           os.environ["SLACK_SCIM_TEST_MODE"].startswith("prod")
