/**
 * @name Openness and Curiosity Patterns
 * @description Identifies code patterns that exhibit openness and curiosity through exploration of multiple options
 * @kind problem
 * @problem.severity recommendation
 * @precision high
 * @id python/fractal-communication/openness-curiosity
 * @tags curiosity_anchor
 *       openness
 */

import python

/**
 * A function that explores multiple paths/options
 */
predicate hasMultiplePathExploration(Function f) {
  exists(If ifstmt |
    // Inside the function
    ifstmt.getScope() = f and
    // Has both if and else branches
    exists(ifstmt.getBody()) and
    exists(ifstmt.getOrelse())
  )
}

/**
 * A function that tries different approaches or patterns
 */
predicate hasDiverseApproaches(Function f) {
  // Contains multiple distinct operation types
  count(BinaryExpr binop | 
    binop.getScope() = f | 
    binop.getOp().getClass()
  ) >= 3 or
  
  // Uses different data structure types
  exists(Call call1, Call call2 |
    call1.getScope() = f and
    call2.getScope() = f and
    call1 != call2 and
    (
      call1.getFunc().(Name).getId() = "list" and
      call2.getFunc().(Name).getId() = "dict"
    )
  )
}

/**
 * Functions that exhibit openness through polymorphic behavior
 */
predicate hasPolymorphicPattern(Function f) {
  // Function with type checking that handles different types differently
  exists(Call isinstance |
    isinstance.getScope() = f and
    isinstance.getFunc().(Name).getId() = "isinstance" and
    // Connected to a branching structure
    exists(If ifstmt |
      ifstmt.getScope() = f and
      // The isinstance call is in the test condition
      ifstmt.getTest().getASubExpression*() = isinstance
    )
  )
}

from Function f
where 
  hasMultiplePathExploration(f) and
  (hasDiverseApproaches(f) or hasPolymorphicPattern(f))
select f, "This function demonstrates openness and curiosity through exploration of multiple paths and approaches." 