from Lib import csv
import numpy

class MyError(RuntimeError):
    def __init__(self, msg):
        self.message = msg
    # ^^^ __init__ ^^^
# ^^^ class MyPacketError ^^^

class gauss:
    def __init__(self):
        self.A = []
        self.B = []
        with open('A.csv', newline='') as csvfile:
            readerA = csv.reader(csvfile, delimiter=' ')
            i = 0
            for row in readerA:
                self.A.append([])
                for elem in row:
                    self.A[i].append(int(elem))
                i += 1
        with open('B.csv', newline='') as csvfile:
            readerB = csv.reader(csvfile, delimiter=' ')
            for row in readerB:
                self.B.append(int(row[0]))
    # ^^^ def __init__

    def solve(self):
        if not self.check():
            return
        n = len(self.A)
        self.straight(n)
        X = self.reverse(n)
        return X
    # ^^^ def solve

    def check(self):
        try:
            # rows check:
            if len(self.A) != len(self.B):
                raise MyError('Ошибка: размеры матриц A и B не соответствуют друг другу.')
            # square A check:
            for i in range(1, len(self.A)):
                if len(self.A[i]) != len(self.A[i-1]):
                    raise MyError('Ошибка: матрица A не квадратная.')
            # determinant A
            detA = numpy.linalg.det(numpy.array(self.A))
            if detA == 0:
                raise MyError('Ошибка: матрица A вырожденная.')
            # if has solutions
            extendedA = self.A.copy()
            for i in range(0, len(self.A)):
                extendedA[i].append(self.B[i])
            rankExtA = numpy.linalg.matrix_rank(numpy.array(extendedA))
            rankA = numpy.linalg.matrix_rank(numpy.array(self.A))
            if rankA != rankExtA:
                raise MyError('Ошибка: СЛАУ несовместна.')
        except MyError as e:
            print(e.message)
            return False
        # if A[0][0] is zero, swap lines
        if self.A[0][0] == 0:
            for i in range(1, len(self.A)):
                if self.A[i][0] != 0:
                    print('Внимание: A[0][0]=0. A[0] и A[' + str(i) + '] переставлены.')
                    self.A[0], self.A[i] = self.A[i], self.A[0]
                    self.B[0], self.B[i] = self.B[i], self.B[0]
                    break
        return True

    # ^^^ def check
    def straight(self, n):
        for k in range(0, n-1):
            for i in range(k+1, n):
                t = self.A[i][k] / self.A[k][k]
                self.A[i][k] = 0
                for j in range(k+1, n):
                    self.A[i][j] -= t * self.A[k][j]
                self.B[i] -= t * self.B[k]
    # ^^^ def straight

    def reverse(self, n):
        X = [None] * n
        X[n - 1] = self.B[n - 1] / self.A[n - 1][n - 1]
        for i in range(n - 2, -1, -1):
            sum = 0
            for j in range(i + 1, n):
                sum += self.A[i][j] * X[j]
            X[i] = (self.B[i] - sum) / self.A[i][i]
        return X
    # ^^^ def reverse

# ^^^ class gauss

