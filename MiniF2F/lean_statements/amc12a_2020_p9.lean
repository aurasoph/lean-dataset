import Mathlib

theorem amc12a_2020_p9 (S : Finset ℝ)
    (h₀ : ∀ x : ℝ, x ∈ S ↔ 0 ≤ x ∧ x ≤ 2 * Real.pi ∧ Real.tan (2 * x) = Real.cos (x / 2)) : S.card = 5 := by
