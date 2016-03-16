"""
For Project 4, you will work with two types of matrices: alignment matrices and 
scoring matrices. Alignment matrices will follow the same indexing scheme that we 
used for grids in "Principles of Computing". Entries in the alignment matrix will 
be indexed by their row and column with these integer indices starting at zero. We 
will model these matrices as lists of lists in Python and can access a particular 
entry via an expression of the form alignment_matrix[row][col].
For scoring matrices, we take a different approach since the rows and the columns 
of the matrix are indexed by characters in Σ∪{′−′}. In particular, we will represent 
a scoring matrix in Python as a dictionary of dictionaries. Given two characters 
row_char and col_char, we can access the matrix entry corresponding to this pair of 
characters via scoring_matrix[row_char][col_char].
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Takes as input a set of characters alphabet and
    three scores diag_score, off_diag_score, and dash_score.
    The function returns a dictionary of dictionaries.
    The score for any entry indexed by one or more dashes is dash_score.
    The score for the remaining diagonal entries is diag_score.
    Finally, the score for the remaining off-diagonal entries is off_diag_score.
    """
    alphabet_copy = set(alphabet)
    alphabet_copy.add('-')
    scoring_matrix = {}
    for letter_1 in alphabet_copy:
        letter_1_dict = {}
        for letter_2 in alphabet_copy:
            if (letter_2 == '-' or letter_1 == '-'):
                letter_1_dict[letter_2] = dash_score
            elif (letter_1 == letter_2):
                letter_1_dict[letter_2] = diag_score
            else:
                letter_1_dict[letter_2] = off_diag_score
        scoring_matrix[letter_1] = letter_1_dict
    return scoring_matrix


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Takes as input two sequences seq_x and seq_y whose elements share
    a common alphabet with the scoring matrix scoring_matrix. The function
    computes and returns the alignment matrix for seq_x and seq_y as described
    in the Homework. If global_flag is True, each entry of the alignment matrix
    is computed using the method described in Question 8 of the Homework.
    If global_flag is False, each entry is computed using the method described
    in Question 12 of the Homework.
    """
    alignment_matrix = [[0 for dummy_ind1 in range(len(seq_y) + 1)] 
                        for dummy_ind2 in range(len(seq_x) + 1)]
    alignment_matrix[0][0] = 0
    for id_x in range(1, len(seq_x) + 1):
        alignment_matrix[id_x][0] = alignment_matrix[id_x - 1][0] + scoring_matrix[seq_x[id_x - 1]]['-']
        if (not global_flag):
            alignment_matrix[id_x][0] = max(0, alignment_matrix[id_x][0])
    for id_y in range(1, len(seq_y) + 1):
        alignment_matrix[0][id_y] = alignment_matrix[0][id_y - 1] + scoring_matrix['-'][seq_y[id_y - 1]]
        if (not global_flag):
            alignment_matrix[0][id_y] = max(0, alignment_matrix[0][id_y])          
    for idx_x in range(1, len(seq_x) + 1):
        for idx_y in range(1, len(seq_y) + 1):
            alignment_matrix[idx_x][idx_y] = max(alignment_matrix[idx_x - 1][idx_y - 1] 
                + scoring_matrix[seq_x[idx_x - 1]][seq_y[idx_y - 1]],
                alignment_matrix[idx_x - 1][idx_y] + scoring_matrix[seq_x[idx_x - 1]]['-'],
                alignment_matrix[idx_x][idx_y - 1] + scoring_matrix['-'][seq_y[idx_y - 1]])
            if (not global_flag):
                alignment_matrix[idx_x][idx_y] = max(0, alignment_matrix[idx_x][idx_y])                
    return alignment_matrix

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share
    a common alphabet with the scoring matrix scoring_matrix. This function
    computes a global alignment of seq_x and seq_y using the global alignment matrix
    alignment_matrix.
    The function returns a tuple of the form (score, align_x, align_y) where score
    is the score of the global alignment align_x and align_y. Note that
    align_x and align_y should have the same length and may include
    the padding character '-'.
    """
    x_len = len(seq_x)
    y_len = len(seq_y)
    x_alignment = ''
    y_alignment = ''
    optimal_score = alignment_matrix[x_len][y_len]
    while x_len and y_len:
        if (alignment_matrix[x_len][y_len] == alignment_matrix[x_len - 1][y_len - 1] + scoring_matrix[seq_x[x_len - 1]][seq_y[y_len - 1]]):
            x_alignment = seq_x[x_len - 1] + x_alignment
            y_alignment = seq_y[y_len - 1] + y_alignment
            x_len -= 1
            y_len -= 1
        else:
            if (alignment_matrix[x_len][y_len] == alignment_matrix[x_len - 1][y_len] + scoring_matrix[seq_x[x_len - 1]]['-']):
                x_alignment = seq_x[x_len - 1] + x_alignment
                y_alignment = '-' + y_alignment
                x_len -= 1
            else:
                x_alignment = '-' + x_alignment
                y_alignment = seq_y[y_len - 1] + y_alignment
                y_len -= 1
    while (x_len > 0):
        x_alignment = seq_x[x_len - 1] + x_alignment
        y_alignment = '-' + y_alignment
        x_len -= 1
    while (y_len > 0):
        x_alignment = '-' + x_alignment
        y_alignment = seq_y[y_len - 1] + y_alignment
        y_len -= 1
    return optimal_score, x_alignment, y_alignment


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose
    elements share a common alphabet with the scoring
    matrix scoring_matrix. This function computes
    a local alignment of seq_x and seq_y using
    the local alignment matrix alignment_matrix. 
    The function returns a tuple of the form
    (score, align_x, align_y) where score is the score
    of the optimal local alignment align_x and align_y.
    Note that align_x and align_y should have
    the same length and may include the padding character '-'.
    """
    x_alignment = ''
    y_alignment = ''
    max_score = float('-inf')
    max_idx = (-1, -1)
    for row_num in range(len(alignment_matrix)):
        row = alignment_matrix[row_num]
        for col_num in range(len(row)):
            score = alignment_matrix[row_num][col_num]
            if (score > max_score):
                max_score = score
                max_idx = (row_num, col_num)
    idx_x, idx_y = max_idx[0], max_idx[1]
    while alignment_matrix[idx_x][idx_y] and idx_x and idx_y:
        if (alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y - 1] + scoring_matrix[seq_x[idx_x - 1]][seq_y[idx_y - 1]]):
            x_alignment = seq_x[idx_x - 1] + x_alignment
            y_alignment = seq_y[idx_y - 1] + y_alignment
            idx_x -= 1
            idx_y -= 1
        else:
            if (alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y] + scoring_matrix[seq_x[idx_x - 1]]['-']):
                x_alignment = seq_x[idx_x - 1] + x_alignment
                y_alignment = '-' + y_alignment
                idx_x -= 1
            else:
                x_alignment = '-' + x_alignment
                y_alignment = seq_y[idx_y - 1] + y_alignment
                idx_y -= 1
    while idx_x and alignment_matrix[idx_x][idx_y]:
        x_alignment = seq_x[idx_x - 1] + x_alignment
        y_alignment = '-' + y_alignment
        idx_x -= 1
    while idx_y and alignment_matrix[idx_x][idx_y]:
        x_alignment = '-' + x_alignment
        y_alignment = seq_y[idx_y - 1] + y_alignment
        idx_y -= 1
    return max_score, x_alignment, y_alignment
