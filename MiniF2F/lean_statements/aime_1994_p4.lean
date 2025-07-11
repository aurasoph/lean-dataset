import Mathlib

theorem aime_1994_p4 (n : ℕ) (h₀ : 0 < n)
  (h₀ : (∑ k in Finset.Icc 1 n, Int.floor (Real.logb 2 k)) = 1994) : n = 312 := by
