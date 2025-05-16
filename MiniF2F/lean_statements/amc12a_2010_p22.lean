import Mathlib

theorem amc12a_2010_p22 (x : ℝ) : 49 ≤ ∑ k:ℤ in Finset.Icc 1 119, abs (↑k * x - 1) := by
