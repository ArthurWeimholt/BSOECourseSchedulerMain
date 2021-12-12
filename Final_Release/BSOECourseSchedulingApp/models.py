"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *
import datetime
from .common import db, Field, auth
from pydal.validators import *


import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_contact_id():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

def get_user():
    return auth.current_user.get('id') if auth.current_user else None


#This is the DataBase file

# New

db.define_table(
    'major',
    Field('name', requires=IS_NOT_EMPTY()),
    Field('requirement_name', requires=IS_NOT_EMPTY()),
)

db.define_table(
    'student',
    Field('student_id', 'reference auth_user', default=get_user),
    Field('major_id', 'reference major'),
    Field('is_admin', 'boolean'),
)

db.define_table(
    'course',
    Field('name', requires=IS_NOT_EMPTY()), # CSE12
    Field('description'),
    Field('unit'),
    Field('full_description'),
    Field('offered_fall', 'boolean', default=True),
    Field('offered_winter', 'boolean', default=True),
    Field('offered_spring', 'boolean', default=True),
    Field('offered_summer', 'boolean', default=True),
    Field('requirement_name', default=None),
)

db.course.offered_fall.readable = db.course.offered_fall.writable = True

db.define_table(
    'studentCourse',
    Field('student_id', 'reference auth_user', default=get_user),
    Field('course_id', 'reference course'),
    Field('season'),  # Fall , Winter, Spring, Summer.
    Field('year'),  # Freshman, Sophomore, Junior, Senior, Extra
    Field('period', 'integer')  # 0-4
)


db.define_table(
    'requirement',
    Field('requirement_name'),
    Field('type'),  # AND, OR, SINGLE
    Field('course_requirement_name'),  # conditional
    Field('course_or_requirement', 'boolean'),  # course requirement boolean true=course false=requirement
)

db.major.truncate()
db.major.insert(name="Computer Science B.S.", requirement_name = "REQComputerScienceB.S.")

#db.course.truncate()
#db.course.insert(name= "CSE 20", description="Beginning Programming in Python", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=False)
#db.course.insert(name= "CSE 30", description="Programming Abstractions: Python", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=False, requirement_name="REQCSE30")
#db.course.insert(name= "CSE 16", description="Applied Discrete Mathematics", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQCSE16")
#db.course.insert(name= "CSE 12", description="Computer Systems and Assembly Language and Lab", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQCSE12")
#db.course.insert(name= "MATH 19A", description="Calculus for Science, Engineering, and Mathematics", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQMATH19A")
#db.course.insert(name= "MATH 19B", description="Calculus for Science, Engineering, and Mathematics", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQMATH19B")
#db.course.insert(name= "MATH 20A", description="Honors Calculus", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQMATH20A")
#db.course.insert(name= "MATH 20B", description="Honors Calculus", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQMATH20B")
#db.course.insert(name= "CSE 13S", description="Computer Systems and C Programming", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=False, requirement_name="REQCSE13S")
#db.course.insert(name= "AM 10", description="Mathematical Methods for Engineers I", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=False, requirement_name="REQAM10")
#db.course.insert(name= "MATH 21", description="Linear Algebra", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQMATH21")
#db.course.insert(name= "AM 30", description="Multivariable Calculus for Engineers", offered_fall = True, offered_winter = False, offered_spring = True, offered_summer=False, requirement_name="REQAM30")
#db.course.insert(name= "MATH 23A", description="Vector Calculus", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQMATH23A")
#db.course.insert(name= "ECE 30", description="Engineering Principles of Electronics", offered_fall = False, offered_winter = False, offered_spring = True, offered_summer=False, requirement_name="REQECE30")


