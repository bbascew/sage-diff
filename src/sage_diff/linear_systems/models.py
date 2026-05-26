from dataclasses import dataclass, field


@dataclass(frozen=True)
class FirstIntegral:
    expression: object
    kind: str
    domain_conditions: tuple = field(default_factory=tuple)
    eigenvalues: tuple = field(default_factory=tuple)
    vectors: tuple = field(default_factory=tuple)
