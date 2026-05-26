Справочник API
==============

На этой странице описан публичный API, экспортируемый из ``sage_diff`` и
``sage_diff.linear_systems``.

Модель данных
-------------

FirstIntegral
~~~~~~~~~~~~~

``FirstIntegral`` — неизменяемый ``dataclass``, описывающий один построенный
первый интеграл.

Поля:

``expression``
   Символьное Sage-выражение для функции ``W(x)``.

``kind``
   Строка, указывающая формулу, по которой построено выражение. Примеры:
   ``real_zero``, ``real_pair``, ``complex_eigen``,
   ``real_jordan_exponential``.

``domain_conditions``
   Кортеж Sage-выражений, которые должны быть ненулевыми или должны
   удовлетворять ограничениям области. Например, для отношений здесь
   сохраняются знаменатели.

``eigenvalues``
   Кортеж собственных чисел, использованных при построении интеграла.

``vectors``
   Кортеж собственных векторов или векторов жордановой цепочки, использованных
   при построении интеграла.

Основные функции построения
---------------------------

linear_first_integrals
~~~~~~~~~~~~~~~~~~~~~~

Сигнатура:

.. code-block:: python

   linear_first_integrals(A, variables=None)

Строит кандидаты в первые интегралы для линейной системы

.. math::

   \dot{x} = A x.

Параметры:

``A``
   Квадратная Sage-матрица или объект, приводимый к матрице. Если нужно,
   реализация вызывает ``sage.all.matrix``.

``variables``
   Необязательный список или кортеж Sage-переменных. Если аргумент не передан,
   автоматически создаются вещественные переменные ``x1, x2, ..., xn``.

Возвращает:

   Список объектов ``FirstIntegral``. Дубликаты удаляются по строковому виду
   упрощенного выражения.

Метод:

   Функция вычисляет ``B = A.transpose()``, находит правые собственные векторы
   и жордановы цепочки матрицы ``B``, затем применяет формулы из
   ``mathematical_method.rst``.

Пример:

.. code-block:: python

   from sage.all import QQ, matrix, var
   from sage_diff.linear_systems import linear_first_integrals

   x = var("x1 x2", domain="real")
   A = matrix(QQ, [[0, -1], [1, 0]])
   integrals = linear_first_integrals(A, x)

lie_derivative
~~~~~~~~~~~~~~

Сигнатура:

.. code-block:: python

   lie_derivative(expression, A, variables)

Вычисляет производную Ли скалярного выражения вдоль векторного поля ``A*x``:

.. math::

   \mathcal{L}_{A} W(x)
   =
   \sum_{i=1}^{n}
   \frac{\partial W}{\partial x_i}(Ax)_i.

Параметры:

``expression``
   Sage-выражение ``W(x)``.

``A``
   Матрица системы.

``variables``
   Переменные, соответствующие координатам ``x``.

Возвращает:

   Упрощенное Sage-выражение.

Пример:

.. code-block:: python

   assert lie_derivative(integral.expression, A, x).simplify_full() == 0

linear_form
~~~~~~~~~~~

Сигнатура:

.. code-block:: python

   linear_form(coefficients, variables)

Строит линейную форму

.. math::

   p_v(x) = v^T x = \sum_{i=1}^{n} v_i x_i.

Параметры:

``coefficients``
   Вектор или итерируемый объект с коэффициентами ``v_i``.

``variables``
   Переменные ``x_i``.

Возвращает:

   Sage-выражение.

Функции-формулы
---------------

Функции-формулы экспортируются для точечного использования и тестов. Они не
ищут собственные векторы самостоятельно: вызывающий код передает собственные
числа, собственные векторы, жордановы цепочки и переменные напрямую.

real_zero_integral
~~~~~~~~~~~~~~~~~~

Сигнатура:

.. code-block:: python

   real_zero_integral(eigenvector, variables)

Строит

.. math::

   W(x) = p_v(x)

для вещественного собственного вектора ``v`` с нулевым собственным числом.
Возвращает ``FirstIntegral`` с ``kind = "real_zero"``.

real_ratio_integral
~~~~~~~~~~~~~~~~~~~

Сигнатура:

.. code-block:: python

   real_ratio_integral(eigenvector1, eigenvector2, variables, eigenvalue=None)

Строит

.. math::

   W(x) = \frac{p_{v_2}(x)}{p_{v_1}(x)}

для двух собственных векторов одного и того же ненулевого вещественного
собственного числа. Возвращает ``kind = "real_ratio"`` и записывает ``p_v1`` в
``domain_conditions``.

