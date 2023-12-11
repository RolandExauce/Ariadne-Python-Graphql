# partial prisma errors:
CONSTRAINT_VIOLATION = "Unique constraint failed on the fields"


# custom errors
INVALID_DATE = "INVALID DATE! CHECK YEAR, MONTH AND DAYS, ALSO USE THIS FORMAT: YYYY.MM.DD"
UNKNOWN_ERR = "AN UNKNOWN ERROR OCCURED!"
DUPLICATE_RECORD = "NO DUPLICATES ALLOWED!"
NO_USERS = "NO USERS WERE FOUND!"
NOT_AUTHORIZED = "NO PERMISSIONS TO EXECUTE!"
NO_AUTH = "NO AUTHENTICATED USER FOUND!"

##################################################################
INVALID_TOKEN = "INVALID TOKEN OR FORMAT!"


# check if error was caught and return custom error
def custom_prisma_error_msgs(err: str) -> str:
    if CONSTRAINT_VIOLATION in err:
        return DUPLICATE_RECORD
    else:
        return err


# login validation
USER_NOT_FOUND = "SRY, BUT THIS USER DOES NOT EXIST"
WRONG_PASSWORD = "SRY, BUT A USER WITH THIS PASSWORD DOES NOT EXIST"


# success messages and error messages for user operations
def user_op_msgs(op: str, caseErr=None):
    success_msgs = {
        "CREATE": "USER WAS CREATED SUCCESSFULLY",
        "DELETE": "USER WAS DELETED SUCCESSFULLY",
        "UPDATE": "USER WAS UPDATED SUCCESSFULLY"
    }

    error_msgs = {
        "CREATE": "FAILED TO CREATE USER",
        "DELETE": "FAILED TO DELETE USER",
        "UPDATE": "FAILED TO UPDATE USER"
    }

    if op in success_msgs and caseErr is None:
        return success_msgs[op]
    elif op in error_msgs and caseErr == "FAILED":
        return error_msgs[op]
    else:
        return "INVALID OPERATION"