# db.course.truncate()
# db.course.insert(name= "CSE 20", description="Beginning Programming in Python", unit="5", full_description="Provides students with Python programming skills and the ability to design programs and read Python code. Topics include data types, control flow, methods and advanced functions, built-in data structures, and introduction to OOP. No prior programming experience is required.",offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=False)
# db.course.insert(name= "CSE 30", description="Programming Abstractions: Python", unit="7", full_description="Introduction to software development in Python focusing on structuring software in terms of objects endowed with primitive operations. Introduces concepts and techniques via a sequence of concrete case studies. Coursework consists of programming assignments and a final examination.",offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=False, requirement_name="REQCSE30")
# db.course.insert(name= "CSE 16", description="Applied Discrete Mathematics", unit="5", full_description="Introduction to applications of discrete mathematical systems. Topics include sets, functions, relations, graphs, predicate calculus, mathematical proof methods (induction, contraposition, contradiction), counting methods (permutations, combinations), and recurrences. Examples are drawn from computer science and computer engineering.",offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQCSE16")
# db.course.insert(name= "CSE 12", description="Computer Systems and Assembly Language and Lab", unit="5", full_description="Introduction to computer systems and assembly language and how computers compute in hardware and software. Topics include digital logic, number systems, data structures, compiling/assembly process, basics of the system software, and computer architecture.",offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQCSE12")
# db.course.insert(name= "MATH 19A", description="Calculus for Science, Engineering, and Mathematics", unit="5", full_description="The limit of a function, calculating limits, continuity, tangents, velocities, and other instantaneous rates of change. Derivatives, the chain rule, implicit differentiation, higher derivatives. Exponential functions, inverse functions, and their derivatives. The mean value theorem, monotonic functions, concavity, and points of inflection. Applied maximum and minimum problems.", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQMATH19A")
# db.course.insert(name= "MATH 19B", description="Calculus for Science, Engineering, and Mathematics", unit="5", full_description="The definite integral and the fundamental theorem of calculus. Areas, volumes. Integration by parts, trigonometric substitution, and partial fractions methods. Improper integrals. Sequences, series, absolute convergence and convergence tests. Power series, Taylor and Maclaurin series." ,offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQMATH19B")
# db.course.insert(name= "MATH 20A", description="Honors Calculus", unit="5", full_description="Methods of proof, number systems, binomial and geometric sums. Sequences, limits, continuity, and the definite integral. The derivatives of the elementary functions, the fundamental theorem of calculus, and the main theorems of differential calculus.", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQMATH20A")
# db.course.insert(name= "MATH 20B", description="Honors Calculus", unit="5", full_description="Orbital mechanics, techniques of integration, and separable differential equations. Taylor expansions and error estimates, the Gaussian integral, Gamma function and Stirling's formula. Series and power series, numerous applications to physics.", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQMATH20B")
# db.course.insert(name= "CSE 13S", description="Computer Systems and C Programming", unit="7", full_description="C programming, command line, shell programming, editors, debuggers, source code control, and other tools. Basic computer systems, algorithm design and development, data types, program structures. Develops understanding of process model, compile-link-execute build cycle, language-machine interface, memory, and data representation.", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=False, requirement_name="REQCSE13S")
# db.course.insert(name= "AM 10", description="Mathematical Methods for Engineers I", unit="5", full_description="Applications-oriented course on complex numbers and linear algebra integrating Matlab as a computational support tool. Introduction to complex algebra. Vectors, bases and transformations, matrix algebra, solutions of linear systems, inverses and determinants, eigenvalues and eigenvectors, and geometric transformations.", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=False, requirement_name="REQAM10")
# db.course.insert(name= "MATH 21", description="Linear Algebra", unit="5", full_description="Systems of linear equations matrices, determinants. Introduces abstract vector spaces, linear transformation, inner products, the geometry of Euclidean space, and eigenvalues.", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQMATH21")
# db.course.insert(name= "AM 30", description="Multivariable Calculus for Engineers", unit="5", full_description="Advanced multivariate calculus course for engineering majors. Coordinate systems, parametric curves and surfaces; partial derivatives, gradient, Taylor expansion, stationary points, constrained optimization; integrals in multiple dimensions; integrals over curves and surfaces. Applications to engineering form an integral part of the course.",offered_fall = True, offered_winter = False, offered_spring = True, offered_summer=False, requirement_name="REQAM30")
# db.course.insert(name= "MATH 23A", description="Vector Calculus", unit="5", full_description="Vectors in n-dimensional Euclidean space. The inner and cross products. The derivative of functions from n-dimensional to m-dimensional Euclidean space is studied as a linear transformation having matrix representation. Paths in 3-dimensions, arc length, vector differential calculus, Taylor's theorem in several variables, extrema of real-valued functions, constrained extrema and Lagrange multipliers, the implicit function theorem, some applications.", ffered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQMATH23A")
# db.course.insert(name= "ECE 30", description="Engineering Principles of Electronics", unit="5", full_description="Suitable for sophomores pursuing computer science and engineering careers. Aims at deriving basic engineering principles directly from examples relevant to computing and electronics: 1) Newton’s Laws and related fundamental mechanics; 2) basic thermodynamics and heat/energy transfer; 3) key electromagnetic principles, including Coulomb’s Law, Gauss’s Law, and basic circuit analysis using Kirchoff’s Laws/Rules; and 4) Ray optics for fiber optic communications and camera electronics.", offered_fall = False, offered_winter = False, offered_spring = True, offered_summer=False, requirement_name="REQECE30")
# db.course.insert(name= "CSE 101", description="Introduction to Data Structures and Algorithms", unit="5", full_description="Linked lists, stacks, queues, hash tables, trees, heaps, and graphs will be covered. Students will also be taught how to derive big-Oh analysis of simple algorithms. All assignments will be in C/C++. (Formerly Computer Science 101 Algorithms and Abstract Data Types.)", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=False, requirement_name="REQCSE101")
#
# db.course.insert(name= "CSE 102", description="Introduction to Analysis of Algorithms", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=False, requirement_name="REQCSE102", unit="5", full_description="Methods for the systematic construction and mathematical analysis of algorithms. Order notation, the RAM model of computation, lower bounds, and recurrence relations are covered. The algorithm design techniques include divide-and-conquer, branch and bound, and dynamic programming. Applications to combinatorial, graph, string, and geometric algorithms. (Formerly Computer Science 102.)")
# db.course.insert(name= "CSE 103", description="Computational Models", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=False, requirement_name="REQCSE103", unit="5", full_description="Various representations for regular languages, context-free grammars, normal forms, simple parsing, pumping lemmas, Turing machines, the Church-Turing thesis, intractable problems, the P-NP question. (Formerly CMPS 130.)")
# db.course.insert(name= "CSE 106", description="Applied Graph Theory and Algorithms", offered_fall = False, offered_winter = True, offered_spring = False, offered_summer=False, requirement_name="REQCSE106", unit="5", full_description="Basic concepts and algorithms are reviewed including trees, Eulerian and Hamiltonian graphs, and graph transversal. Algorithms are explored to solve problems in connectivity, routing, matching, and embedding of graphs. Graph theory and algorithms are developed around applications in computer engineering. (Formerly Computer Engineering 177.)")
# db.course.insert(name= "CSE 107", description="Probability and Statistics for Engineers", offered_fall = False, offered_winter = True, offered_spring = True, offered_summer=False, requirement_name="REQCSE107", unit="5", full_description="Introduction to fundamental tools of stochastic analysis. Probability, conditional probability; Bayes Theorem; random variables and transforms; independence; Bernnoulli trials. Statistics, inference from limited data; outcomes of repeated experiments; applications to design; assessment of relative frequency and probability; law of large numbers; precision of measurements. Elements of stochastic processes, Poisson processes; Markov chains. Students cannot receive credit for this course and Applied Mathematics and Statistics 131. (Formerly Computer Engineering 107.)")
# db.course.insert(name= "CSE 112", description="Comparative Programming Languages", offered_fall = True, offered_winter = False, offered_spring = True, offered_summer=False, requirement_name="REQCSE112", unit="5", full_description="Covers several programming languages and compares styles, philosophy, and design principles. Principles underlying declarative, functional, and object-oriented programming styles are studied. Students write programs emphasizing each of these techniques. (Formerly Computer Science 112.)")
# db.course.insert(name= "CSE 114A", description="Foundations of Programming Languages", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=False, requirement_name="REQCSE114A", unit="5", full_description="Problem solving emphasizing recursion, data abstraction, and higher-order functions. Introduction to types and type checking, modular programming, and reasoning about program correctness. (Formerly CSE 116, Introduction to Functional Programming.)")
# db.course.insert(name= "CSE 115A", description="Introduction to Software Engineering", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=False, requirement_name="REQCSE115A", unit="5", full_description="Emphasizes the characteristics of well-engineered software systems. Topics include requirements analysis and specification, design, programming, verification and validation, maintenance, and project management. Practical and research methods are studied. Imparts an understanding of the steps used to effectively develop computer software. (Formerly Computer Science 115.)")
# db.course.insert(name= "CSE 120", description="Computer Architecture", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=False, requirement_name="REQCSE120", unit="5", full_description="Introduction to computer architecture including examples of current approaches and the effect of technology and software. Computer performance evaluation, basic combinatorial and sequential digital components, different instruction set architectures with a focus on the MIPS ISA and RISC paradigm. Evolution of CPU microarchitecture from single-cycle to multi-cycle pipelines, with overview of super-scalar, multiple-issue and VLIW. Memory system, cache, virtual memory and relationship between memory and performance. Evolution of PC system architecture. May include advanced topics, such as parallel processing, MIMD, and SIMD.")
# db.course.insert(name= "CSE 130", description="Principles of computer Systems Design", offered_fall = True, offered_winter = True, offered_spring = False, offered_summer=False, requirement_name="REQCSE130", unit="5", full_description="Covers the principles governing computer-systems design and complexity; familiarity with memory, storage, and networking; concurrency and synchronization; layering (abstraction and modularity); naming; client-server and virtualized system models; and performance. Requires significant programming projects demonstrating mastery of these concepts.")
# db.course.insert(name= "MATH 22", description="Introduction to Calculus of Several Variables", offered_fall = False, offered_winter = True, offered_spring = False, offered_summer=True, requirement_name="REQMATH22", unit="5", full_description="Functions of several variables. Continuity and partial derivatives. The chain rule, gradient and directional derivative. Maxima and minima, including Lagrange multipliers. The double and triple integral and change of variables. Surface area and volumes. Applications from biology, chemistry, earth sciences, engineering, and physics. Students cannot receive credit for this course and MATH 23A.")
# db.course.insert(name= "MATH 23A", description="Vector Calculus", offered_fall = True, offered_winter = True, offered_spring = True, offered_summer=True, requirement_name="REQMATH23A", unit="5", full_description="Vectors in n-dimensional Euclidean space. The inner and cross products. The derivative of functions from n-dimensional to m-dimensional Euclidean space is studied as a linear transformation having matrix representation. Paths in 3-dimensions, arc length, vector differential calculus, Taylor's theorem in several variables, extrema of real-valued functions, constrained extrema and Lagrange multipliers, the implicit function theorem, some applications. Students cannot receive credit for this course and MATH 22 or AM 30.")

