import Mathlib

/- Negative fixture: intentionally incomplete. Never import into a delivery library.
The goal is to catch acceptance based only on absence of sorry in the main proof.
Not compiled in the package-building environment. -/

namespace EulerLeanProNegative

lemma admitted_upper (a b : ℝ) : 2 * a * b ≤ a ^ 2 + b ^ 2 := by
  sorry

theorem misleading_main (a b : ℝ) : 2 * a * b ≤ a ^ 2 + b ^ 2 := by
  exact admitted_upper a b

-- Run this in an isolated test project; inspect the actual returned axioms.
#print axioms misleading_main

end EulerLeanProNegative
