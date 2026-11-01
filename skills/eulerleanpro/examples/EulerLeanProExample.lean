import Mathlib

/-!
# A readable formalization example

For real numbers a and b, |2ab| ≤ a² + b².
The proof uses nonnegativity of (a-b)² and (a+b)² to obtain two bounds.

This bundled example has NOT been compiled in the package-building environment.
Build it using the receiving project's pinned Lean/Mathlib environment.
-/

namespace EulerLeanProExample

/-- Nonnegativity of `(a-b)^2` gives the upper bound on twice the product. -/
lemma twice_mul_upper (a b : ℝ) : 2 * a * b ≤ a ^ 2 + b ^ 2 := by
  nlinarith [sq_nonneg (a - b)]

/-- Nonnegativity of `(a+b)^2` gives the corresponding lower bound. -/
lemma twice_mul_lower (a b : ℝ) : -(a ^ 2 + b ^ 2) ≤ 2 * a * b := by
  nlinarith [sq_nonneg (a + b)]

/-- Twice the absolute product is bounded by the sum of the squares. -/
theorem abs_twice_mul_le (a b : ℝ) : |2 * a * b| ≤ a ^ 2 + b ^ 2 := by
  exact abs_le.mpr ⟨twice_mul_lower a b, twice_mul_upper a b⟩

end EulerLeanProExample
