import Mathlib

theorem algebra_amgm_sqrtxymulxmyeqxpy_xpygeq4 (x y : ℝ) (h₀ : 0 < x ∧ 0 < y) (h₁ : y ≤ x)
  (h₂ : Real.sqrt (x * y) * (x - y) = x + y) : x + y ≥ 4 := by
