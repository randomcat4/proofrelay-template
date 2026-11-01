import Mathlib

/- Negative semantic fixture. It may be type-correct, but does NOT prove the
unconditional inequality: the target is already a field of the input.
Never import into a delivery library. Not compiled during package construction. -/

namespace EulerLeanProNegative

structure AssumedBound (a b : ℝ) : Prop where
  result : |2 * a * b| ≤ a ^ 2 + b ^ 2

theorem misleading_conditional (a b : ℝ) (h : AssumedBound a b) :
    |2 * a * b| ≤ a ^ 2 + b ^ 2 := by
  exact h.result

end EulerLeanProNegative
