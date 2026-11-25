;;;; 8. https://adventofcode.com/2024/day/8

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

(defun antennas (grid m n)
  "The positions of the antennas on the map, keyed by frequency."
  (declare (type (simple-array character (* *)) grid) (type fixnum m n))
  (let ((by-frequency (make-hash-table :test #'eql)))
    (loop for i below m
          do (loop for j below n
                   for c = (aref grid i j)
                   unless (char= c #\.)
                     do (push (cons i j) (gethash c by-frequency))))
    by-frequency))

(defun mark (antinodes m n i j)
  "Record an antinode at (I, J), unless that falls off the map."
  (declare (type simple-bit-vector antinodes) (type fixnum m n i j))
  (when (and (< -1 i m) (< -1 j n))
    (setf (sbit antinodes (+ (* i n) j)) 1)))

(defun mark-line (antinodes m n i j di dj)
  "Record an antinode at (I, J) and at every (DI, DJ) step from it off the map."
  (declare (type simple-bit-vector antinodes) (type fixnum m n i j di dj))
  (loop while (and (< -1 i m) (< -1 j n))
        do (setf (sbit antinodes (+ (* i n) j)) 1)
           (incf i di)
           (incf j dj)))

(defmacro do-antenna-pairs ((ai aj bi bj di dj) grid m n &body body)
  "Run BODY for each pair of same-frequency antennas, with the step between them."
  `(loop for positions being the hash-values of (antennas ,grid ,m ,n)
         do (loop for ((,ai . ,aj) . others) on positions
                  do (loop for (,bi . ,bj) in others
                           for ,di = (- ,bi ,ai)
                           for ,dj = (- ,bj ,aj)
                           do (progn ,@body)))))

(defun part-a (s)
  (multiple-value-bind (grid m n) (char-grid s)
    (let ((antinodes (make-array (* m n) :element-type 'bit :initial-element 0)))
      (do-antenna-pairs (ai aj bi bj di dj) grid m n
        (mark antinodes m n (+ bi di) (+ bj dj))
        (mark antinodes m n (- ai di) (- aj dj)))
      (count 1 antinodes))))

(defun part-b (s)
  "The step between a pair is its full separation, so the only antinodes on the
line through them are the two antennas and the extensions past each end."
  (multiple-value-bind (grid m n) (char-grid s)
    (let ((antinodes (make-array (* m n) :element-type 'bit :initial-element 0)))
      (do-antenna-pairs (ai aj bi bj di dj) grid m n
        (mark-line antinodes m n bi bj di dj)
        (mark-line antinodes m n ai aj (- di) (- dj)))
      (count 1 antinodes))))

(defparameter *test-string* "
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
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
