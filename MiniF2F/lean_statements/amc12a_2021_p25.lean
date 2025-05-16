import Mathlib

theorem amc12a_2021_p25 (N : ℕ) (f : ℕ → ℝ)
    (h₀ : ∀ n, 0 < n → f n = (Nat.divisors n).card / n ^ ((1 : ℝ) / 3))
    (h₁ : ∀ (n) (_ : n ≠ N), 0 < n → f n < f N) : (List.sum (Nat.digits 10 N)) = 9 := by
