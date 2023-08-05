"""A Hypothesis extension for JSON schemata."""
# pylint: disable=no-value-for-parameter,too-many-return-statements,bad-continuation


import json
import re
from typing import Any, Dict, List, Union

import hypothesis.provisional as prov
import hypothesis.strategies as st
import jsonschema
from hypothesis import assume
from hypothesis.errors import InvalidArgument

# Mypy does not (yet!) support recursive type definitions.
# (and writing a few steps by hand is a DoS attack on the AST walker in Pytest)
JSONType = Union[None, bool, float, str, list, dict]

JSON_STRATEGY: st.SearchStrategy[JSONType] = st.deferred(
    lambda: st.one_of(
        st.none(),
        st.booleans(),
        st.floats(allow_nan=False, allow_infinity=False).map(lambda x: x or 0.0),
        st.text(),
        st.lists(JSON_STRATEGY, max_size=3),
        st.dictionaries(st.text(), JSON_STRATEGY, max_size=3),
    )
)


def encode_canonical_json(value: JSONType) -> str:
    """Canonical form serialiser, for uniqueness testing."""
    if isinstance(value, (type(None), bool, str, int, float)):
        return json.dumps(value)
    if isinstance(value, list):
        return "[" + ",".join(map(encode_canonical_json, value)) + "]"
    assert isinstance(value, dict)
    assert all(isinstance(k, str) for k in value)
    elems = sorted(
        f"{encode_canonical_json(k)}:{encode_canonical_json(v)}"
        for k, v in value.items()
    )
    return "{" + ",".join(elems) + "}"


def from_schema(schema: dict) -> st.SearchStrategy[JSONType]:
    """Take a JSON schema and return a strategy for allowed JSON objects.

    This strategy supports almost all of the schema elements described in the
    draft RFC as of November 2018 (draft 7), with the following exceptions:

    - For objects, the "dependencies" keyword is not supported.
    - Subschemata are not supported, i.e. the "if", "then", and "else" keywords,
      and the "allOf, "anyOf", "oneOf", and "not" keywords.
    - Schema reuse with "definitions" is not supported.
    - string-encoding of non-JSON data is not supported.
    - schema annotations, i.e. "title", "description", "default",
    "readOnly", "writeOnly", and "examples" are not supported.
    - JSON pointers are not supported.
    """
    # Boolean objects are special schemata; False rejects all and True accepts all.
    if schema is False:
        return st.nothing()
    if schema is True:
        return JSON_STRATEGY
    # Otherwise, we're dealing with "objects", i.e. dicts.
    if not isinstance(schema, dict):
        raise InvalidArgument(
            f"Got schema={schema} of type {type(schema).__name__}, "
            "but expected a dict."
        )
    jsonschema.validators.validator_for(schema).check_schema(schema)

    # Now we handle as many validation keywords as we can...
    if schema == {}:
        return JSON_STRATEGY

    if "enum" in schema:
        return st.sampled_from(schema["enum"])
    if "const" in schema:
        return st.just(schema["const"])
    # Schema must have a type then, so:
    if schema["type"] == "null":
        return st.none()
    if schema["type"] == "boolean":
        return st.booleans()
    if schema["type"] in ("number", "integer"):
        return numeric_schema(schema)
    if schema["type"] == "string":
        return string_schema(schema)
    if schema["type"] == "array":
        return array_schema(schema)
    assert schema["type"] == "object"
    return object_schema(schema)


def numeric_schema(schema: dict) -> st.SearchStrategy[float]:
    """Handle numeric schemata."""
    multiple_of = schema.get("multipleOf")
    lower = schema.get("minimum")
    upper = schema.get("maximum")
    if multiple_of is not None or schema["type"] == "integer":
        if lower is not None and schema.get("exclusiveMinimum"):
            lower += 1
        if upper is not None and schema.get("exclusiveMaximum"):
            upper -= 1
        if multiple_of is not None:
            if lower is not None:
                lower += (multiple_of - lower) % multiple_of
                lower //= multiple_of
            if upper is not None:
                upper -= upper % multiple_of
                upper //= multiple_of
            return st.integers(lower, upper).map(
                lambda x: x * multiple_of  # type: ignore
            )
        return st.integers(lower, upper)
    strategy = st.floats(
        min_value=lower, max_value=upper, allow_nan=False, allow_infinity=False
    )
    if schema.get("exclusiveMaximum") or schema.get("exclusiveMinimum"):
        return strategy.filter(lambda x: x not in (lower, upper))
    # Negative-zero does not round trip through JSON, so force it to positive
    return strategy.map(lambda n: 0.0 if n == 0 else n)


