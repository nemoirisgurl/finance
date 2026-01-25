from datetime import datetime


def is_valid_date(date):
    try:
        return datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False


def calc_interest(
    principal, rate, years, monthly_contribution=0, compounds_per_year=12
):
    data = []
    r = rate / 100
    n = compounds_per_year
    for year in range(1, years + 1):
        if r == 0:
            new_principal = principal + (monthly_contribution * 12 * year)
        else:
            fv_principal = principal * (1 + r / n) ** (n * year)
            fv_contributions = monthly_contribution * (
                ((1 + r / n) ** (n * year) - 1) / (r / n)
            )
            new_principal = fv_principal + fv_contributions
        data.append(
            {
                "year": year,
                "principal": round(new_principal, 2),
            }
        )
    return data
