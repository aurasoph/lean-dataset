import Mathlib

theorem mathd_numbertheory_257 (x : ℕ) (h₀ : 1 ≤ x ∧ x ≤ 100)
    (h₁ : 77 ∣ (∑ k in Finset.range 101, k) - x) : x = 45 := by
