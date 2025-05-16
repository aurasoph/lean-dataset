import Mathlib

theorem imo_1962_p4 (S : Set ℝ)
    (h₀ : S = { x : ℝ | Real.cos x ^ 2 + Real.cos (2 * x) ^ 2 + Real.cos (3 * x) ^ 2 = 1 }) :
    S =
      { x : ℝ |
        ∃ m : ℤ,
          x = Real.pi / 2 + m * Real.pi ∨
            x = Real.pi / 4 + m * Real.pi / 2 ∨ x = Real.pi / 6 + m * Real.pi / 6 ∨ x = 5 * Real.pi / 6 + m * Real.pi / 6 } := by
