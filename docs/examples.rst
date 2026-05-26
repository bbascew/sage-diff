Примеры
=======

Все примеры используют один и тот же принцип проверки: для каждого построенного
выражения вычисляется производная Ли вдоль системы ``dot{x} = A x``.

.. code-block:: python

   for integral in linear_first_integrals(A, x):
       assert lie_derivative(integral.expression, A, x).simplify_full() == 0

Пример с вещественным спектром
------------------------------

Этот пример соответствует системе четвертого порядка из статьи, где спектр
матрицы ``B = A^T`` вещественный.

.. code-block:: python

   from sage.all import QQ, matrix, var
   from sage_diff.linear_systems import lie_derivative, linear_first_integrals

   x = var("x1 x2 x3 x4", domain="real")
   A = matrix(
       QQ,
       [
           [1, -2, 0, -1],
           [-1, 4, -1, 2],
           [0, 2, 1, 1],
           [2, -4, 2, -2],
       ],
   )

   integrals = linear_first_integrals(A, x)
   kinds = {integral.kind for integral in integrals}

   assert {"real_zero", "real_ratio", "real_pair"} <= kinds

В этом случае нулевое собственное число дает линейный первый интеграл,
одинаковые ненулевые собственные числа дают отношение, а разные ненулевые
собственные числа дают степенное произведение.

Дефектный жорданов блок
-----------------------

Следующая матрица — стандартный пример дефектной матрицы с собственными числами
``1, 2, 4, 4`` и одним жордановым блоком размера 2 для собственного числа ``4``.

.. code-block:: python

   x = var("x1 x2 x3 x4", domain="real")
   A = matrix(
       QQ,
       [
           [5, 4, 2, 1],
           [0, 1, -1, -1],
           [-1, -1, 3, 0],
           [1, 1, -1, 2],
       ],
   )

   integrals = linear_first_integrals(A, x)
   kinds = {integral.kind for integral in integrals}

   assert {"real_pair", "real_jordan_exponential"} <= kinds

Жорданов блок дает интеграл вида

.. math::

   p_0(x)\exp\left(-\lambda\frac{p_1(x)}{p_0(x)}\right).

Нильпотентная жорданова цепочка
-------------------------------

Для нильпотентного блока длины 4 можно взять

.. math::

   B =
   \begin{pmatrix}
   0 & 1 & 0 & 0 \\
   0 & 0 & 1 & 0 \\
   0 & 0 & 0 & 1 \\
   0 & 0 & 0 & 0
   \end{pmatrix}.

В тестируемой системе используется ``A = B^T``.

.. code-block:: python

   x = var("x1 x2 x3 x4", domain="real")
   B = matrix(QQ, [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]])
   A = B.transpose()

   integrals = linear_first_integrals(A, x)
   kinds = {integral.kind for integral in integrals}

   assert {"real_zero", "real_jordan_psi_2", "real_jordan_psi_3"} <= kinds

Нетривиальные инварианты цепочки основаны на формулах

.. math::

   \Psi_2(x) = \frac{p_0(x)p_2(x) - p_1(x)^2}{p_0(x)^2},

и

.. math::

   \Psi_3(x)
   =
   \frac{p_0(x)^2p_3(x)-3p_0(x)p_1(x)p_2(x)+2p_1(x)^3}{p_0(x)^3}.

Несколько жордановых блоков с одним собственным числом
------------------------------------------------------

Этот пример проверяет, что сборщик корректно обрабатывает несколько жордановых
цепочек для одного и того же собственного числа:

.. math::

   B = J_3(2) \oplus J_2(2).

.. code-block:: python

   from sage.all import block_diagonal_matrix

   x = var("x1 x2 x3 x4 x5", domain="real")
   block3 = matrix(QQ, [[2, 1, 0], [0, 2, 1], [0, 0, 2]])
   block2 = matrix(QQ, [[2, 1], [0, 2]])
   A = block_diagonal_matrix(block3, block2).transpose()

   integrals = linear_first_integrals(A, x)
   assert [integral.kind for integral in integrals] == [
       "real_ratio",
       "real_jordan_exponential",
       "real_jordan_psi_2",
       "real_jordan_exponential",
   ]

Отношение появляется из-за двух независимых собственных векторов для одного
ненулевого собственного числа. Каждый нетривиальный блок также дает свой
жорданов интеграл.

Несколько нильпотентных жордановых блоков
-----------------------------------------

Нильпотентный случай с двумя цепочками проверяет обработку нулевого собственного
числа:

.. math::

   B = J_3(0) \oplus J_2(0).

