#!/usr/bin/env python3
"""One place that knows what a currency CODE means, shared by every report script.

WHY THIS EXISTS (2026-08-01, found by an outside adversarial review).

Some exchanges quote share prices in a currency's SMALL unit. London quotes in
pence, and the code for pence is `GBp` — the same three letters as `GBP`, pounds,
differing only in the case of the last letter. Reading one as the other is a
hundredfold error.

`data/trigger_sweep.py` already knew this and checked the code BEFORE folding its
case. `data/eod_report.py` did not: it called `.upper()` on the code first, so
`GBp` became `GBP`, and an approved order of 500 pence printed to Ben's phone as
**£500.00** when it means **£5.00**. Two files, two answers, one of them off by a
factor of a hundred, in the message that reaches his phone.

That is this engine's most common defect shape: two objects that look the same
(`GBp` and `GBP`) and a rule in prose telling the next reader to tell them apart.
The fix is structural — one module, imported by all four report scripts, so there
is only one place where a code becomes money and no script can invent its own
answer.

Two rules this module enforces:

  1. THE CODE IS READ AS RECORDED. `GBp` is never uppercased before the small-unit
     check. It is the only code whose upper-case form collides with a real
     currency, so it is matched case-sensitively; every other small-unit code
     (GBX, ZAc, ILA, USX) has no such collision and is matched either way.

  2. A CURRENCY IS NEVER GUESSED FROM A TICKER SUFFIX. `.L` is the London
     exchange, and London lists instruments priced in pence, in pounds and in
     dollars — the suffix does not say which. Callers pass the currency that was
     RECORDED for the instrument (the `ccy` column of triggers.csv or
     approved_orders.csv, the `price_ccy` column of watchlist.csv, or the price
     vendor's own currency field returned beside the price series). When nothing
     was recorded, the number prints bare: a missing symbol is recoverable, a
     guessed one is not.

Usage:
    from currency_units import format_money, unit
    format_money(500, "GBp")   -> '£5.00 (500 pence)'
    format_money(500, "GBP")   -> '£500.00'
    format_money(1718000, "KRW") -> '₩1,718,000'
    unit("GBp").major, unit("GBp").per_major   -> ('GBP', 100)
"""

from __future__ import annotations

from collections import namedtuple

# --------------------------------------------------------------- small units
# A currency code that names the SMALL unit, mapped to (major code, how many of
# the small unit make one major unit, what the small unit is called).
#
# `GBp` is here on its own because `"GBp".upper() == "GBP"`, a different currency.
# Matching it needs the exact string. Everything in _SMALL_ANY_CASE has an
# upper-case form that is not a currency of its own, so case cannot confuse it.
_SMALL_EXACT = {
    "GBp": ("GBP", 100, "pence"),
    "GBp-pence": ("GBP", 100, "pence"),   # long form seen in triggers.csv
}
_SMALL_ANY_CASE = {
    "GBX": ("GBP", 100, "pence"),     # London, the ISO-style spelling of pence
    "ZAC": ("ZAR", 100, "cents"),     # Johannesburg quotes in cents ("ZAc")
    "ILA": ("ILS", 100, "agorot"),    # Tel Aviv quotes in agorot
    "USX": ("USD", 100, "cents"),     # US sub-dollar quoting convention
}

# --------------------------------------------------------------- major units
_SYMBOL = {
    "USD": "$", "EUR": "€", "GBP": "£", "KRW": "₩", "JPY": "¥", "HKD": "HK$",
    "TWD": "NT$", "CAD": "C$", "AUD": "A$", "CHF": "CHF ", "BRL": "R$",
    "CNY": "CN¥", "SGD": "S$", "INR": "₹", "ZAR": "R", "ILS": "₪",
    "NZD": "NZ$", "MXN": "MX$", "TRY": "₺", "THB": "฿", "PHP": "₱",
    "SEK": "SEK ", "NOK": "NOK ", "DKK": "DKK ", "PLN": "PLN ", "IDR": "Rp",
}
# The renminbi is written CN¥ rather than ¥ on purpose: the yen already owns ¥,
# and two currencies sharing one symbol is the same "two objects, one shape"
# trap that produced the pence bug.

# Currencies with no sub-unit in normal share-price quoting. '₩1,718,000' beats
# '1,718,000.00 KRW', and the trailing '.00' is noise nobody reads.
#
# RECONCILED 2026-08-01. The Taiwan dollar used to be here in eod_report.py and
# trigger_sweep.py (zero decimals) while timing_gauge.py and wake_check.py printed
# it with two. The Taiwan Stock Exchange quotes shares to two decimals below
# NT$10 (tick NT$0.01), so zero decimals silently rounds a real price away.
# Two decimals is now the single answer everywhere. The won and the yen genuinely
# have no sub-unit in equity quoting and keep zero.
_DECIMALS = {"KRW": 0, "JPY": 0, "IDR": 0, "CLP": 0, "VND": 0, "HUF": 0, "ISK": 0}
DEFAULT_DECIMALS = 2


