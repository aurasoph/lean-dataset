import Mathlib

theorem mathd_algebra_342 (a d : ℝ) (h₀ : (∑ k in Finset.range 5, a + k * d) = 70)
    (h₁ : (∑ k in Finset.range 10, a + k * d) = 210) : a = 42 / 5 := by
