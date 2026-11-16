# Benchmark sources

Each file holds one example copied from the official documentation: the import lines of the
example and the class definitions, unchanged. There are five examples per level. These
25 files are the benchmark used by the scripts and by the files in `results/` and `evaluation/`.

| File | Classes | Version | Source lines |
|---|---|---|---|
| `level_1/case_1.py` | User | pydantic v2.10.6 | [docs/concepts/models.md L67-L69](https://github.com/pydantic/pydantic/blob/v2.10.6/docs/concepts/models.md?plain=1#L67-L69) |
| `level_1/case_2.py` | Model | pydantic v2.12.5 | [docs/concepts/models.md L194-L197](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/concepts/models.md?plain=1#L194-L197) |
| `level_1/case_3.py` | Item | fastapi 0.136.1 | [docs_src/body/tutorial001_py310.py L5-L9](https://github.com/fastapi/fastapi/blob/0.136.1/docs_src/body/tutorial001_py310.py#L5-L9) |
| `level_1/case_4.py` | User | fastapi 0.136.1 | [docs_src/security/tutorial002_an_py310.py L12-L16](https://github.com/fastapi/fastapi/blob/0.136.1/docs_src/security/tutorial002_an_py310.py#L12-L16) |
| `level_1/case_5.py` | Model | pydantic v2.12.5 | [docs/concepts/models.md L1546-L1551](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/concepts/models.md?plain=1#L1546-L1551) |
| `level_2/case_1.py` | Model | pydantic v2.12.5 | [docs/concepts/fields.md L433-L436](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/concepts/fields.md?plain=1#L433-L436) |
| `level_2/case_2.py` | Item | fastapi 0.136.1 | [docs_src/body_fields/tutorial001_an_py310.py L9-L15](https://github.com/fastapi/fastapi/blob/0.136.1/docs_src/body_fields/tutorial001_an_py310.py#L9-L15) |
| `level_2/case_3.py` | FilterParams | fastapi 0.136.1 | [docs_src/query_param_models/tutorial001_an_py310.py L9-L13](https://github.com/fastapi/fastapi/blob/0.136.1/docs_src/query_param_models/tutorial001_an_py310.py#L9-L13) |
| `level_2/case_4.py` | Model | pydantic v2.12.5 | [docs/errors/validation_errors.md L1526-L1527](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/errors/validation_errors.md?plain=1#L1526-L1527) |
| `level_2/case_5.py` | Model | pydantic v2.12.5 | [docs/errors/validation_errors.md L1691-L1692](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/errors/validation_errors.md?plain=1#L1691-L1692) |
| `level_3/case_1.py` | Image, Item | fastapi 0.136.1 | [docs_src/body_nested_models/tutorial004_py310.py L7-L18](https://github.com/fastapi/fastapi/blob/0.136.1/docs_src/body_nested_models/tutorial004_py310.py#L7-L18) |
| `level_3/case_2.py` | Image, Item, Offer | fastapi 0.136.1 | [docs_src/body_nested_models/tutorial007_py310.py L7-L25](https://github.com/fastapi/fastapi/blob/0.136.1/docs_src/body_nested_models/tutorial007_py310.py#L7-L25) |
| `level_3/case_3.py` | Foo, Bar, Spam | pydantic v2.12.5 | [docs/concepts/models.md L295-L307](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/concepts/models.md?plain=1#L295-L307) |
| `level_3/case_4.py` | BarModel, FooBarModel | pydantic v2.12.5 | [docs/concepts/models.md L676-L683](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/concepts/models.md?plain=1#L676-L683) |
| `level_3/case_5.py` | Hobby, User | pydantic v2.12.5 | [docs/concepts/serialization.md L801-L807](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/concepts/serialization.md?plain=1#L801-L807) |
| `level_4/case_1.py` | Model | pydantic v2.12.5 | [docs/concepts/validators.md L440-L447](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/concepts/validators.md?plain=1#L440-L447) |
| `level_4/case_2.py` | Model | pydantic v2.12.5 | [docs/concepts/validators.md L91-L99](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/concepts/validators.md?plain=1#L91-L99) |
| `level_4/case_3.py` | Model | pydantic v2.12.5 | [docs/concepts/validators.md L219-L228](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/concepts/validators.md?plain=1#L219-L228) |
| `level_4/case_4.py` | Model | pydantic v2.12.5 | [docs/concepts/validators.md L145-L151](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/concepts/validators.md?plain=1#L145-L151) |
| `level_4/case_5.py` | Model | pydantic v2.12.5 | [docs/concepts/validators.md L293-L302](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/concepts/validators.md?plain=1#L293-L302) |
| `level_5/case_1.py` | UserModel | pydantic v2.12.5 | [docs/concepts/validators.md L480-L489](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/concepts/validators.md?plain=1#L480-L489) |
| `level_5/case_2.py` | UserModel | pydantic v2.12.5 | [docs/concepts/validators.md L504-L513](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/concepts/validators.md?plain=1#L504-L513) |
| `level_5/case_3.py` | UserModel | pydantic v2.12.5 | [docs/concepts/validators.md L615-L625](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/concepts/validators.md?plain=1#L615-L625) |
| `level_5/case_4.py` | Square | pydantic v2.12.5 | [pydantic/functional_validators.py L687-L695](https://github.com/pydantic/pydantic/blob/v2.12.5/pydantic/functional_validators.py#L687-L695) |
| `level_5/case_5.py` | User, Organization | pydantic v2.12.5 | [docs/examples/custom_validators.md L183-L201](https://github.com/pydantic/pydantic/blob/v2.12.5/docs/examples/custom_validators.md?plain=1#L183-L201) |
