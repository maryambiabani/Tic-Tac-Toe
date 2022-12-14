import numpy as np
#_________________________________make _game_base_matrix_____________________________________
class Game_Base:
    def __init__(self):
        return
    game_base_matrix = [[]]
    game_base_matrix_row = []
    def fill(self):
        import itertools
        game_base_matrix = list(itertools.product([0, 1, 2], repeat=9))
        return game_base_matrix

    def is_feasible(self,row):
        number_of_x = 0
        number_of_o = 0
        number_of_no = 0
        feasibility = False

        for i in range(len(row)):
            if row[i] == 1:
                number_of_x = number_of_x + 1
            if row[i] == 2:
                number_of_o = number_of_o + 1
            if row[i] == 0:
                number_of_no = number_of_no + 1
        row = row + ((len(row) - number_of_no),)

        if number_of_x == number_of_o + 1 or number_of_x == number_of_o or number_of_o == number_of_x + 1:
            feasibility = True

        return feasibility, row

    def rotate_90(self, matrix):
        rotated90 = zip(*matrix[::-1])
        test2 = list(zip(*matrix[::-1]))
        zipped_list = test2[:]
        rotated90 = list(test2)
        return rotated90

    def rotate_180(self, matrix):
        rotated180 = self.rotate_90(self.rotate_90(matrix))
        return rotated180

    def rotate_270(self, matrix):
        rotated270 = self.rotate_90(self.rotate_90(self.rotate_90(matrix)))
        return rotated270

    def flip_h(self,A):
        A = np.flipud(A)
        return A

    def flip_v(self,A):
        A = np.fliplr(A)
        return A
    def build_matrix(self):

        game_base_matrix = self.fill()
        # REMOVE INFEASIBLES
        # ADD GAME LEVEL
        final_game_base_matrix = []

        for i in range(len(game_base_matrix)):
            f = False
            f, r = self.is_feasible(game_base_matrix[i])
            if f:
                final_game_base_matrix.append(r)

        game_base = final_game_base_matrix.copy()
        game_base_without_Level = final_game_base_matrix.copy()
        wLevel = []
        index_number = []
        for row in game_base_without_Level:
            row = list(row)
            del row[9]
            wLevel.append(row)

        for row in wLevel:

            matrix = np.reshape(row, (3, 3))
            m_90 =self.rotate_90(matrix)
            m_90_h = self.flip_h(m_90)
            m_90_v = self.flip_v(m_90)
            m_90 = np.reshape(m_90, (1, 9)).tolist()
            m_90_h = np.reshape(m_90_h, (1, 9)).tolist()
            m_90_v = np.reshape(m_90_v, (1, 9)).tolist()
            if m_90[0] in wLevel:
                index_number.append(wLevel.index(m_90[0]))
                wLevel.remove(m_90[0])
            if m_90_h[0] in wLevel:
                index_number.append(wLevel.index(m_90_h[0]))
                wLevel.remove(m_90_h[0])
            if m_90_v[0] in wLevel:
                index_number.append(wLevel.index(m_90_v[0]))
                wLevel.remove(m_90_v[0])

            m_180 = self.rotate_180(matrix)
            m_180_h = self.flip_h(m_180)
            m_180_v = self.flip_v(m_180)
            m_180 = np.reshape(m_180, (1, 9)).tolist()
            m_180_h = np.reshape(m_180_h, (1, 9)).tolist()
            m_180_v = np.reshape(m_180_v, (1, 9)).tolist()

            if m_180[0] in wLevel:
                index_number.append(wLevel.index(m_180[0]))
                wLevel.remove(m_180[0])
            if m_180_h[0] in wLevel:
                index_number.append(wLevel.index(m_180_h[0]))
                wLevel.remove(m_180_h[0])
            if m_180_v[0] in wLevel:
                index_number.append(wLevel.index(m_180_v[0]))
                wLevel.remove(m_180_v[0])

            m_270 = self.rotate_270(matrix)
            m_270_h = self.flip_h(m_270)
            m_270_v = self.flip_v(m_270)
            m_270 = np.reshape(m_270, (1, 9)).tolist()
            m_270_h = np.reshape(m_270_h, (1, 9)).tolist()
            m_270_v = np.reshape(m_270_v, (1, 9)).tolist()
            if m_270[0] in wLevel:
                index_number.append(wLevel.index(m_270[0]))
                wLevel.remove(m_270[0])
            if m_270_h[0] in wLevel:
                index_number.append(wLevel.index(m_270_h[0]))
                wLevel.remove(m_270_h[0])
            if m_270_v[0] in wLevel:
                index_number.append(wLevel.index(m_270_v[0]))
                wLevel.remove(m_270_v[0])

            m_v = self.flip_v(matrix)
            m_v = np.reshape(m_v, (1, 9)).tolist()
            if m_v[0] in wLevel:
                index_number.append(wLevel.index(m_v[0]))
                wLevel.remove(m_v[0])

            m_h = self.flip_h(matrix)
            m_h = np.reshape(m_h, (1, 9)).tolist()
            if m_h[0] in wLevel:
                index_number.append(wLevel.index(m_h[0]))
                wLevel.remove(m_h[0])

            m_d = np.transpose(self.rotate_180(matrix))
            m_d = np.reshape(m_d, (1, 9)).tolist()
            if m_d[0] in wLevel:
                index_number.append(wLevel.index(m_d[0]))
                wLevel.remove(m_d[0])
        final_matrix = []
        final_matrix.append(tuple([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
        final_matrix.append(tuple([1, 0, 0, 0, 0, 0, 0, 0, 0, 1]))
        final_matrix.append(tuple([0, 1, 0, 0, 0, 0, 0, 0, 0, 1]))
        final_matrix.append(tuple([0, 0, 0, 0, 1, 0, 0, 0, 0, 1]))
        final_matrix.append(tuple([2, 0, 0, 0, 0, 0, 0, 0, 0, 1]))
        final_matrix.append(tuple([0, 2, 0, 0, 0, 0, 0, 0, 0, 1]))
        final_matrix.append(tuple([0, 0, 0, 0, 2, 0, 0, 0, 0, 1]))
        for index in index_number:
            final_game_base_matrix.pop(index)
        for i in final_game_base_matrix:
            final_matrix.append(i)

        final_matrix.sort(key=lambda x: x[9])
        # print(final_matrix)
        return final_matrix,game_base
