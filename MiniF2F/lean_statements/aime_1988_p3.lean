import Mathlib

theorem aime_1988_p3 (x : ℝ) (h₀ : 0 < x)
  (h₁ : Real.logb 2 (Real.logb 8 x) = Real.logb 8 (Real.logb 2 x)) : Real.logb 2 x ^ 2 = 27 := by
