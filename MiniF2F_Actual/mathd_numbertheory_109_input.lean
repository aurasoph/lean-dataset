import Mathlib

theorem mathd_numbertheory_109 (v : ℕ → ℕ) (h₀ : ∀ n, v n = 2 * n - 1) :
  (∑ k in Finset.Icc 1 100, v k) % 7 = 4 := by
