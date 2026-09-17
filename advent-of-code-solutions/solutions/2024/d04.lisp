;;;; 4. https://adventofcode.com/2024/day/4

(declaim (optimize (speed 3) (safety 1)))

(defun trim (s)
  "Drop the blank lines that wrap every puzzle input."
  (string-trim '(#\Newline #\Return) s))

(defun split-on (s char)
  "The pieces of S between occurrences of CHAR."
  (loop with end = (length s)
        with start = 0
        for pos = (position char s :start start)
        collect (subseq s start (or pos end))
        while pos
        do (setf start (1+ pos))))

(defun lines (s)
  (split-on s #\Newline))

(defun char-grid (s)
  "S as a 2-D character array, plus its row and column counts.
Short rows are padded with dots so the array stays rectangular."
  (let* ((rows (lines (trim s)))
         (m (length rows))
         (n (reduce #'max rows :key #'length))
         (grid (make-array (list m n) :element-type 'character
                                      :initial-element #\.)))
    (loop for row in rows
          for i from 0
          do (loop for c across row
                   for j from 0
                   do (setf (aref grid i j) c)))
    (values grid m n)))

(deftype grid () '(simple-array character (* *)))

(deftype index ()
  "A row or column of the grid. Bounding it keeps the offset arithmetic inline."
  '(unsigned-byte 16))

(deftype offset ()
  "One step along a row or a column, in either direction or not at all."
  '(integer -1 1))

(defun xmas-at-p (grid m n i j di dj)
  "Does XMAS read from (I, J) in direction (DI, DJ)?
Only the far end is bounds-checked; the cells between it and (I, J) are inside."
  (declare (type grid grid) (type index m n i j) (type offset di dj))
  (let ((end-i (+ i (* 3 di)))
        (end-j (+ j (* 3 dj))))
    (and (< -1 end-i m) (< -1 end-j n)
         (char= (aref grid i j) #\X)
         (char= (aref grid (+ i di) (+ j dj)) #\M)
         (char= (aref grid (+ i di di) (+ j dj dj)) #\A)
         (char= (aref grid end-i end-j) #\S))))

(defun part-a (s)
  (multiple-value-bind (grid m n) (char-grid s)
    (loop for i below m
          sum (loop for j below n
                    sum (loop for (di dj) in '((0 1) (1 0) (1 1) (-1 1))
                              count (xmas-at-p grid m n i j di dj)
                              count (xmas-at-p grid m n i j (- di) (- dj)))))))

(defun mas-p (a b)
  "Do the two ends of a diagonal through an A spell MAS, either way round?"
  (or (and (char= a #\M) (char= b #\S))
      (and (char= a #\S) (char= b #\M))))

(defun part-b (s)
  (multiple-value-bind (grid m n) (char-grid s)
    (declare (type grid grid))
    (loop for i from 1 below (1- m)
          sum (loop for j from 1 below (1- n)
                    count (and (char= (aref grid i j) #\A)
                               (mas-p (aref grid (1- i) (1+ j)) (aref grid (1+ i) (1- j)))
                               (mas-p (aref grid (1- i) (1- j)) (aref grid (1+ i) (1+ j))))))))

(defparameter *test-string* "
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
")

(defun read-file (path)
  (with-open-file (in path :external-format :utf-8)
    (let ((buffer (make-string (file-length in))))
      (subseq buffer 0 (read-sequence buffer in)))))

(defun seconds ()
  (/ (get-internal-real-time) (float internal-time-units-per-second 1d0)))

(defun main ()
  (let ((s (read-file (second sb-ext:*posix-argv*))))
    (dolist (part '(part-a part-b))
      (let* ((start (seconds))
             (answer (funcall part s)))
        (format t "~A~%" answer)
        (format *error-output* "~(~A~): ~,4Fs~%" part (- (seconds) start))))))

(main)
