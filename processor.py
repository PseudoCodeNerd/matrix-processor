class Matrix(object):
    def __init__(self, R=1, C=1):
        """
        takes two ints : R and C specifying rows and columns of matrix
        Default is 1x1 0 matrix (or simply 0).
        """
        self.R = int(R)
        self.C = int(C)
        self.matrix = [[0 for c in range(self.C)] for r in range(self.R)]

    def check_dims(self, other):
        if (self.R == other.R) and (self.C == other.C):
            return True
        else:
            return False

    def has_floats(self, inp):
        return ((sum([elem.isdigit() for elem in inp])) < len(inp))

    def make(self):
        for i in range(self.R):
            row = input().split(maxsplit=self.C)
            if self.has_floats(row):
                self.matrix[i] = list(map(float, row))
            else:
                self.matrix[i] = list(map(int, row))

    def __str__(self):
        vis = ""
        for i in range(self.R):
            vis += f'{" ".join([str(j) for j in self.matrix[i]])}\n'
        return vis

    def __add__(self, other):
        if self.check_dims(other):
            M = Matrix(self.R, self.C)
            for i in range(self.R):
                for j in range(self.C):
                    M.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]
            return M
        else:
            return "The operation cannot be performed."

    def __sub__(self, other):
        if self.check_dims(other):
            M = Matrix(self.R, self.C)
            for i in range(self.R):
                for j in range(self.C):
                    M.matrix[i][j] = self.matrix[i][j] - other.matrix[i][j]
            return M
        else:
            return "The operation cannot be performed."

    def __mul__(self, other):
        # Case 1: Integer multiplication
        if isinstance(other, int) or isinstance(other, float):
            M = Matrix(self.R, self.C)
            M.matrix = [[round(n * other, 3) + 0 for n in self.matrix[i]] for i in range(self.R)]
        # Case 2: Matrix multiplication
        elif isinstance(other, Matrix):
            if self.C != other.R: raise ValueError
            M = Matrix(self.R, other.C)
            for i in range(self.R):
                for j in range(other.C):
                    for k in range(other.R):
                        M.matrix[i][j] += self.matrix[i][k] * other.matrix[k][j]
        else:
            return "The operation cannot be performed."
        return M

    def transpose(self, m):
        M = Matrix(self.R, self.C)
        M.matrix = [[m[j][i] for j in range(self.C)] for i in range(self.R)]
        return M

    def hori_transpose(self):
        M = Matrix(self.R, self.C)
        n = self.R - 1
        for i in range(self.R): M.matrix[i] = self.matrix[n - i]
        return M

    def ver_transpose(self):
        M = Matrix(self.R, self.C)
        M.matrix = [[self.matrix[i][self.C - 1 - j] for j in range(self.C)] for i in range(self.R)]
        return M

    def side_transpose(self):
        M = Matrix(self.R, self.C)
        M.matrix = [[self.matrix[self.C - 1 - j][self.R - 1 - i] for j in range(self.C)] for i in range(self.R)]
        return M

    def det_recur(self, A):
        d = 0
        # Base Case
        if len(A) == 2 and len(A[0]) == 2:
            v = A[0][0] * A[1][1] - A[1][0] * A[0][1]
            return v
        for c in range(len(A)):
            d += ((-1) ** c) * A[0][c] * self.det_recur(self.get_minor(A, 0, c))
        return d

    def determinant(self):
        if len(self.matrix[0]) == 1:
            return self.matrix[0][0]
        elif (self.R == self.C) and (self.R != 1):
            M = self.matrix
            return self.det_recur(M)
        else:
            return "The operation cannot be performed."

    def get_minor(self, M, a, b):
        return [row[:b] + row[b + 1:] for row in (M[:a] + M[a + 1:])]

    def inverse(self):
        M = self.matrix
        if len(M[0]) == 1:
            return 1 / M[0][0]
        elif len(M) == 2:
            det = self.det_recur(M)
            return [[M[1][1] / det, -1 * M[0][1] / det], [-1 * M[1][0] / det, M[0][0] / det]]
        elif (self.det_recur(M) != 0) and (self.R == self.C):
            det = self.determinant()
            cofacts = []
            for r in range(len(M)):
                cofact_r = []
                for c in range(len(M)):
                    minor = self.get_minor(M, r, c)
                    cofact_r.append(((-1) ** (r + c)) * self.det_recur(minor))
                cofacts.append(cofact_r)
            cofact_T = self.transpose(cofacts)
            return cofact_T * (1 / det)
        else:
            return "This matrix doesn't have an inverse."


def init():
    transpose = {1: "Main diagonal", 2: "Side Diagonal", 3: "Vertical line", 4: "Horizontal line"}
    welp = {1: "Add Matrices", 2: "Multiply matrix by a constant", 3: "Multiply matrices", 4: "Transpose matrix",
            5: "Calculate a determinant", 6: "Inverse matrix", 0: "Exit"}
    init_b = True
    while init_b:
        for f in welp.keys():
            print("{}. {}".format(f, welp[f]))
        i = int(input("Your choice: "))
        if i == 0:
            init_b = False
        elif i == 1:
            a, b = map(int, input("Enter size of first matrix: ").split())
            A = Matrix(a, b)
            print("Enter first matrix: ")
            A.make()
            c, d = map(int, input("Enter size of second matrix: ").split())
            B = Matrix(c, d)
            print("Enter second matrix: ")
            B.make()
            print("The result is: ")
            print(A + B)
        elif i == 2:
            a, b = map(int, input("Enter size of matrix: ").split())
            A = Matrix(a, b)
            print("Enter matrix:")
            A.make()
            B = input("Enter constant: ")
            if B.isdigit():
                B = int(B)
            else:
                B = float(B)
            print("The result is: ")
            print(A * B)
        elif i == 3:
            a, b = map(int, input("Enter size of first matrix: ").split())
            A = Matrix(a, b)
            print("Enter first matrix: ")
            A.make()
            c, d = map(int, input("Enter size of second matrix: ").split())
            B = Matrix(c, d)
            print("Enter second matrix: ")
            B.make()
            print("The result is: ")
            print(A * B)
        elif i == 4:
            print()
            for g in transpose.keys():
                print("{}. {}".format(g, transpose[g]))
            j = int(input("Your choice: "))
            a, b = map(int, input("Enter matrix size: ").split())
            A = Matrix(a, b)
            print("Enter matrix: ")
            A.make()
            print("The result is: ")
            if j == 1:
                print(A.transpose(A.matrix))
            elif j == 2:
                print(A.side_transpose())
            elif j == 3:
                print(A.ver_transpose())
            elif j == 4:
                print(A.hori_transpose())
            else:
                print("Choose an operation.")
        elif i == 5:
            a, b = map(int, input("Enter matrix size: ").split())
            A = Matrix(a, b)
            print("Enter matrix: ")
            A.make()
            print("The result is: ")
            print(A.determinant())
        elif i == 6:
            a, b = map(int, input("Enter matrix size: ").split())
            A = Matrix(a, b)
            print("Enter matrix: ")
            A.make()
            print("The result is: ")
            print(A.inverse())


init()
"""
2.65 3.54 3.88 8.99
3.12 5.45 7.77 5.56
5.31 2.23 2.33 9.81
1.67 1.67 1.01 9.99
"""