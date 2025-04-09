/**
 * @name Recursive Pattern Detection
 * @description Identifies recursive function patterns that reflect the fractal communication structure z = z² + c
 * @kind problem
 * @problem.severity recommendation
 * @precision high
 * @id python/fractal-communication/recursive-patterns
 * @tags fractal-framework
 *       integration
 *       transformation
 */

import python

/**
 * A function that calls itself directly (simple recursion)
 */
predicate isDirectlyRecursive(Function f) {
  exists(Call call |
    call.getScope() = f and
    call.getFunc().(Name).getId() = f.getName()
  )
}

/**
 * A function that transforms its own result and adds new input (embodying z = z² + c pattern)
 */
predicate hasFractalPattern(Function f) {
  // Function is recursive
  isDirectlyRecursive(f) and
  
  // Has at least one parameter (input c)
  f.getArgCount() > 0 and
  
  // Contains operations that could represent transformation of previous state
  exists(BinaryExpr binop |
    binop.getScope() = f and
    (binop.getOp() instanceof Add or binop.getOp() instanceof Mult)
  )
}

from Function f
where hasFractalPattern(f)
select f, "This function exhibits a fractal communication pattern with recursive transformation and external input integration." 