.. code-block:: python

   x = var("x1 x2 x3 x4 x5", domain="real")
   block3 = matrix(QQ, [[0, 1, 0], [0, 0, 1], [0, 0, 0]])
   block2 = matrix(QQ, [[0, 1], [0, 0]])
   A = block_diagonal_matrix(block3, block2).transpose()

   integrals = linear_first_integrals(A, x)
   assert [integral.kind for integral in integrals] == [
       "real_zero",
       "real_zero",
       "real_jordan_psi_2",
   ]

Комплексное собственное число
-----------------------------

Для вещественной матрицы, у которой ``B = A^T`` имеет комплексную пару
``3 +/- i`` и одно вещественное собственное число ``2``:

.. code-block:: python

   x = var("x1 x2 x3", domain="real")
   B = matrix(QQ, [[3, -1, 0], [1, 3, 0], [0, 0, 2]])
   A = B.transpose()

   integrals = linear_first_integrals(A, x)
   kinds = {integral.kind for integral in integrals}

   assert {"complex_eigen", "complex_real"} <= kinds

Комплексная пара дает угловой экспоненциальный интеграл ``complex_eigen``.
Дополнительное вещественное собственное число дает интеграл ``complex_real``.

Интеграл для двух комплексных пар
---------------------------------

Две независимые комплексные пары дают угловой интеграл-разность:

.. code-block:: python

   x = var("x1 x2 x3 x4", domain="real")
   B = matrix(QQ, [[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 0, -2], [0, 0, 2, 0]])
   A = B.transpose()

   integrals = linear_first_integrals(A, x)
   kinds = {integral.kind for integral in integrals}

   assert {"complex_eigen", "complex_pair"} <= kinds

Нулевая жорданова цепочка и комплексное собственное число
---------------------------------------------------------

Этот пример соответствует смешанной формуле: нулевая жорданова цепочка плюс
комплексное собственное число.

.. math::

   B = J_2(0) \oplus
   \begin{pmatrix}
   3 & -2 \\
   2 & 3
   \end{pmatrix}.

.. code-block:: python

   x = var("x1 x2 x3 x4", domain="real")
   zero_block = matrix(QQ, [[0, 1], [0, 0]])
   complex_block = matrix(QQ, [[3, -2], [2, 3]])
   A = block_diagonal_matrix(zero_block, complex_block).transpose()

   integrals = linear_first_integrals(A, x)
   assert [integral.kind for integral in integrals] == [
       "real_zero",
       "complex_eigen",
       "zero_jordan_complex_radius",
       "zero_jordan_complex_angle",
   ]

Комплексный жорданов блок
-------------------------

Вещественное представление комплексного жорданова блока длины 2 проверяется на
матрице

.. math::

   B =
   \begin{pmatrix}
   2 & -3 & 1 & 0 \\
   3 & 2 & 0 & 1 \\
   0 & 0 & 2 & -3 \\
   0 & 0 & 3 & 2
   \end{pmatrix}.

.. code-block:: python

   x = var("x1 x2 x3 x4", domain="real")
   B = matrix(QQ, [[2, -3, 1, 0], [3, 2, 0, 1], [0, 0, 2, -3], [0, 0, 3, 2]])
   A = B.transpose()

   integrals = linear_first_integrals(A, x)
   kinds = {integral.kind for integral in integrals}

   assert {"complex_eigen", "complex_jordan_exponential", "complex_jordan_angle"} <= kinds

Реализация использует только цепочку с положительной мнимой частью, поэтому
сопряженная цепочка не создает дублирующие угловые интегралы.

Комплексная жорданова цепочка длины 3
-------------------------------------

Для комплексного жорданова блока длины 3 реализация дополнительно возвращает
вещественную и мнимую части старшего инварианта ``Psi``:

.. code-block:: python

   x = var("x1 x2 x3 x4 x5 x6", domain="real")
   B = matrix(
       QQ,
       [
           [2, -3, 1, 0, 0, 0],
           [3, 2, 0, 1, 0, 0],
           [0, 0, 2, -3, 1, 0],
           [0, 0, 3, 2, 0, 1],
           [0, 0, 0, 0, 2, -3],
           [0, 0, 0, 0, 3, 2],
       ],
   )
   A = B.transpose()

   integrals = linear_first_integrals(A, x)
   assert [integral.kind for integral in integrals] == [
       "complex_eigen",
       "complex_jordan_exponential",
       "complex_jordan_angle",
       "complex_jordan_psi_2_real",
       "complex_jordan_psi_2_imaginary",
   ]
