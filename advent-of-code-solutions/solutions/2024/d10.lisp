;;;; 10. https://adventofcode.com/2024/day/10

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

(defun digit-grid (s)
  "S as a 2-D array of the digits it holds, plus its row and column counts."
  (let* ((rows (lines (trim s)))
         (m (length rows))
         (n (reduce #'max rows :key #'length))
         (grid (make-array (list m n) :element-type '(unsigned-byte 8)
                                      :initial-element 0)))
    (loop for row in rows
          for i from 0
          do (loop for c across row
                   for j from 0
                   do (setf (aref grid i j) (or (digit-char-p c) 0))))
    (values grid m n)))


(deftype heights () '(simple-array (unsigned-byte 8) (* *)))

;; A trail rises by exactly one at every step, so it can never return to a cell
;; it has already used. The walks below need no visited set.

(defun mark-summits (grid m n i j summits)
  "Record every 9 the trails from (I, J) reach."
  (declare (type heights grid) (type simple-bit-vector summits)
           (type fixnum m n i j))
  (let ((height (aref grid i j)))
    (if (= height 9)
        (setf (sbit summits (+ (* i n) j)) 1)
        (loop for (di dj) in '((0 1) (0 -1) (1 0) (-1 0))
              for next-i of-type fixnum = (+ i di)
              for next-j of-type fixnum = (+ j dj)
              when (and (< -1 next-i m) (< -1 next-j n)
                        (= (aref grid next-i next-j) (1+ height)))
                do (mark-summits grid m n next-i next-j summits)))))

(defun count-trails (grid m n i j)
  "How many distinct trails run from (I, J) up to a 9."
  (declare (type heights grid) (type fixnum m n i j))
  (let ((height (aref grid i j)))
    (if (= height 9)
        1
        (loop for (di dj) in '((0 1) (0 -1) (1 0) (-1 0))
              for next-i of-type fixnum = (+ i di)
              for next-j of-type fixnum = (+ j dj)
              when (and (< -1 next-i m) (< -1 next-j n)
                        (= (aref grid next-i next-j) (1+ height)))
                sum (count-trails grid m n next-i next-j)))))

(defun part-a (s)
  (multiple-value-bind (grid m n) (digit-grid s)
    (let ((summits (make-array (* m n) :element-type 'bit :initial-element 0)))
      (loop for i below m
            sum (loop for j below n
                      when (zerop (aref grid i j))
                        sum (progn
                              (fill summits 0)
                              (mark-summits grid m n i j summits)
                              (count 1 summits)))))))

(defun part-b (s)
  (multiple-value-bind (grid m n) (digit-grid s)
    (loop for i below m
          sum (loop for j below n
                    when (zerop (aref grid i j))
                      sum (count-trails grid m n i j)))))

(defparameter *test-string* "
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
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
