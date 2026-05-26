Документация sage-diff
======================

``sage-diff`` — небольшая Python-библиотека на базе SageMath для символьной
работы с линейными автономными дифференциальными системами

.. math::

   \dot{x} = A x,
   \qquad x \in \mathbb{R}^{n}.

Текущий фокус библиотеки — построение и проверка автономных первых интегралов
для таких систем. Скалярная функция ``W(x)`` считается первым интегралом, если
ее производная Ли вдоль векторного поля равна нулю:

.. math::

   \mathcal{L}_{A} W(x) = 0.

Реализация следует спектральному методу из статьи
``papers/ПОСТРОЕНИЕ_ИНТЕГРАЛОВ_ЛИНЕЙНОЙ_ДИФФЕРЕНЦИАЛЬНОЙ_СИСТЕМЫ.md`` и
использует SageMath для точной символьной линейной алгебры.

Содержание
----------

- `Математический метод <mathematical_method.rst>`_
- `Справочник API <api.rst>`_
- `Примеры <examples.rst>`_

Быстрый старт
-------------

.. code-block:: python

   from sage.all import QQ, matrix, var
   from sage_diff.linear_systems import lie_derivative, linear_first_integrals

   x = var("x1 x2", domain="real")
   A = matrix(QQ, [[0, -1], [1, 0]])

   integrals = linear_first_integrals(A, x)

   for integral in integrals:
       assert lie_derivative(integral.expression, A, x).simplify_full() == 0

Команды для разработки
----------------------

Создать или обновить локальное Conda-окружение с SageMath:

.. code-block:: console

   make env
   make env-update

Запустить проверки локально без пересборки Docker-образа:

.. code-block:: console

   make lint
   make test

Модель зависимости от SageMath
------------------------------

SageMath устанавливается через Conda, а не через ``pip``. Поэтому в проекте
намеренно нет обычной PyPI-зависимости ``sage`` в ``pyproject.toml``.

Основной публичный API
----------------------

Для обычного использования достаточно импортировать функции из
``sage_diff.linear_systems``:

.. code-block:: python

   from sage_diff.linear_systems import (
       FirstIntegral,
       lie_derivative,
       linear_first_integrals,
       linear_form,
   )

``linear_first_integrals`` строит список кандидатов в первые интегралы, а
``lie_derivative`` проверяет, что найденные выражения действительно сохраняются
на траекториях системы.
