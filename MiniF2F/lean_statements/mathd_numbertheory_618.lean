import Mathlib

theorem mathd_numbertheory_618 (n : ℕ) (p : ℕ → ℕ) (h₀ : ∀ x, p x = x ^ 2 - x + 41)
    (h₁ : 1 < Nat.gcd (p n) (p (n + 1))) : 41 ≤ n := by
