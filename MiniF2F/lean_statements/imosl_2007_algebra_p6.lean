import Mathlib

theorem imosl_2007_algebra_p6 (a : ℕ → NNReal) (h₀ : (∑ x in Finset.range 100, a (x + 1) ^ 2) = 1) :
    (∑ x in Finset.range 99, a (x + 1) ^ 2 * a (x + 2)) + a 100 ^ 2 * a 1 < 12 / 25 := by
