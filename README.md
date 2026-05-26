# sage-diff

`sage-diff` — библиотека на базе SageMath для символьной работы с линейными автономными дифференциальными системами.

Текущий фокус проекта — построение и проверка автономных первых интегралов для систем

$$
\dot{x} = A x, \qquad x \in \mathbb{R}^{n}.
$$

Первый интеграл `W(x)` проверяется через производную Ли:

$$
\mathcal{L}_{A} W(x)
=
\sum_{i=1}^{n}
\frac{\partial W}{\partial x_i}(Ax)_i
= 0.
$$

Метод основан на спектральном построении первых интегралов по собственным векторам и жордановым цепочкам матрицы

$$
B = A^T.
$$

## Возможности

- построение первых интегралов для `dx/dt = A x`
- поддержка вещественных собственных чисел
- поддержка комплексных собственных пар
- поддержка жордановых цепочек
- поддержка нильпотентных случаев
- проверка результата через производную Ли
- точные символьные вычисления через SageMath

## Быстрый пример

```python
from sage.all import QQ, matrix, var
from sage_diff.linear_systems import lie_derivative, linear_first_integrals

x = var("x1 x2", domain="real")
A = matrix(QQ, [[0, -1], [1, 0]])

integrals = linear_first_integrals(A, x)

for integral in integrals:
    print(integral.kind, integral.expression)
    assert lie_derivative(integral.expression, A, x).simplify_full() == 0
```

## Установка окружения

SageMath ставится через Conda, а не через `pip`. Поэтому в `pyproject.toml` нет зависимости `sage`.

Создать локальное окружение:

```bash
make env
```

Если окружение уже есть, обновить его:

```bash
make env-update
```

Запустить тесты:

```bash
make test
```

Запустить линтер:

```bash
make lint
```

Запустить один тест:

```bash
make test-one TEST=tests/test_first_integrals.py::test_builds_nilpotent_jordan_chain_integrals
```

## Docker

Можно использовать Docker-образ с Conda и SageMath:

```bash
docker build -t sage-diff .
docker run --rm sage-diff
```

Для быстрых focused-тестов без пересборки образа:

```bash
docker run --rm -v "$PWD":/workspace -w /workspace sage-diff pytest tests/test_first_integrals.py
```

## Публичный API

Основной API находится в `sage_diff.linear_systems`:

```python
from sage_diff.linear_systems import (
    FirstIntegral,
    lie_derivative,
    linear_first_integrals,
    linear_form,
)
```

`linear_first_integrals(A, variables=None)` строит список объектов `FirstIntegral`.

`lie_derivative(expression, A, variables)` вычисляет производную Ли вдоль системы `dot{x} = A x`.

`linear_form(coefficients, variables)` строит линейную форму

$$
p_v(x) = v^T x.
$$

## Тип результата

Каждый найденный интеграл представлен объектом `FirstIntegral`:

```python
FirstIntegral(
    expression=...,          # Sage-выражение W(x)
    kind=...,                # тип формулы
    domain_conditions=...,   # ограничения области
    eigenvalues=...,         # использованные собственные числа
    vectors=...,             # использованные собственные / присоединенные векторы
)
```

Примеры `kind`:

- `real_zero`
- `real_ratio`
- `real_pair`
- `complex_eigen`
- `complex_real`
- `complex_pair`
- `real_jordan_exponential`
- `real_jordan_psi_2`
- `complex_jordan_exponential`
- `complex_jordan_angle`
- `zero_jordan_real`
- `zero_jordan_complex_radius`
- `zero_jordan_complex_angle`

## Математическая идея

Для системы

$$
\dot{x} = A x
$$

рассматривается транспонированная матрица

$$
B = A^T.
$$

Если `v` — собственный вектор `B`,

$$
Bv = \lambda v,
$$

то линейная форма

$$
p_v(x) = v^T x
$$

удовлетворяет

$$
\frac{d}{dt}p_v(x(t)) = \lambda p_v(x(t)).
$$

Из таких частных интегралов строятся первые интегралы: отношения, степенные произведения, экспоненциальные выражения, угловые выражения и жордановы инварианты.

## Документация

Подробная документация лежит в `docs/`:

- [`docs/index.rst`](docs/index.rst)
- [`docs/mathematical_method.rst`](docs/mathematical_method.rst)
- [`docs/api.rst`](docs/api.rst)
- [`docs/examples.rst`](docs/examples.rst)

## Структура проекта

```text
src/sage_diff/
  __init__.py
  linear_systems/
    algebra.py
    builder.py
    first_integrals.py
    models.py
    spectrum.py
    formulas/
      real.py
      complex.py
      jordan.py
```

## Проверенные случаи

Тесты покрывают:

- вещественный спектр из статьи
- дефектный жорданов блок
- нильпотентную жорданову цепочку
- несколько жордановых блоков с одним собственным числом
- несколько нильпотентных блоков
- комплексные собственные пары
- комплексные жордановы блоки
- нулевую жорданову цепочку вместе с комплексным собственным числом

Главный критерий каждого теста:

```python
lie_derivative(integral.expression, A, x).simplify_full() == 0
```
