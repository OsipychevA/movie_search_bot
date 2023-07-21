import re


def parse_year_range(text: str) -> tuple[tuple[int, int] | None, str]:
    """Parses a text string to extract a range of years.

    The function expects a text string of a range of years in the format 'yyyy...yyyy",
    where each "y" represents a digit.
    It extracts the minimum and maximum year from a string and returns them as a tuple.

    Args:
        text (str): The text string to parse.

    Returns:
        tuple[tuple[int, int] | None, str]: A tuple containing the minimum and maximum year as a tuple,
        and an error message if any.

    Raises:
        None

    Example:
        parse_year_range('1850...2020')
        ((1850, 2020), '')

    """
    result = re.match(pattern=r'(\d{4}).+?(\d{4})', string=text)
    if result is None:
        return None, 'Неправильный формат. Попробуйте ещё раз.'
    min_year, max_year = map(int, result.groups())
    if min_year < 1850 or max_year < 1850:
        return None, 'Год слишком маленький. Укажите год больше 1850. Попробуйте ещё раз.'
    if min_year > max_year:
        return None, 'Минимальный год должен быть меньше чем максимальный. Попробуйте ещё раз.'
    return (min_year, max_year), ''

