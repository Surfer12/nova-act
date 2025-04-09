/**
 * @name Grounding and Safety Anchors
 * @description Identifies error handling and validation patterns that provide grounding and safety anchors
 * @kind problem
 * @problem.severity recommendation
 * @precision high
 * @id python/fractal-communication/grounding-safety
 * @tags safety_anchor
 *       grounding
 */

import python

/**
 * A try-except block that provides error handling
 */
class ErrorHandlingBlock extends Try {
  ErrorHandlingBlock() {
    // Has at least one exception handler
    exists(ExceptStmt except | except = this.getAHandler())
  }
}

/**
 * A function that validates its inputs before processing
 */
predicate hasInputValidation(Function f) {
  exists(If ifstmt |
    // Inside the function
    ifstmt.getScope() = f and
    // Near the beginning of the function
    ifstmt.getLocation().getStartLine() <= f.getLocation().getStartLine() + 5 and
    // Contains parameter reference
    exists(Name name |
      name.getLocation().getStartLine() = ifstmt.getLocation().getStartLine() and
      name.getId() = f.getAnArg().getAsName().getId()
    )
  )
}

/**
 * A function with both error handling and input validation
 */
predicate hasGroundingAndSafety(Function f) {
  // Has input validation
  hasInputValidation(f) and
  // Has error handling
  exists(ErrorHandlingBlock tryblock |
    tryblock.getScope() = f
  )
}

from Function f
where hasGroundingAndSafety(f)
select f, "This function implements grounding and safety anchors through input validation and error handling." 