class Unit(namedtuple("Unit", "recorded major per_major small_name symbol decimals")):
    """What one recorded currency code means.

    recorded    the code exactly as it was written down ('GBp')
    major       the currency it belongs to ('GBP'), or '' when unrecognised
    per_major   how many recorded units make one major unit (100 for pence, else 1)
    small_name  'pence' / 'cents' / 'agorot', or '' when the code IS the major unit
    symbol      '£', or '' when the currency has no short symbol
    decimals    how many decimal places the MAJOR amount is written to
    """

    __slots__ = ()

    @property
    def is_small_unit(self):
        """True when the recorded code names pence/cents/agorot rather than the currency."""
        return self.per_major != 1

    @property
    def known(self):
        return bool(self.major)

    def to_major(self, value):
        """500 pence -> 5.0 pounds. The number Ben should read as money."""
        return float(value) / self.per_major


def unit(code):
    """Resolve a recorded currency code into (major currency, scale) and how to print it.

    The small-unit check runs on the code AS RECORDED, before any case folding —
    that ordering is the whole point of this module. `unit('GBp')` is pence and
    `unit('GBP')` is pounds; nothing here may ever make them the same object.
    """
    raw = (code or "").strip()
    if not raw:
        return Unit("", "", 1, "", "", DEFAULT_DECIMALS)

    small = _SMALL_EXACT.get(raw) or _SMALL_ANY_CASE.get(raw.upper())
    if small:
        major, per, name = small
        return Unit(raw, major, per, name, _SYMBOL.get(major, ""),
                    _DECIMALS.get(major, DEFAULT_DECIMALS))

    major = raw.upper()
    if major in _SYMBOL or major in _DECIMALS or len(major) == 3:
        return Unit(raw, major, 1, "", _SYMBOL.get(major, ""),
                    _DECIMALS.get(major, DEFAULT_DECIMALS))
    return Unit(raw, "", 1, "", "", DEFAULT_DECIMALS)


def format_money(value, code, with_small=True):
    """The amount as money, with the currency always named.

        format_money(500, 'GBp')     -> '£5.00 (500 pence)'
        format_money(500, 'GBP')     -> '£500.00'
        format_money(1718000, 'KRW') -> '₩1,718,000'
        format_money(2425, 'TWD')    -> 'NT$2,425.00'
        format_money(12.5, 'CZK')    -> '12.50 CZK'
        format_money(12.5, '')       -> '12.50'

    A small-unit code prints the MONEY first and the figure as it was recorded in
    brackets, so the sentence can never be read as a hundred times the real amount
    and still ties back to the number written on the row. Pass with_small=False
    where the brackets will not fit.

    An unrecognised or missing code prints the bare number. That is deliberate:
    a missing symbol is recoverable, a guessed one is the dollars-read-as-euros
    error this book has already made.
    """
    try:
        v = float(value)
    except (TypeError, ValueError):
        return str(value)

    u = unit(code)
    if not u.known:
        return f"{v:,.{DEFAULT_DECIMALS}f}"

    if u.is_small_unit:
        major_txt = _plain(u.to_major(v), u)
        if not with_small:
            return major_txt
        return f"{major_txt} ({v:,.0f} {u.small_name})"
    return _plain(v, u)


def _plain(v, u):
    """'£5.00' when the currency has a symbol, '12.50 PLN' when it does not."""
    if u.symbol:
        return f"{u.symbol}{v:,.{u.decimals}f}"
    return f"{v:,.{u.decimals}f} {u.major}".strip()


def same_currency(a, b):
    """Do two recorded codes describe the same money? 'GBp' and 'GBP' do; a
    figure in one is a hundred times a figure in the other, so callers that add
    or compare amounts must convert with to_major() first."""
    return unit(a).major == unit(b).major and bool(unit(a).major)


if __name__ == "__main__":  # a runnable statement of what this module promises
    cases = [
        (500, "GBp", "£5.00 (500 pence)"),
        (500, "GBX", "£5.00 (500 pence)"),
        (500, "GBP", "£500.00"),
        (430, "GBp", "£4.30 (430 pence)"),
        (500, "ZAc", "R5.00 (500 cents)"),
        (500, "ILA", "₪5.00 (500 agorot)"),
        (500, "USX", "$5.00 (500 cents)"),
        (1718000, "KRW", "₩1,718,000"),
        (2425, "TWD", "NT$2,425.00"),
        (7.94, "USD", "$7.94"),
        (29.97, "EUR", "€29.97"),
        (12.5, "PLN", "PLN 12.50"),
        (12.5, "CZK", "12.50 CZK"),
        (12.5, "", "12.50"),
    ]
    bad = 0
    for value, code, want in cases:
        got = format_money(value, code)
        ok = got == want
        bad += not ok
        print(f"{'ok  ' if ok else 'FAIL'} format_money({value!r}, {code!r}) = {got!r}"
              + ("" if ok else f"  expected {want!r}"))
    print(f"\nunit('GBp') -> major={unit('GBp').major} per_major={unit('GBp').per_major}")
    print(f"unit('GBP') -> major={unit('GBP').major} per_major={unit('GBP').per_major}")
    raise SystemExit(1 if bad else 0)