real_pair_integral
~~~~~~~~~~~~~~~~~~

Сигнатура:

.. code-block:: python

   real_pair_integral(lambda1, eigenvector1, lambda2, eigenvector2, variables)

Строит

.. math::

   W(x) = p_{v_1}(x)^{\lambda_2}p_{v_2}(x)^{-\lambda_1}

для двух разных ненулевых вещественных собственных чисел. Возвращает
``kind = "real_pair"``.

complex_eigen_integral
~~~~~~~~~~~~~~~~~~~~~~

Сигнатура:

.. code-block:: python

   complex_eigen_integral(eigenvalue, eigenvector, variables)

Для ``lambda = xi + zeta*i`` и ``v = eta + mu*i`` строит

.. math::

   W(x)
   =
   \left(p_\eta(x)^2 + p_\mu(x)^2\right)
   \exp\left(
     -2\frac{\xi}{\zeta}
     \arctan\frac{p_\mu(x)}{p_\eta(x)}
   \right).

Возвращает ``kind = "complex_eigen"``.

complex_real_integral
~~~~~~~~~~~~~~~~~~~~~

Сигнатура:

.. code-block:: python

   complex_real_integral(
       complex_eigenvalue,
       complex_eigenvector,
       real_eigenvalue,
       real_eigenvector,
       variables,
   )

Строит

.. math::

   W(x)
   =
   p_{v_r}(x)
   \exp\left(
     -\frac{\lambda_r}{\zeta}
     \arctan\frac{p_\mu(x)}{p_\eta(x)}
   \right).

Возвращает ``kind = "complex_real"``.

complex_pair_integral
~~~~~~~~~~~~~~~~~~~~~

Сигнатура:

.. code-block:: python

   complex_pair_integral(lambda1, eigenvector1, lambda2, eigenvector2, variables)

Строит

.. math::

   W(x)
   =
   \zeta_1 \arctan\frac{p_{\mu_2}(x)}{p_{\eta_2}(x)}
   -
   \zeta_2 \arctan\frac{p_{\mu_1}(x)}{p_{\eta_1}(x)}.

Возвращает ``kind = "complex_pair"``.

jordan_chain_integrals
~~~~~~~~~~~~~~~~~~~~~~

Сигнатура:

.. code-block:: python

   jordan_chain_integrals(eigenvalue, chain, variables)

Выбирает вещественную или комплексную формулу для жордановой цепочки в
зависимости от собственного числа. Цепочка должна быть в нормировке

.. math::

   (B - \lambda E)v^k = k v^{k-1}.

Возвращает список объектов ``FirstIntegral``.

zero_jordan_real_integral
~~~~~~~~~~~~~~~~~~~~~~~~~

Сигнатура:

.. code-block:: python

   zero_jordan_real_integral(real_eigenvalue, real_eigenvector, zero_chain, variables)

Для нулевой жордановой цепочки ``v0, v1`` и ненулевого вещественного
собственного числа ``lambda_r`` строит

.. math::

   W(x)
   =
   p_{v_r}(x)
   \exp\left(-\lambda_r\frac{p_1(x)}{p_0(x)}\right).

Возвращает ``kind = "zero_jordan_real"``.

zero_jordan_complex_integrals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Сигнатура:

.. code-block:: python

   zero_jordan_complex_integrals(complex_eigenvalue, complex_eigenvector, zero_chain, variables)

Для нулевой жордановой цепочки и комплексного собственного числа строит два
первых интеграла:

.. math::

   W_1(x)
   =
   \left(p_\eta(x)^2 + p_\mu(x)^2\right)
   \exp\left(-2\xi\frac{p_1(x)}{p_0(x)}\right),

.. math::

   W_2(x)
   =
   \arctan\frac{p_\mu(x)}{p_\eta(x)}
   -
   \zeta\frac{p_1(x)}{p_0(x)}.

Возвращает интегралы с ``kind = "zero_jordan_complex_radius"`` и
``kind = "zero_jordan_complex_angle"``.

Внутренние модули
-----------------

Совместимый публичный путь импорта:
``sage_diff.linear_systems.first_integrals``. Внутри реализация разделена на
модули:

``models.py``
   Dataclass-модели.

``algebra.py``
   Приведение к матрице, переменные, линейные формы, вещественная/мнимая части
   и производная Ли.

``spectrum.py``
   Собственные векторы Sage и жордановы цепочки.

``builder.py``
   Высокоуровневая сборка ``linear_first_integrals``.

``formulas/``
   Формулы, разложенные по группам: вещественные, комплексные и жордановы
   случаи.
