import Mathlib

theorem aime_1994_p3 (x : ℤ) (f : ℤ → ℤ) (h0 : f x + f (x - 1) = x ^ 2) (h1 : f 19 = 94) :
    f 94 % 1000 = 561 := by
