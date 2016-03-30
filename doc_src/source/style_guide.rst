.. title:: Style Guide


Style Guide
===========

Follow or perish!


C++
===


- Public Types (class, struct, usings): UpperCamelCase
  (http://www.stroustrup.com/bs_faq2.html#Hungarian)

- Methods, Variables: underscore_case

- Make sure directory/module structure matches namespace-structure for user-expected includes

- Code is required, by a decree of the High Command of His Majesty Emperor C. Frescolino, to compile with these flags on gcc:

    -Werror -Wall -Wextra -Wpedantic

- It is highly recommended to compile it at least on clang and icc as well. For clang, the following settings are recommended:

    -Werror -Weverything

  and these optionally (plus any deemed useful on a case-by-case basis):

    -Wno-c++98-compat -Wno-c++98-compat-pedantic -Wno-missing-prototypes -Wno-exit-time-destructors -Wno-global-constructors -Wno-implicit-fallthrough -Wno-disabled-macro-expansion -Wno-documentation-unknown-command



Python
======

https://www.python.org/dev/peps/pep-0008/
