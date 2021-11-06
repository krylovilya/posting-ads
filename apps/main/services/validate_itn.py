from django.core.exceptions import ValidationError


def validate_itn(itn):
    """Валидатор для поля itn в модели Seller."""
    if not check_itn(itn):
        raise ValidationError(
            'ИНН некорректен',
            params={'itn': itn},
        )


def check_itn(itn: str) -> bool:
    """Проверка ИНН."""
    if len(itn) not in (10, 12):
        return False

    def itn_csum(_itn):
        k = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
        pairs = zip(k[11 - len(_itn):], [int(x) for x in _itn])
        return str(sum([k * v for k, v in pairs]) % 11 % 10)

    if len(itn) == 10:
        return itn[-1] == itn_csum(itn[:-1])
    else:
        return itn[-2:] == itn_csum(itn[:-2]) + itn_csum(itn[:-1])
