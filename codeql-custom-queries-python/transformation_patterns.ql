/**
 * @name Transformation Patterns
 * @description Identifies code with bifurcation points where small changes create significant transformations
 * @kind problem
 * @problem.severity recommendation
 * @precision high
 * @id python/fractal-communication/transformation
 * @tags transformation
 */

import python

/**
 * A function containing a potential bifurcation point through threshold checking
 */
predicate hasThresholdBifurcation(Function f) {
  exists(Compare compare |
    compare.getScope() = f and
    // Looking for comparison expressions that might represent thresholds
    exists(compare.getComparator(_)) and
    // Connected to a branching structure that significantly changes behavior
    exists(If ifstmt |
      ifstmt.getScope() = f and
      ifstmt.getTest() = compare and
      // Significant difference between branches
      count(Stmt s | s.getParent*() = ifstmt.getBody()) > 3 and
      exists(ifstmt.getOrelse()) and
      count(Stmt s | s.getParent*() = ifstmt.getOrelse()) > 3
    )
  )
}

/**
 * A function that transforms data through multiple stages
 */
predicate hasMultiStageTransformation(Function f) {
  // At least three assignment operations in sequence
  exists(Assign a1, Assign a2, Assign a3 |
    a1.getScope() = f and
    a2.getScope() = f and
    a3.getScope() = f and
    a1 != a2 and a2 != a3 and a1 != a3 and
    a1.getLocation().getStartLine() < a2.getLocation().getStartLine() and
    a2.getLocation().getStartLine() < a3.getLocation().getStartLine() and
    // With each assignment using the result of the previous one
    exists(Name n1, Name n2 |
      n1.getId() = a1.getATarget().(Name).getId() and
      a2.getValue().getASubExpression*() = n1 and
      n2.getId() = a2.getATarget().(Name).getId() and
      a3.getValue().getASubExpression*() = n2
    )
  )
}

/**
 * A function with state-based behavior changes
 */
predicate hasStateDependentTransformation(Function f) {
  // Function that changes behavior based on object state
  exists(Attribute selfAttr, If ifstmt |
    selfAttr.getScope() = f and
    ifstmt.getScope() = f and
    selfAttr.getObject().(Name).getId() = "self" and
    ifstmt.getTest().getASubExpression*() = selfAttr
  )
}

from Function f
where 
  hasThresholdBifurcation(f) or
  hasMultiStageTransformation(f) or
  hasStateDependentTransformation(f)
select f, "This function demonstrates transformation patterns through bifurcation points, multi-stage processing, or state-dependent behavior changes." 