/**
 * @name Integration Patterns
 * @description Identifies code that connects across different domains or systems to create coherent functionality
 * @kind problem
 * @problem.severity recommendation
 * @precision high
 * @id python/fractal-communication/integration
 * @tags integration
 */

import python

/**
 * A function that connects multiple modules or libraries
 */
predicate connectsMultipleDomains(Function f) {
  // Count distinct imported modules used
  count(ImportExpr imp, Call call |
    call.getScope() = f and
    call.getFunc().(Attribute).getObject().(Name).getId() = imp.getName() |
    imp
  ) >= 2
}

/**
 * A function that transforms data between different formats
 */
predicate performsDataTransformation(Function f) {
  // Has data structure creation and manipulation
  exists(Call dictCreation, Call jsonOp |
    dictCreation.getScope() = f and
    jsonOp.getScope() = f and
    (
      dictCreation.getFunc().(Name).getId() = "dict" or
      dictCreation instanceof DictExpr
    ) and
    exists(Attribute attr |
      attr = jsonOp.getFunc() and
      attr.getObject().(Name).getId() = "json"
    )
  )
}

/**
 * A function that integrates user input with system operations
 */
predicate integratesUserAndSystem(Function f) {
  // Has both input functions and system operations
  exists(Call inputCall, Call systemCall |
    inputCall.getScope() = f and
    systemCall.getScope() = f and
    (
      inputCall.getFunc().(Name).getId() = "input" or
      exists(Attribute attr |
        attr = inputCall.getFunc() and
        attr.getObject().(Name).getId() = "input"
      )
    ) and
    (
      exists(Attribute attr |
        attr = systemCall.getFunc() and
        (
          attr.getObject().(Name).getId() = "os" or
          attr.getObject().(Name).getId() = "sys" or
          attr.getObject().(Name).getId() = "path"
        )
      )
    )
  )
}

from Function f
where 
  (connectsMultipleDomains(f) or performsDataTransformation(f) or integratesUserAndSystem(f))
select f, "This function demonstrates integration by connecting different domains, transforming data between formats, or bridging user input with system operations." 