db.requirement.truncate()
db.requirement.insert(requirement_name="REQCSE30", type="SINGLE", course_requirement_name="CSE 20", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE16", type ="OR", course_requirement_name="MATH 19A", course_or_requirement = "True")
db.requirement.insert(requirement_name="REQCSE16", type ="OR", course_requirement_name="MATH 19B", course_or_requirement = "True")
db.requirement.insert(requirement_name="REQCSE16", type ="OR", course_requirement_name="MATH 20A", course_or_requirement = "True")
db.requirement.insert(requirement_name="REQCSE16", type ="OR", course_requirement_name="MATH 20B", course_or_requirement = "True")

db.requirement.insert(requirement_name="REQCSE12", type ="SINGLE", course_requirement_name="CSE 20", course_or_requirement="True")
db.requirement.insert(requirement_name="REQMATH19B", type="OR", course_requirement_name="MATH 19A", course_or_requirement="True")
db.requirement.insert(requirement_name="REQMATH19B", type="OR", course_requirement_name="MATH 20A", course_or_requirement="True")
db.requirement.insert(requirement_name="REQMATH20B", type="OR", course_requirement_name="MATH 19A", course_or_requirement="True")
db.requirement.insert(requirement_name="REQMATH20B", type="OR", course_requirement_name="MATH 20A", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE13S", type="SINGLE", course_requirement_name="CSE 12", course_or_requirement="True")
db.requirement.insert(requirement_name="REQMATH21", type="OR", course_requirement_name="MATH 19A", course_or_requirement="True")
db.requirement.insert(requirement_name="REQMATH21", type="OR", course_requirement_name="MATH 20A", course_or_requirement="True")
db.requirement.insert(requirement_name="REQAM30", type="OR", course_requirement_name="MATH 19B", course_or_requirement="True")
db.requirement.insert(requirement_name="REQAM30", type="OR", course_requirement_name="MATH 20B", course_or_requirement="True")
db.requirement.insert(requirement_name="REQAM30", type="OR", course_requirement_name="AM 10", course_or_requirement="True")
db.requirement.insert(requirement_name="REQMATH23A", type="OR", course_requirement_name="MATH 19B", course_or_requirement="True")
db.requirement.insert(requirement_name="REQMATH23A", type="OR", course_requirement_name="MATH 20B", course_or_requirement="True")
db.requirement.insert(requirement_name="REQECE30", type="SINGLE", course_requirement_name="MATH 19B", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE101", type="AND", course_requirement_name="CSE 12", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE101", type="AND", course_requirement_name="CSE 13S/CSE 13E", course_or_requirement="False")
db.requirement.insert(requirement_name="REQCSE101", type="AND", course_requirement_name="CSE 16", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE101", type="AND", course_requirement_name="CSE 30", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE101", type="AND", course_requirement_name="MATH 19B/MATH 20B", course_or_requirement="False")
db.requirement.insert(requirement_name="CSE 13S/CSE 13E", type="OR", course_requirement_name="CSE 13S", course_or_requirement="True")
db.requirement.insert(requirement_name="CSE 13S/CSE 13E", type="OR", course_requirement_name="CSE 13E", course_or_requirement="True")
db.requirement.insert(requirement_name="MATH 19B/MATH 20B", type="OR", course_requirement_name="MATH 19B", course_or_requirement="True")
db.requirement.insert(requirement_name="MATH 19B/MATH 20B", type="OR", course_requirement_name="MATH 20B", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE102", type="OR", course_requirement_name="CSE 101", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE103", type="OR", course_requirement_name="CSE 101", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE106", type="OR", course_requirement_name="CSE 101", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE107", type="AND", course_requirement_name="CSE 16", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE107", type="AND", course_requirement_name="MATH 22/MATH 23A", course_or_requirement="False")
db.requirement.insert(requirement_name="MATH 22/MATH 23A", type="OR", course_requirement_name="MATH 22", course_or_requirement="True")
db.requirement.insert(requirement_name="MATH 22/MATH 23A", type="OR", course_requirement_name="MATH 23A", course_or_requirement="True")
db.requirement.insert(requirement_name="REQMATH22", type="OR", course_requirement_name="MATH 19B", course_or_requirement="True")
db.requirement.insert(requirement_name="REQMATH22", type="OR", course_requirement_name="MATH 20B", course_or_requirement="True")
db.requirement.insert(requirement_name="REQMATH23A", type="OR", course_requirement_name="MATH 19B", course_or_requirement="True")
db.requirement.insert(requirement_name="REQMATH23A", type="OR", course_requirement_name="MATH 20B", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE112", type="OR", course_requirement_name="CSE 101", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE114A", type="OR", course_requirement_name="CSE 101", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE115A", type="AND", course_requirement_name="CSE 101", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE115A", type="AND", course_requirement_name="CSE 130", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE120", type="AND", course_requirement_name="CSE 12", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE120", type="AND", course_requirement_name="CSE 13S/CSE 13E", course_or_requirement="False")
db.requirement.insert(requirement_name="REQCSE130", type="AND", course_requirement_name="CSE 12", course_or_requirement="True")
db.requirement.insert(requirement_name="REQCSE130", type="AND", course_requirement_name="CSE 101", course_or_requirement="True")

db.student.truncate()
db.student.insert(student_id=4, major_id=1, is_admin = True)
db.student.insert(student_id=5, major_id=1, is_admin = True)


db.commit()
