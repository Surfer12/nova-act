/**
 * @name Embodiment Patterns
 * @description Identifies code that embodies abstract concepts through concrete implementations
 * @kind problem
 * @problem.severity recommendation
 * @precision high
 * @id python/fractal-communication/embodiment
 * @tags embodiment
 *       return_anchor
 */

import python

/**
 * A class that concretely implements an abstract interface
 */
predicate implementsAbstractInterface(Class c) {
  // Class inherits from an ABC or interface
  exists(ClassExpr baseClass |
    baseClass = c.getABase() and
    (
      // Either inherits from ABC
      exists(Name name |
        name = baseClass.(Name) and
        name.getId() = "ABC"
      ) or
      // Or has abstract methods
      exists(Function method |
        method.getScope() = baseClass.(ClassExpr).getDefinedClass() and
        method.getName().matches("%abstract%")
      )
    )
  )
}

/**
 * A function that translates between abstract domain concepts and concrete implementations
 */
predicate performsAbstractConcreteTranslation(Function f) {
  // Function has descriptive documentation that mentions abstract concepts
  exists(string docstring |
    docstring = f.getDocString().getText() and
    (
      docstring.matches("%abstract%concrete%") or
      docstring.matches("%concept%implementation%") or
      docstring.matches("%model%representation%")
    )
  )
}

/**
 * A function that converts user intent into system actions
 */
predicate convertsIntentToAction(Function f) {
  // Has command pattern or similar "intent to action" translation
  (
    // Command pattern with execute method
    f.getName() = "execute" or
    f.getName() = "run" or
    f.getName() = "perform" or
    f.getName() = "apply"
  ) and
  // Takes an action parameter or has action in signature
  (
    exists(Parameter p |
      p = f.getAnArg() and
      (
        p.getName() = "action" or
        p.getName() = "command" or
        p.getName() = "operation"
      )
    ) or
    f.getQualifiedName().matches("%Action%") or
    f.getQualifiedName().matches("%Command%")
  )
}

from AstNode node
where 
  (
    node instanceof Class and implementsAbstractInterface(node) 
  ) or (
    node instanceof Function and
    (performsAbstractConcreteTranslation(node) or convertsIntentToAction(node))
  )
select node, "This element demonstrates embodiment patterns by converting abstract concepts to concrete implementations." 