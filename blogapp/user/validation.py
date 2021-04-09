def validate(data):
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if (password != confirm_password):
        return {
            "error": "Password does not match.",
            "success": False
        }

    if len(password) < 8:
        return{
            "error": "Password is too short.",
            "success": False
        }

    if len(password) > 15:
        return{
            "error": "Password is too long.",
            "success": False
        }



def is_valid_pass(password):
    pass