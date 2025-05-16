**Description of versions (branches)**
_These notes refer to the original repository and only the final version of the code is avaialble here, but these notes have been kept to showcase the progress of work in this project._

Version 2: Before professor's notes in his email on 18 April 2025.

Version 7: Added file for calculating B_4

Version 9: Latest update to code for calculating B_4

Version 11: Noticed errors in true value of B_4 and minor spelling, but value is incorrect (outputs 23.400781524807606)

Version 12: Added a factor to the final sum to take into account the difference between units in the value accepted (http://www.sklogwiki.org/SklogWiki/index.php/Hard_sphere:_virial_coefficients) (in units of a hard sphere volume) and the units of the value calculated in the program (in units of sigma)

Version 14: Cluster integrals 1 and 3 should be negative because they have an even number of conenctions (they are positive but the overall sign is ngative) so update to fix this (need to inverstiage theory behind this). Also another issue is that N=10^5 gives closer value than N=10^6.

Version 19: Final version of logarithmic graphs, note that data was removed from CSV files to simplify them.
