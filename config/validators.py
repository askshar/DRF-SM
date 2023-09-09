from accounts.models import UserPasswordHistoryMananger


def password_validator(password=None):
    if password:
        if not len(password) >= 6:
            return False

        has_letter = any(char.isalpha() for char in password)
        has_number = any(char.isdigit() for char in password)
        has_symbol = any(char in '@#$&' for char in password)

        return has_letter and has_number and has_symbol
    return False


def password_history_validator(user, password=None):
    passwords = UserPasswordHistoryMananger.objects.filter(
        user=user).order_by('-created_at')

    if len(passwords) > 3:
        passwords_to_delete = passwords[4:]
        passwords_to_delete.delete()

    for value in passwords:
        if value.password == password:
            return True
    return False
