import typing

from pydantic import BaseModel, validate_model, Field
from pydantic.typing import Optional, Literal, List, Dict, Union
import inspect

def validate(model: BaseModel):


    for field_name, field_props in model.__fields__.items():
        field = getattr(model, field_name)
        if isinstance(field, BaseModel):
            validate(field)
        elif isinstance(field, list):
            [validate(x) for x in field if isinstance(x, BaseModel)]
        elif isinstance(field, dict):
            [validate(v) for k,v in field.items() if isinstance(v, BaseModel)]

    *_, validation_error = validate_model(model.__class__, model.__dict__)
    if validation_error:
        raise validation_error


class Inner(BaseModel):

    foo: Literal['bar']


class Outer(BaseModel):

    inner: Inner
    inner_list: List[Union[int, Inner, Literal['foo']]]
    inner_dict: Dict[str, Inner]

def main():
    # Prepare the structure
    outer = Outer.construct()

    # Further down, figure out inner needs to be set
    outer.inner = Inner.construct()

    # Even futher down, populate inner.foo with incorrect value
    outer.inner.foo = "bar"
    outer.inner_list = [Inner.construct(foo="bar"), "foo", 1]
    outer.inner_dict = {"foo": Inner.construct(), "bar": Inner.construct(foo="bar")}
    outer.inner_dict["foo"].foo = "bar"

    # This currently does not raise a validation_error
    validate(outer)
    print("Outer did not raise error")

    # This does
    #validate(outer.inner)

if __name__ == '__main__':
    main()