RFC3339_FORMATS = (
    "date-fullyear",
    "date-month",
    "date-mday",
    "time-hour",
    "time-minute",
    "time-second",
    "time-secfrac",
    "time-numoffset",
    "time-offset",
    "partial-time",
    "full-date",
    "full-time",
    "date-time",
)
JSON_SCHEMA_STRING_FORMATS = RFC3339_FORMATS + (
    "email",
    "idn-email",
    "hostname",
    "idn-hostname",
    "ipv4",
    "ipv6",
    "uri",
    "uri-reference",
    "iri",
    "iri-reference",
    "uri-template",
    "json-pointer",
    "relative-json-pointer",
    "regex",
)


def rfc3339(name: str) -> st.SearchStrategy[str]:
    """Given the name of an RFC3339 date or time format,
    return a strategy for conforming values.

    See https://tools.ietf.org/html/rfc3339#section-5.6
    """
    # Hmm, https://github.com/HypothesisWorks/hypothesis/issues/170
    # would make this a lot easier...
    assert name in RFC3339_FORMATS
    simple = {
        "date-fullyear": st.integers(0, 9999).map(str),
        "date-month": st.integers(1, 12).map(str),
        "date-mday": st.integers(1, 28).map(str),  # incomplete but valid
        "time-hour": st.integers(0, 23).map(str),
        "time-minute": st.integers(0, 59).map(str),
        "time-second": st.integers(0, 59).map(str),  # ignore negative leap seconds
        "time-secfrac": st.from_regex(r"\.[0-9]+"),
    }
    if name in simple:
        return simple[name]
    if name == "time-numoffset":
        return st.tuples(
            st.sampled_from(["+", "-"]), rfc3339("time-hour"), rfc3339("time-minute")
        ).map(":".join)
    if name == "time-offset":
        return st.just("Z") | rfc3339("time-numoffset")  # type: ignore
    if name == "partial-time":
        return st.times().map(str)
    if name == "full-date":
        return st.dates().map(str)
    if name == "full-time":
        return st.tuples(rfc3339("partial-time"), rfc3339("time-offset")).map("".join)
    assert name == "date-time"
    return st.tuples(rfc3339("full-date"), rfc3339("full-time")).map("T".join)


def string_schema(schema: dict) -> st.SearchStrategy[str]:
    """Handle schemata for strings."""
    # also https://json-schema.org/latest/json-schema-validation.html#rfc.section.7
    min_size = schema.get("minLength", 0)
    max_size = schema.get("maxLength", float("inf"))
    strategy: Any = st.text(min_size=min_size, max_size=schema.get("maxLength"))
    assert not (
        "format" in schema and "pattern" in schema
    ), "format and regex constraints are supported, but not both at once."
    if "pattern" in schema:
        strategy = st.from_regex(schema["pattern"])
    elif "format" in schema:
        url_synonyms = ["uri", "uri-reference", "iri", "iri-reference", "uri-template"]
        domains = prov.domains()  # type: ignore
        strategy = {
            # A value of None indicates a known but unsupported format.
            **{name: rfc3339(name) for name in RFC3339_FORMATS},
            "date": rfc3339("full-date"),
            "time": rfc3339("full-time"),
            "email": st.emails(),  # type: ignore
            "idn-email": st.emails(),  # type: ignore
            "hostname": domains,
            "idn-hostname": domains,
            "ipv4": prov.ip4_addr_strings(),  # type: ignore
            "ipv6": prov.ip6_addr_strings(),  # type: ignore
            **{name: domains.map("https://{}".format) for name in url_synonyms},
            "json-pointer": st.just(""),
            "relative-json-pointer": st.just(""),
            "regex": REGEX_PATTERNS,
        }.get(schema["format"])
        if strategy is None:
            raise InvalidArgument(f"Unsupported string format={schema['format']}")
    return strategy.filter(lambda s: min_size <= len(s) <= max_size)  # type: ignore


def array_schema(schema: dict) -> st.SearchStrategy[List[JSONType]]:
    """Handle schemata for arrays."""
    items = schema.get("items", {})
    additional_items = schema.get("additionalItems", {})
    min_size = schema.get("minItems", 0)
    max_size = schema.get("maxItems")
    unique = schema.get("uniqueItems")
    contains = schema.get("contains", {})
    if isinstance(items, list):
        min_size = max(0, min_size - len(items))
        if max_size is not None:
            max_size -= len(items)
        if contains != {}:
            assert (
                additional_items == {}
            ), "Cannot handle additionalItems and contains togther"
            additional_items = contains
            min_size = max(min_size, 1)
        fixed_items = st.tuples(*map(from_schema, items))
        extra_items = st.lists(
            from_schema(additional_items), min_size=min_size, max_size=max_size
        )
        return st.tuples(fixed_items, extra_items).map(
            lambda t: list(t[0]) + t[1]  # type: ignore
        )
    if contains != {}:
        assert items == {}, "Cannot handle items and contains togther"
        items = contains
    if unique:
        return st.lists(
            from_schema(items),
            min_size=min_size,
            max_size=max_size,
            unique_by=encode_canonical_json,
        )
    return st.lists(from_schema(items), min_size=min_size, max_size=max_size)


