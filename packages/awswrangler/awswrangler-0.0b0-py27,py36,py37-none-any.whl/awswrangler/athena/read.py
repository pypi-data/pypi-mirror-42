import pandas as pd

from ..common import get_session
from ..athena.utils import run_query, query_validation


def read(
    database, query, s3_output=None, region=None, key=None, secret=None, profile=None
):
    """
    Read any Glue object through the AWS Athena
    """
    session = get_session(key=key, secret=secret, profile=profile, region=region)
    if not s3_output:
        account_id = session.client("sts").get_caller_identity().get("Account")
        session_region = session.region_name
        s3_output = (
            "s3://aws-athena-query-results-" + account_id + "-" + session_region + "/"
        )
        s3 = session.resource("s3")
        s3.Bucket(s3_output)
    athena_client = session.client("athena")
    qe = run_query(athena_client, query, database, s3_output)
    validation = query_validation(athena_client, qe)
    if validation["QueryExecution"]["Status"]["State"] == "FAILED":
        message_error = (
            "Your query is not valid: "
            + validation["QueryExecution"]["Status"]["StateChangeReason"]
        )
        raise Exception(message_error)
    else:
        file = s3_output + qe + ".csv"
        df = pd.read_csv(file)
    return df
