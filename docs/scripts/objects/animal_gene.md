[Previous Folder](../navbox/navbox.md) | [Previous File](animal.md) | [Next File](animal_part.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)

# animal_gene.py

## Classes

### `AnimalGene`

#### Class Methods

##### [`from_forced_gene(gene_id: str, data: dict) -> 'AnimalGene'`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L30)

Create/update a gene with an explicit range and mark it as forced.

Accepts {"min": x, "max": y} or {"minValue": x, "maxValue": y}.

##### [`_parse() -> dict`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L77)

##### [`load(attribute: str | None = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L86)

Load from cache, re-parse if version changed.

##### [`all() -> dict[str, 'AnimalGene']`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L110)

##### [`count() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L116)

##### [`exists(gene_id: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L122)

#### Static Methods

##### [`_split_commas(obj: object)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L67)

#### Object Methods

##### [`__new__(gene_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L12)

##### [`__init__(gene_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L21)

##### [`get(key: str, default = None)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L129)

##### [`clamp(value: float) -> float`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L175)

Clamp to [minValue, maxValue] when provided.

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L185)

#### Properties

##### [`data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L133)

##### [`is_valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L137)

##### [`name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L141)

##### [`has_range`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L147)

##### [`min_value`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L151)

##### [`max_value`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L155)

##### [`is_forced`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L159)

##### [`forced_values`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L164)

##### [`dominance`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L168)

##### [`ratio`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L172)

### `AnimalGeneticDisorder`

#### Class Methods

##### [`load()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L211)

Load disorders from AnimalGene data.

##### [`all() -> dict[str, 'AnimalGeneticDisorder']`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L219)

##### [`count() -> int`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L225)

##### [`exists(disorder_id: str) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L231)

#### Object Methods

##### [`__new__(disorder_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L193)

##### [`__init__(disorder_id: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L202)

##### [`__repr__()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L245)

#### Properties

##### [`is_valid`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L237)

##### [`value`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/animal_gene.py#L241)

Raw value (mirrors the key in current data).


[Previous Folder](../navbox/navbox.md) | [Previous File](animal.md) | [Next File](animal_part.md) | [Next Folder](../parser/creation_method_parser.md) | [Back to Index](../../index.md)