def object_schema(schema: dict) -> st.SearchStrategy[Dict[str, JSONType]]:
    """Handle a manageable subset of possible schemata for objects."""
    hard_keywords = "dependencies if then else allOf anyOf oneOf not".split()
    assert not any(kw in schema for kw in hard_keywords)

    required = schema.get("required", [])  # required keys
    names = schema.get("propertyNames", {"type": "string"})  # schema for optional keys
    min_size = max(len(required), schema.get("minProperties", 0))
    max_size = schema.get("maxProperties", float("inf"))

    properties = schema.get("properties", {})  # exact name: value schema
    patterns = schema.get("patternProperties", {})  # regex for names: value schema
    additional = schema.get("additionalProperties", {})  # schema for other values

    @st.composite
    def from_object_schema(draw: Any) -> Any:
        """Here, we do some black magic with private Hypothesis internals.

        It's unfortunate, but also the only way that I know of to satisfy all
        the interacting constraints without making shrinking totally hopeless.

        If any Hypothesis maintainers are reading this... I'm so, so sorry.
        """
        import hypothesis.internal.conjecture.utils as cu

        elements = cu.many(  # type: ignore
            draw(st.data()).conjecture_data,
            min_size=min_size,
            max_size=max_size,
            average_size=min(min_size + 5, (min_size + max_size) // 2),
        )
        out: dict = {}
        while elements.more():
            for name in required:
                if name not in out:
                    key = name
                    break
            else:
                key = draw(
                    (
                        from_schema(names)
                        | st.sampled_from(sorted(properties))
                        | st.one_of(*map(st.from_regex, sorted(patterns)))
                    ).filter(lambda s: s not in out)
                )
            if key in properties:
                out[key] = draw(from_schema(properties[key]))
            else:
                for rgx, matching_schema in patterns.items():
                    if re.search(rgx, string=key) is not None:
                        out[key] = draw(from_schema(matching_schema))
                        break
                else:
                    out[key] = draw(from_schema(additional))
        return out

    return from_object_schema()


# OK, now on to the inverse: a strategy for generating schemata themselves.


def json_schemata() -> st.SearchStrategy[Union[bool, Dict[str, JSONType]]]:
    """A Hypothesis strategy for arbitrary JSON schemata.

    This strategy may generate anything that can be handled by `from_schema`,
    and is used to provide full branch coverage when testing this package.
    """
    return _json_schemata()


@st.composite
def regex_patterns(draw: Any) -> st.SearchStrategy[str]:
    """A strategy for simple regular expression patterns."""
    fragments = st.one_of(
        st.just("."),
        st.from_regex(r"\[\^?[A-Za-z0-9]+\]"),
        REGEX_PATTERNS.map("{}+".format),
        REGEX_PATTERNS.map("{}?".format),
        REGEX_PATTERNS.map("{}*".format),
    )
    result = draw(st.lists(fragments, min_size=1, max_size=3).map("".join))
    try:
        re.compile(result)
    except re.error:
        assume(False)
    return result  # type: ignore


REGEX_PATTERNS = regex_patterns()


@st.composite
def _json_schemata(draw: Any, recur: bool = True) -> Any:
    """Wrapped so we can disable the pylint error in one place only."""
    # Current version of jsonschema does not support boolean schemata,
    # but 3.0 will.  See https://github.com/Julian/jsonschema/issues/337
    unique_list = st.lists(
        JSON_STRATEGY, min_size=1, max_size=10, unique_by=encode_canonical_json
    )
    options = [
        st.builds(dict),
        st.just({"type": "null"}),
        st.just({"type": "boolean"}),
        gen_number("integer"),
        gen_number("number"),
        gen_string(),
        st.fixed_dictionaries(dict(const=JSON_STRATEGY)),
        st.fixed_dictionaries(dict(enum=unique_list)),
    ]
    if recur:
        options.extend([gen_array(), gen_object()])
    return draw(draw(st.sampled_from(options)))


@st.composite
def gen_number(draw: Any, kind: str) -> Dict[str, Union[str, float]]:
    """Draw a numeric schema."""
    max_int_float = 2 ** 53
    lower = draw(st.none() | st.integers(-max_int_float, max_int_float))
    upper = draw(st.none() | st.integers(-max_int_float, max_int_float))
    if lower is not None and upper is not None and lower > upper:
        lower, upper = upper, lower
    multiple_of = draw(st.none() | st.integers(2, 100))
    assume(None in (multiple_of, lower, upper) or multiple_of <= (upper - lower))
    out: Dict[str, Union[str, float]] = {"type": kind}
    if lower is not None:
        if draw(st.booleans()):
            out["exclusiveMinimum"] = True
            lower -= 1
        out["minimum"] = lower
    if upper is not None:
        if draw(st.booleans()):
            out["exclusiveMaximum"] = True
            upper += 1
        out["maximum"] = upper
    if multiple_of is not None:
        out["multipleOf"] = multiple_of
    return out


@st.composite
def gen_string(draw: Any) -> Dict[str, Union[str, int]]:
    """Draw a string schema."""
    min_size = draw(st.none() | st.integers(0, 10))
    max_size = draw(st.none() | st.integers(0, 1000))
    if min_size is not None and max_size is not None and min_size > max_size:
        min_size, max_size = max_size, min_size
    pattern = draw(st.none() | REGEX_PATTERNS)
    format_ = draw(st.none() | st.sampled_from(JSON_SCHEMA_STRING_FORMATS))
    out: Dict[str, Union[str, int]] = {"type": "string"}
    if pattern is not None:
        out["pattern"] = pattern
    elif format_ is not None:
        out["format"] = format_
    if min_size is not None:
        out["minLength"] = min_size
    if max_size is not None:
        out["maxLength"] = max_size
    return out


@st.composite
def gen_array(draw: Any) -> Dict[str, JSONType]:
    """Draw an array schema."""
    min_size = draw(st.none() | st.integers(0, 5))
    max_size = draw(st.none() | st.integers(2, 5))
    if min_size is not None and max_size is not None and min_size > max_size:
        min_size, max_size = max_size, min_size
    items = draw(
        st.builds(dict)
        | _json_schemata(recur=False)
        | st.lists(_json_schemata(recur=False), min_size=1, max_size=10)
    )
    out = {"type": "array", "items": items}
    if isinstance(items, list):
        increment = len(items)
        additional = draw(st.none() | _json_schemata(recur=False))
        if additional is not None:
            out["additionalItems"] = additional
        elif draw(st.booleans()):
            out["contains"] = draw(_json_schemata(recur=False).filter(bool))
            increment += 1
        if min_size is not None:
            min_size += increment
        if max_size is not None:
            max_size += increment
    else:
        if draw(st.booleans()):
            out["uniqueItems"] = True
        if items == {}:
            out["contains"] = draw(_json_schemata(recur=False))
    if min_size is not None:
        out["minItems"] = min_size
    if max_size is not None:
        out["maxItems"] = max_size
    return out


@st.composite
def gen_object(draw: Any) -> Dict[str, JSONType]:
    """Draw an object schema."""
    out: Dict[str, JSONType] = {"type": "object"}
    names = draw(st.sampled_from([None, None, None, draw(gen_string())]))
    required = draw(st.booleans())
    if required and names is None:
        required = draw(st.lists(st.text(), min_size=1, max_size=5, unique=True))
    elif required:
        required = draw(
            st.lists(from_schema(names), min_size=1, max_size=5, unique=True)
        )

    # Trying to generate schemata that are consistent would mean dealing with
    # overlapping regex and names, and that would suck.  So instead we ensure that
    # there *are* no overlapping requirements, which is much easier.
    properties = draw(st.dictionaries(st.text(), _json_schemata(recur=False)))
    disjoint = REGEX_PATTERNS.filter(
        lambda r: all(re.search(r, string=name) is None for name in properties)
    )
    patterns = draw(st.dictionaries(disjoint, _json_schemata(recur=False), max_size=1))
    additional = draw(st.none() | _json_schemata(recur=False))

    min_size = draw(st.none() | st.integers(0, 5))
    max_size = draw(st.none() | st.integers(2, 5))
    if min_size is not None and max_size is not None and min_size > max_size:
        min_size, max_size = max_size, min_size

    if names is not None:
        out["propertyNames"] = names
    if required:
        out["required"] = required
        if min_size is not None:
            min_size += len(required)
        if max_size is not None:
            max_size += len(required)
    if min_size is not None:
        out["minProperties"] = min_size
    if max_size is not None:
        out["maxProperties"] = max_size
    if properties:
        out["properties"] = properties
    if patterns:
        out["patternProperties"] = patterns
    if additional is not None:
        out["additionalProperties"] = additional
    return out
